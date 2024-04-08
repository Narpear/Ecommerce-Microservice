from flask import Flask, render_template
import socket

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/health')
def health():
    return jsonify(
        status = "UP"
    )

if __name__ == '__main__':
    app.run()