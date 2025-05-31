import psycopg2
import time
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate

class QueryAnalyzer:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="e-commerce_platform",
            user="postgres",
            password="Your Password",  # Replace with your actual password
            host="localhost"
        )
        self.cur = self.conn.cursor()
        
    def benchmark_query(self, query, name="", batch_size=1000):
        start_time = time.time()
        self.cur.execute(query)
        
        results = []
        while True:
            batch = self.cur.fetchmany(batch_size) # Fetchmany instead of fetch by size
            if not batch:
                break
            results.extend(batch)
    
        execution_time = time.time() - start_time
        print(f"\n{name} Execution Time: {execution_time:.4f} seconds")
        return results, execution_time

    def analyze_weekly_active_users(self):
        print("\n=== Weekly Active Users Analysis ===")
        
        # Basic query
        basic_query = """
        SELECT 
            DATE_TRUNC('week', timestamp) as week,
            COUNT(DISTINCT user_id) as active_users
        FROM events
        GROUP BY week
        ORDER BY week;
        """
        
        # Optimized query using date partitioning and index
        optimized_query = """
        SELECT 
            DATE_TRUNC('week', timestamp) as week,
            COUNT(DISTINCT user_id) as active_users
        FROM events
        WHERE timestamp >= CURRENT_DATE - INTERVAL '90 days'
        GROUP BY DATE_TRUNC('week', timestamp)
        ORDER BY week;
        """
        
        basic_results, basic_time = self.benchmark_query(basic_query, "Basic WAU Query")
        opt_results, opt_time = self.benchmark_query(optimized_query, "Optimized WAU Query")
        
        return basic_results, opt_results, basic_time, opt_time

    def analyze_revenue_per_category(self):
        print("\n=== Revenue per Category Analysis ===")
        
        # Basic query
        basic_query = """
        SELECT 
            p.category,
            SUM(p.price) as total_revenue
        FROM events e
        JOIN products p ON e.product_id = p.product_id
        WHERE e.event_type = 'purchased'
        GROUP BY p.category
        ORDER BY total_revenue DESC;
        """
        
        # Optimized query using index-optimized joins
        optimized_query = """
        SELECT 
            p.category,
            SUM(p.price * event_counts.purchase_count) as total_revenue
        FROM products p
        JOIN (
            SELECT product_id, COUNT(*) as purchase_count
            FROM events 
            WHERE event_type = 'purchased'
            GROUP BY product_id
        ) event_counts ON p.product_id = event_counts.product_id
        GROUP BY p.category
        ORDER BY total_revenue DESC;
        """
        
        basic_results, basic_time = self.benchmark_query(basic_query, "Basic Revenue Query")
        opt_results, opt_time = self.benchmark_query(optimized_query, "Optimized Revenue Query")
        
        return basic_results, opt_results, basic_time, opt_time

    def create_performance_report(self):
        # Run analyses
        wau_basic, wau_opt, wau_basic_time, wau_opt_time = self.analyze_weekly_active_users()
        rev_basic, rev_opt, rev_basic_time, rev_opt_time = self.analyze_revenue_per_category()
        
        # Create performance summary
        performance_summary = pd.DataFrame({
            'Query Type': ['Weekly Active Users', 'Revenue per Category'],
            'Basic Time (s)': [wau_basic_time, rev_basic_time],
            'Optimized Time (s)': [wau_opt_time, rev_opt_time],
            'Improvement (%)': [
                ((wau_basic_time - wau_opt_time) / wau_basic_time) * 100,
                ((rev_basic_time - rev_opt_time) / rev_basic_time) * 100
            ]
        })
        
        # Print results
        print("\n=== Performance Report ===")
        print("\nQuery Performance Summary:")
        print(tabulate(performance_summary, headers='keys', tablefmt='pipe', floatfmt='.4f'))

    def __del__(self):
        self.cur.close()
        self.conn.close()

if __name__ == "__main__":
    analyzer = QueryAnalyzer()
    analyzer.create_performance_report()
