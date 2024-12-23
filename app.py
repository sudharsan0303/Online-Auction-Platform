from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
from datetime import timedelta
from datetime import datetime


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads/'  # Folder where images will be stored
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')

def get_user_db_connection():
    conn = sqlite3.connect('data_base/user_data.db')
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

# Helper function to get a connection to the donar data database
def get_auction_db_connection():
    conn = sqlite3.connect('data_base/auction.db')
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('user_login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('Please log in as an admin to access this page.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username and password match admin credentials (using environment variables)
        admin_username = os.getenv('ADMIN_USERNAME', 'Admin@2024')
        admin_password = os.getenv('ADMIN_PASSWORD', 'Admin@2024Auction')

        if username == admin_username and password == admin_password:
            session['admin_logged_in'] = True  # Set admin session
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin username or password. Please try again.', 'error')
            return redirect(url_for('admin_login'))

    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin_logged_in' in session:
        return render_template('admin_dashboard.html')
    else:
        flash('Please log in to access the admin dashboard.', 'error')
        return redirect(url_for('admin_login'))


@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_user_db_connection()
        cursor = conn.cursor()

        # Query the database to check if the user exists
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session.permanent = True  # Make session permanent (optional for session lifetime)
            flash('Login successful!', 'success')
            return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
            return redirect(url_for('user_login'))

    return render_template('login_page.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        full_name = request.form['full_name']
        age = int(request.form['age'])
        email = request.form['email']
        phone = request.form['phone']
        city = request.form['city']
        username = request.form['username']
        password = request.form['password']

        # Password hash for security
        hashed_password = generate_password_hash(password)

        # Age validation (must be 18 or older)
        if age < 18:
            flash('You must be 18 years or older to create an account.', 'error')
            return redirect(url_for('create_account'))

        conn = get_user_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO users (full_name, age, email, phone, city, username, password)
                VALUES (?, ?, ?, ?, ?, ?, ? )
            ''', (full_name, age, email, phone, city, username, hashed_password))

            conn.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('user_login'))

        except sqlite3.IntegrityError:
            flash('Username already exists. Please choose another.', 'error')

        finally:
            conn.close()

    return render_template('create_account.html')

@app.route('/user_dashboard')
@login_required
def user_dashboard():
    username = session['username']
    return render_template('dashboard.html', username=username)

@app.route('/create_auction', methods=['GET', 'POST'])
@login_required
def create_auction():
    if request.method == 'POST':
        item_name = request.form['item_name']
        description = request.form['description']
        starting_bid = float(request.form['starting_bid'])
        auction_end_date = request.form['auction_end_date']
        seller_id = session['user_id']

        conn = get_auction_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO auctions (item_name, description, starting_bid, auction_end_date, seller_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (item_name, description, starting_bid, auction_end_date, seller_id))

            conn.commit()
            flash('Auction created successfully!', 'success')
            return redirect(url_for('current_auctions'))

        except sqlite3.Error as e:
            flash(f'An error occurred: {e}', 'error')
        finally:
            conn.close()

    return render_template('create_auction.html')


@app.route('/current_auctions')
def current_auctions():
    conn = get_auction_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM auctions WHERE auction_end_date > ?', (datetime.now(),))
    auctions = cursor.fetchall()
    conn.close()

    return render_template('current_auctions.html', auctions=auctions)


@app.route('/place_bid/<int:auction_id>', methods=['POST'])
@login_required
def place_bid(auction_id):
    bid_amount = float(request.form['bid_amount'])
    bidder_id = session['user_id']
    bid_time = datetime.now().isoformat()

    conn = get_auction_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT current_bid FROM auctions WHERE id = ?', (auction_id,))
    auction = cursor.fetchone()

    if auction and (auction['current_bid'] is None or bid_amount > auction['current_bid']):
        cursor.execute('''
            INSERT INTO bids (auction_id, bidder_id, bid_amount, bid_time)
            VALUES (?, ?, ?, ?)
        ''', (auction_id, bidder_id, bid_amount, bid_time))

        cursor.execute('UPDATE auctions SET current_bid = ? WHERE id = ?', (bid_amount, auction_id))
        conn.commit()
        flash('Bid placed successfully!', 'success')
    else:
        flash('Bid must be higher than the current bid.', 'error')

    conn.close()
    return redirect(url_for('current_auctions'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        identifier = request.form['identifier']  # Username or email

        conn = get_user_db_connection()
        cursor = conn.cursor()

        # Check if the identifier is an email
        cursor.execute('SELECT * FROM users WHERE email = ? OR username = ?', (identifier, identifier))
        user = cursor.fetchone()

        conn.close()

        if user:
            # Redirect the user to a password reset form where they can reset their password
            flash('User found. Please reset your password.', 'success')
            return redirect(url_for('reset_password', user_id=user['id']))
        else:
            flash('The username or email is not registered.', 'error')

    return render_template('forgot_password.html')


# Route for reset password
@app.route('/reset_password/<user_id>', methods=['GET', 'POST'])
def reset_password(user_id):
    if request.method == 'POST':
        new_password = request.form['password']
        confirm_password = request.form['confirm_password']

        if new_password == confirm_password:
            hashed_password = generate_password_hash(new_password)  # Hash the password for security

            # Update the password in the database
            conn = get_user_db_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET password = ? WHERE id = ?', (hashed_password, user_id))
            conn.commit()
            conn.close()

            flash('Your password has been reset successfully. You can now log in.', 'success')
            return redirect(url_for('user_login'))
        else:
            flash('Passwords do not match. Please try again.', 'error')

    return render_template('reset_password.html', user_id=user_id)

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

if __name__ == '__main__':
    app.run(debug=True)
