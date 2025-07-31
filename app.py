from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def init_db():
    conn = sqlite3.connect('users.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            mobile TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.close()

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        if user and check_password_hash(user[4], password):
            session['user'] = user[1]
            return redirect('/welcome')
        else:
            flash('Invalid email or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']
        if password != confirm:
            flash('Passwords do not match')
        else:
            hashed_pw = generate_password_hash(password)
            try:
                conn = sqlite3.connect('users.db')
                conn.execute('INSERT INTO users (name, mobile, email, password) VALUES (?, ?, ?, ?)',
                             (name, mobile, email, hashed_pw))
                conn.commit()
                conn.close()
                flash('Registration successful! Please log in.')
                return redirect('/login')
            except sqlite3.IntegrityError:
                flash('Email already exists')
    return render_template('register.html')

@app.route('/welcome')
def welcome():
    if 'user' in session:
        return render_template('welcome.html', name=session['user'])
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
