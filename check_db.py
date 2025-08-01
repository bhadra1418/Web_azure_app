import sqlite3

try:
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    print("📋 Tables found in DB:", cursor.fetchall())

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    print("\n✅ Products in DB:")
    if not products:
        print("❌ No products found.")
    else:
        for p in products:
            print(p)

except Exception as e:
    print("❌ Error:", e)

finally:
    conn.close()
