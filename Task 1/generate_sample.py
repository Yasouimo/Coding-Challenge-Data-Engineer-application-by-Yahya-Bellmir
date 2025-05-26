import psycopg2
import random
from datetime import datetime, timedelta

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname="e-commerce_platform",  # Updated database name
        user="postgres",
        password="789456123",
        host="localhost"
    )
    cur = conn.cursor()

    # Clear existing data (optional - remove if you want to keep existing data)
    cur.execute("TRUNCATE TABLE events, products, users CASCADE")

    # Generate users
    print("Generating users...")
    countries = ['US', 'UK', 'MAR', 'FR', 'CA', 'JP']
    for i in range(1, 1001):
        user_id = f"user_{i}"
        signup_date = datetime.now() - timedelta(days=random.randint(1, 365))
        country = random.choice(countries)
        cur.execute("INSERT INTO users VALUES (%s, %s, %s)", (user_id, signup_date, country))

    # Generate products
    print("Generating products...")
    categories = ['Electronics', 'Clothing', 'Home', 'Books', 'Toys']
    for i in range(1, 101):
        product_id = f"prod_{i}"
        category = random.choice(categories)
        price = round(random.uniform(5, 500), 2)
        cur.execute("INSERT INTO products VALUES (%s, %s, %s)", (product_id, category, price))

    # Generate events
    print("Generating events...")
    event_types = ['viewed', 'add-to-cart', 'purchased']
    for i in range(1, 10001):
        user_id = f"user_{random.randint(1, 1000)}"
        event_type = random.choice(event_types)
        product_id = f"prod_{random.randint(1, 100)}"
        timestamp = datetime.now() - timedelta(days=random.randint(0, 30))
        cur.execute("INSERT INTO events VALUES (%s, %s, %s, %s)", 
                    (user_id, event_type, product_id, timestamp))

    conn.commit()
    print("Sample data generated successfully!")

except psycopg2.Error as e:
    print(f"An error occurred: {e}")
finally:
    if cur:
        cur.close()
    if conn:
        conn.close()