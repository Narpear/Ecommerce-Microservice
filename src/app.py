from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
import json
import time

app = Flask(__name__)
app.secret_key = 'lalala'

# Load the fruits data
with open('fruits.json', 'r') as f:
    fruits = json.load(f)
print("Fruits loaded")

bought_items = {}


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Load existing users
        try:
            with open('users.json', 'r') as f:
                users = json.load(f)
        except FileNotFoundError:
            users = {} # Initialize users as an empty dictionary if the file does not exist

        # Check if user exists and password is correct
        if email in users and users[email]['password'] == password:
            flash('Login successful.', 'success')
            return redirect(url_for('shop_render'))

        flash('Incorrect email or password. Please try again.', 'error')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('username')

        # Load existing users
        try:
            with open('users.json', 'r') as f:
                users = json.load(f)
        except FileNotFoundError:
            users = {} # Initialize users as an empty dictionary if the file does not exist

        # Check if user already exists
        if email in users:
            flash('User already exists. Please log in.', 'error')
            return redirect(url_for('login'))

        # Append new user to the dictionary
        users[email] = {"name": name, "password": password}

        # Save the updated dictionary back to the file
        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4)

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('shop_render'))

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
