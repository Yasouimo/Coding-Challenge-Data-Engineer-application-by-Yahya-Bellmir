import psycopg2
import random
from datetime import datetime, timedelta

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname="e-commerce_platform",
        user="postgres",
        password="789456123",
        host="localhost"
    )
    cur = conn.cursor()

    # Clear existing data
    cur.execute("TRUNCATE TABLE events, products, users CASCADE")

    # Generate users
    print("Generating users...")
    countries = ['US', 'UK', 'MAR', 'FR', 'CA', 'JP']
    for i in range(1, 1001):
        signup_date = datetime.now() - timedelta(days=random.randint(1, 365))
        country = random.choice(countries)
        cur.execute("INSERT INTO users (signup_date, country) VALUES (%s, %s)", 
                   (signup_date, country))

    # Generate products
    print("Generating products...")
    categories = ['Electronics', 'Clothing', 'Home', 'Books', 'Toys']
    for i in range(1, 101):
        category = random.choice(categories)
        price = round(random.uniform(5, 500), 2)
        cur.execute("INSERT INTO products (category, price) VALUES (%s, %s)", 
                   (category, price))

    # Generate events
    print("Generating events...")
    event_types = [
        'view_item',
        'view_item_list',
        'add_to_cart',
        'view_cart',
        'remove_from_cart',
        'add_to_wishlist',
        'begin_checkout',
        'add_payment_info',
        'add_shipping_info',
        'purchase'
    ]
    
    # Create weighted probabilities for event types (some events should occur more frequently than others)
    event_weights = {
        'view_item': 30,
        'view_item_list': 25,
        'add_to_cart': 15,
        'view_cart': 8,
        'remove_from_cart': 5,
        'add_to_wishlist': 5,
        'begin_checkout': 4,
        'add_payment_info': 3,
        'add_shipping_info': 3,
        'purchase': 2
    }

    for i in range(1, 10001):
        user_id = random.randint(1, 1000)
        event_type = random.choices(
            population=list(event_weights.keys()),
            weights=list(event_weights.values())
        )[0]
        product_id = random.randint(1, 100)
        timestamp = datetime.now() - timedelta(days=random.randint(0, 30))
        cur.execute("INSERT INTO events (user_id, event_type, product_id, timestamp) VALUES (%s, %s, %s, %s)", 
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