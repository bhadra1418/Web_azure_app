import sqlite3

conn = sqlite3.connect("users.db")
c = conn.cursor()

# Tables
print("📋 Tables found in DB:", list(c.execute("SELECT name FROM sqlite_master WHERE type='table';")))

# Users
print("\n✅ Users in DB:")
for row in c.execute("SELECT * FROM users"):
    print(row)

# Products
print("\n✅ Products in DB:")
for row in c.execute("SELECT * FROM products"):
    print(row)

# Cart
print("\n✅ Cart Contents:")
for row in c.execute("SELECT * FROM cart"):
    print(row)

conn.close()
