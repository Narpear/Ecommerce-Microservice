from flask import Flask, render_template, request, url_for, redirect, flash, session, abort, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
import yaml
import json
import time

app = Flask(__name__)
app.secret_key = 'lalala'

# Configure the database
with open(r'C:\Users\prerk\OneDrive\Desktop\Prerana\PESU\Sem 6\CC\Ecommerce-Microservice\src\db.yaml', 'r') as yamlfile:
    db = yaml.load(yamlfile, Loader=yaml.FullLoader)

print("Database connection established")


# Load the fruits data
with open('fruits.json', 'r') as f:
    fruits = json.load(f)

print("Fruits loaded")

bought_items = {}
    
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
                return redirect(url_for('shop_render'))
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
        return redirect(url_for('shop_render'))

        cur.close()

    return render_template('register.html')


@app.route('/shop', methods=['GET'])
def shop_render():
    return render_template('shop.html', fruits=fruits)

@app.route('/shop', methods=['POST'])
def shop_submit():
    quantities = request.form
    # print("quantities: ", quantities)
    for key, value in quantities.items():
        if value!='0':
            bought_items[key] = int(value)
    print(bought_items)
    return redirect(url_for('billing'))

@app.route('/billing', methods=['GET'])
def billing():
    items_prices_quantities = {}
    total = 0
    for fruit, quantity in bought_items.items():
        price = fruits[fruit]["price"]
        subtotal = quantity*price
        items_prices_quantities[fruit] = {"quantity": quantity, "price": price, "subtotal": subtotal} 
        total += subtotal
    print(items_prices_quantities)
    time.sleep(1)
    return render_template('billing.html', items=items_prices_quantities, total=total)


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
