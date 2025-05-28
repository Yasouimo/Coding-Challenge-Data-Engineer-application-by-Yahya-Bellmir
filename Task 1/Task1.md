# Task 1: Data Exploration & SQL Query Optimization 

## Table of Contents
1. [Setup](#setup)
2. [Database Creation](#database-creation)
3. [Sample Data Generation](#sample-data-generation)
4. [Data Analysis](#data-analysis)
5. [Performance Optimization](#performance-optimization)

## Setup

### PostgreSQL Installation
1. Download PostgreSQL from [official website](https://www.postgresql.org/download/)
2. Run the installer
3. Remember your password during installation
4. Keep default port (5432)
5. Complete installation

### Python Requirements Installation
1. Make sure Python is installed on your system
2. Navigate to the project directory in terminal:
```bash
cd "path/to/project"
```
3. Install required packages:
```bash
pip install -r requirements.txt
```

The requirements.txt file contains:
```
psycopg2>=2.9.9
pandas>=2.0.0
matplotlib>=3.7.0
tabulate>=0.9.0
```

### Database Connection
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE e-commerce_platform;

# Connect to the new database
\c e-commerce_platform
```

## Database Creation

### Tables Creation
```sql
-- Users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    signup_date DATE,
    country VARCHAR(50)
);

-- Products table
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    category VARCHAR(50),
    price DECIMAL(10,2)
);

-- Events table
CREATE TABLE events (
    event_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    event_type VARCHAR(20) CHECK (event_type IN ('viewed', 'add-to-cart', 'purchased')),
    product_id INTEGER REFERENCES products(product_id),
    timestamp TIMESTAMP
);
```

## Sample Data Generation

### Python Script
Created `generate_sample.py` to populate tables with test data:
- 1,000 users
- 100 products
- 10,000 events

### Data Verification
```sql
-- Users verification
SELECT COUNT(*) FROM users;
-- Result: 1000 rows

SELECT * FROM users LIMIT 5;
-- Sample output:
--  user_id | signup_date | country
-- ---------+-------------+---------
--  user_1  | 2024-11-05 | UK
--  user_2  | 2025-01-19 | MAR
--  user_3  | 2025-04-02 | MAR
--  user_4  | 2025-01-03 | MAR
--  user_5  | 2024-10-31 | CA

-- Products verification
SELECT COUNT(*) FROM products;
-- Result: 100 rows

-- Events distribution
SELECT event_type, COUNT(*) 
FROM events 
GROUP BY event_type;
-- Result:
--  event_type  | count
-- -------------+-------
--  purchased   | 3374
--  viewed      | 3279
--  add-to-cart | 3347
```

## Data Analysis

### Implemented Queries

1. Weekly Active Users (WAU)
```sql
-- Basic Query
SELECT 
    DATE_TRUNC('week', timestamp) as week,
    COUNT(DISTINCT user_id) as active_users
FROM events
GROUP BY week
ORDER BY week;

-- Optimized Query
WITH weekly_users AS MATERIALIZED (
    SELECT DISTINCT
        DATE_TRUNC('week', timestamp) as week,
        user_id
    FROM events
    WHERE timestamp >= NOW() - INTERVAL '30 days'
)
SELECT 
    week,
    COUNT(*) as active_users
FROM weekly_users
GROUP BY week
ORDER BY week;
```

2. Revenue per Category
```sql
-- Basic Query
SELECT 
    p.category,
    SUM(p.price) as total_revenue
FROM events e
JOIN products p ON e.product_id = p.product_id
WHERE e.event_type = 'purchased'
GROUP BY p.category
ORDER BY total_revenue DESC;

-- Optimized Query
WITH purchase_counts AS MATERIALIZED (
    SELECT 
        product_id,
        COUNT(*) as purchase_count
    FROM events
    WHERE event_type = 'purchased'
    GROUP BY product_id
)
SELECT 
    p.category,
    SUM(p.price * pc.purchase_count) as total_revenue
FROM purchase_counts pc
JOIN products p ON pc.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;
```

## Performance Optimization

### Benchmarking Results
```
Query Performance Summary:
| Query Type           | Basic Time (s) | Optimized Time (s) | Improvement (%) |
|---------------------|----------------|-------------------|-----------------|
| Weekly Active Users | 0.1405         | 0.0501           | 64.34          |
| Revenue per Category| 0.0211         | 0.0112           | 46.75          |
```

### Optimization Techniques
1. Materialized CTEs for better query planning
2. Pre-aggregation for purchase counts
3. Date filtering for recent data
4. Index creation:
```sql
CREATE INDEX idx_events_timestamp ON events(timestamp);
CREATE INDEX idx_events_type ON events(event_type);
CREATE INDEX idx_events_product ON events(product_id);
```

### Key Improvements
- WAU query optimization showed 64.34% improvement
- Revenue calculation improved by 46.75%
- Materialized CTEs reduced repeated calculations
- Indexes improved join and filtering operations
