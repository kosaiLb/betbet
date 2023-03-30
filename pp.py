import re
from flask import Flask, render_template, url_for, request, jsonify, session, redirect
import mysql.connector
from flask_cors import cross_origin

app = Flask(__name__)
app.secret_key = "secretkey"


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

def user_exist(email, password):
    cur.execute("SELECT user_id, user_status FROM users WHERE user_email=%s AND user_password=%s", [(email), (password)])
    for row in cur:
        return True, row
    return False, False

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
        print(reg_email)
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

@app.route("/login", methods=["GET", "POST"])
@cross_origin()
def login():
    if request.method == 'GET':
        return render_template('login.html', title='Login')

    elif request.method == 'POST':
        log_email = request.form.get('log_email')
        log_pass = request.form.get("log_pass")

        if not check_email(log_email):
            data = { "status" : 0, "msg" : "invalid Email"}

        else:
            res, user_data = user_exist(log_email, log_pass)
            if res == False:
                data = { "status" : 0, "msg" : "email or password are wrong" }
            else:
                data = { "status" : 1, "msg" : "login successfully"}
                print(f"dsd {user_data[0]}")
                session["user_id"] = user_data[0]
                session["user_email"] = log_email
                print(session.keys(), session.values)
                return redirect(url_for("dashboard"))
        return jsonify(data)

@app.route("/dashboard", methods=["GET"])
@cross_origin()
def dashboard():
    print(session.keys(), session.values)
    if "user_id" in session:
        user_id = session["user_id"]
        print(user_id)
        return render_template(
            'dashboard.html',
            title='Dashboard',
            user_id=user_id
        )
    else:
        return redirect(url_for("login"))
            
if __name__ == '__main__':
    app.run(debug=True)
