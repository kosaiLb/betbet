from flask import session
from flask.sessions import SecureCookieSessionInterface

# where `app` is your Flask Application name.
session_cookie = SecureCookieSessionInterface().get_signing_serializer(app)

app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

@app.route('/set')
def set():
    session['key'] = 'value'
    return 'ok'

@app.route('/get')
def get():
    return session.get('key', 'not set')

if __name__ == '__main__':
    app.run(debug=True)
