import re, hashlib, time
from flask import Flask, render_template, url_for, request, jsonify, redirect, session
from flask_cors import cross_origin

import mysql.connector

app = Flask(__name__)

conn = mysql.connector.connect(
    host='127.0.0.1',
    port= 3306,
    user='root',
    password='k11',
    database='bet_db'
)

cur = conn.cursor()
# cur.execute()
# cur.close()
# conn.close()

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
def check_email(email):
    if(re.fullmatch(email_regex, email)):
        return True
    return False

def email_exist(email):
    sql = "SELECT * FROM users WHERE user_email=%s"
    cur.execute(sql, [(email)])
    res = cur.fetchone()
    if cur.rowcount > 0:
        return True
    return False
 

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template('register.html', title='Register')
        
    elif request.method == 'POST':
        reg_email = request.form.get('reg_email')
        reg_pass = request.form.get("reg_pass")

        if not check_email(reg_email):
            data = { "status" : 0, "msg" : "invalid Email"}

        elif email_exist(reg_email):
            data = { "status" : 0, "msg" : "Email Exist"}

        else:
            sql = "INSERT INTO users (user_email, user_password, user_status, user_referer_id) VALUES (%s, %s, %s, %s)"
            val = (reg_email, reg_pass, 1, 1)
            cur.execute(sql, val)
            conn.commit()

            data = { "status" : 1, "msg" : "User registred successfully"}
        return jsonify(data)

def user_exist(email, password):
    cur.execute("SELECT user_id, user_status FROM users WHERE user_email=%s AND user_password=%s", [(email), (password)])
    for row in cur:
        return True, row
    return False, False

def get_user_if_connected(browser_hash):
    cur.execute("SELECT * FROM users WHERE user_conn_hash=%s", [(browser_hash)])
    for row in cur:
        return True, row
    return False, False   

@app.route("/login", methods=["GET", "POST"])
@cross_origin()
def login():
    if request.method == 'GET':
        return render_template('login.html', title='Login')

    elif request.method == 'POST':
        if request.form.get('browser_log_hash'):

            browser_log_hash = request.form.get('browser_log_hash')
            conn_status, user_data = get_user_if_connected(browser_log_hash)

            if conn_status:
                data = { "status" : 1, "msg" : "connected" }
            else:
                data = { "status" : 0, "msg" : "not connected" }
                
            return jsonify(data)

        elif request.form.get('log_email'):
            log_email = request.form.get('log_email')
            log_pass = request.form.get("log_pass")

            if not check_email(log_email):
                data = { "status" : 0, "msg" : "invalid Email"}

            else:
                res, user_data = user_exist(log_email, log_pass)
                if res == False:
                    data = { "status" : 0, "msg" : "email or password are wrong" }

                else:
                    # log_hash = hashlib.sha256(b"password").hexdigest()
                    h = hashlib.sha256()
                    h.update(bin(int(time.time())).encode('utf-8'))
                    h.update(bin(user_data[0]).encode('utf-8'))
                    log_hash = h.hexdigest()

                    cur.execute(
                        "UPDATE users SET user_conn_hash = %s WHERE user_id = %s", 
                        (log_hash, user_data[0])
                    )
                    conn.commit()

                    data = {
                        "status" : 1,
                        "msg" : "login successfully",
                        "session" : log_hash,
                        "log_user_id" : user_data[0]
                    }
                                   
            return jsonify(data)

@app.route("/dash", methods=["GET", "POST"])
@cross_origin()
def dash():
    if request.method == 'GET':
        if "log_hash" in session:
            return render_template('dashboard.html', title='Dash')
    return "<p>not</p>"



if __name__ == '__main__':
    app.run(debug=True)
