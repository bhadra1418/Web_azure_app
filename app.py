from flask import Flask, render_template, request, redirect, session, flash, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ---------------------- DB INITIALIZATION ----------------------
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mobile TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Create products table
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')

    # ✅ Create cart table
    c.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    ''')

    # Optional: Add products if not already inserted
    
    existing = c.execute('SELECT COUNT(*) FROM products').fetchone()[0]
    if existing == 0:
        products = [
            ('Wireless Mouse', 499, 20),
            ('Bluetooth Speaker', 1299, 15),
            ('USB-C Hub', 799, 25),
            ('Laptop Stand', 999, 10),
            ('Mechanical Keyboard', 2499, 8),
            ('Noise Cancelling Headphones', 3499, 12),
            ('Smart LED Bulb', 499, 30),
            ('Smartphone Holder', 299, 50),
            ('Webcam 1080p', 999, 2),
            ('Portable SSD 1TB', 5499, 0)
        ]
        # Insert products into the database
        c.executemany('INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)', products)

    conn.commit()
    conn.close()


# ---------------------- ROUTES ----------------------
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
            session['email'] = user[3]
            session['cart'] = {}
            return redirect('/products')
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

@app.route('/products')
def products():
    if 'user' not in session:
        return redirect('/login')
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    products = c.execute("SELECT * FROM products WHERE quantity > 0").fetchall()

    user = session['user']
    user_id = c.execute("SELECT id FROM users WHERE name = ?", (user,)).fetchone()[0]

    cart_items = c.execute("""
        SELECT p.name, p.price, c.quantity, p.price * c.quantity as subtotal
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = ?
    """, (user_id,)).fetchall()

    cart_total = sum(item[3] for item in cart_items)

    conn.close()
    return render_template('products.html', name=user, products=products, cart_items=cart_items, cart_total=cart_total)



@app.route('/add_to_cart/<int:product_id>', methods=['GET'])
def add_to_cart(product_id):
    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Get user ID
    user = session['user']
    user_id = c.execute('SELECT id FROM users WHERE name = ?', (user,)).fetchone()[0]

    # Get available product quantity
    available_quantity = c.execute(
        'SELECT quantity FROM products WHERE id = ?', (product_id,)
    ).fetchone()

    if not available_quantity:
        conn.close()
        flash("Product not found.")
        return redirect('/products')

    available_quantity = available_quantity[0]

    # Get current quantity in cart
    existing = c.execute(
        'SELECT id, quantity FROM cart WHERE user_id = ? AND product_id = ?',
        (user_id, product_id)
    ).fetchone()

    current_in_cart = existing[1] if existing else 0

    if current_in_cart < available_quantity:
        if existing:
            # Update cart quantity
            c.execute('UPDATE cart SET quantity = quantity + 1 WHERE id = ?', (existing[0],))
        else:
            # Insert new entry
            c.execute('INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)',
                      (user_id, product_id, 1))
        flash("Item added to cart.")
    else:
        flash(f"Only {available_quantity} available in stock. Already in cart: {current_in_cart}")

    conn.commit()
    conn.close()

    return redirect('/products')


@app.route('/remove_from_cart/<product_name>', methods=['POST'])
def remove_from_cart(product_name):
    if 'user' not in session:
        return redirect('/login')
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    user = session['user']
    user_id = c.execute("SELECT id FROM users WHERE name = ?", (user,)).fetchone()[0]
    product_id = c.execute("SELECT id FROM products WHERE name = ?", (product_name,)).fetchone()[0]

    # remove just one quantity or whole entry
    c.execute("DELETE FROM cart WHERE user_id = ? AND product_id = ?", (user_id, product_id))

    conn.commit()
    conn.close()
    return redirect('/products')



@app.route('/cart')
def cart():
    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    user = session['user']
    user_id = c.execute("SELECT id FROM users WHERE name = ?", (user,)).fetchone()[0]

    cart_items = c.execute("""
        SELECT p.name, p.price, c.quantity, p.price * c.quantity as subtotal
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = ?
    """, (user_id,)).fetchall()

    cart_total = sum(item[3] for item in cart_items)
    conn.close()

    return render_template('cart.html', cart_items=cart_items, cart_total=cart_total)


@app.route('/pay')
def pay():
    if 'user' not in session:
        return redirect('/login')
    
    user = session['user']

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Get user_id
    user_id = c.execute("SELECT id FROM users WHERE name = ?", (user,)).fetchone()[0]

    # Fetch cart items
    cart_items = c.execute("""
        SELECT product_id, quantity FROM cart WHERE user_id = ?
    """, (user_id,)).fetchall()

    # Reduce quantity in products
    for product_id, qty_ordered in cart_items:
        current_qty = c.execute("SELECT quantity FROM products WHERE id = ?", (product_id,)).fetchone()[0]
        new_qty = max(0, current_qty - qty_ordered)
        c.execute("UPDATE products SET quantity = ? WHERE id = ?", (new_qty, product_id))

    # Clear cart
    c.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))

    conn.commit()
    conn.close()

    return render_template('order_success.html', name=user)



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ---------------------- MAIN ----------------------
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
