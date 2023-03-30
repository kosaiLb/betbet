import mysql.connector

conn = mysql.connector.connect(
    host='127.0.0.1',
    port= 3306,
    user='root',
    password='k11',
    database='bet_db'
)

cur = conn.cursor()

cur.execute(
"""
create table users(
    user_id int(14) primary key auto_increment,
    user_email varchar(265) not null,
    user_password varchar(265) not null,
    user_status bool not null,
    user_firstname varchar(50),
    user_lastname varchar(50),
    user_birthday date
)
"""
)





# cur.execute("SELECT user_id FROM users WHERE user_email=%s", [('dwwdwdw@www.ww')])
# res = cur.rowcount
# res = cur.fetchone()
# print(res)

# cur.execute("drop table users;")

# cur.execute(
# """
# create table users(
# user_id int(14) primary key auto_increment,
# user_firstname varchar(50),
# user_lastname varchar(50),
# user_birthday date,
# user_email varchar(265) not null,
# user_password varchar(265) not null,
# user_status bool not null,
# user_referer_id int(14) not null,
# user_ip varchar(265)
# )
# """
# )
