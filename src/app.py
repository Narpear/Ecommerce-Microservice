from flask import Flask, render_template, request, url_for, redirect, flash, session, abort, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import requests
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
app.secret_key = 'lalala'

# Configure the database
with open(r'C:\Users\prerk\OneDrive\Desktop\Prerana\PESU\Sem 6\CC\Ecommerce-Microservice\src\db.yaml', 'r') as yamlfile:
    db = yaml.load(yamlfile, Loader=yaml.FullLoader)

print("Database connection established")

app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)
print("Database found")

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE email = %s", (email,))
        existing_user = cur.fetchone()

        if existing_user:
            if check_password_hash(existing_user[2], password):
                flash('Login successful.', 'success')
                return redirect(url_for('success'))
            else:
                flash('Incorrect password. Please try again.', 'error')
        else:
            flash('Email not found. Please register.', 'error')

        cur.close()

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('username')

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE email = %s", (email,))
        existing_user = cur.fetchone()

        if existing_user:
            flash('User already exists. Please log in.', 'error')
            return redirect(url_for('login'))

        hashed_password = generate_password_hash(password)
        cur.execute("INSERT INTO user (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
        mysql.connection.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('success'))

        cur.close()

    return render_template('register.html')

@app.route('/success')
def success():
    return '<h1>Success!<h1>'

@app.route('/health')
def health():
    return jsonify(
        status="UP"
    )

if __name__ == '__main__':
    app.run()
