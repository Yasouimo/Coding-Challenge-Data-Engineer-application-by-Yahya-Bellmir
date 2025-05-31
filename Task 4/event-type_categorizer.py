import os
import json
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

class EcommerceEventAnalyzer:
    def __init__(self):
        self.db_params = {
            'dbname': 'e-commerce_platform',
            'user': 'postgres',
            'password': 'YourPasswordHere',
            'host': 'localhost'
        }
        self.connection = None
        
    def connect_db(self):
        """Connect to PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(**self.db_params)
            print("✅ Database connected successfully")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
    
    def fetch_event_data(self):
        """Fetch event data from database"""
        if not self.connection:
            print("❌ No database connection")
            return None
            
        query = """
        SELECT 
            event_type,
            COUNT(*) as event_count,
            COUNT(DISTINCT user_id) as unique_users
        FROM events 
        GROUP BY event_type
        ORDER BY event_count DESC;
        """
        
        try:
            df = pd.read_sql_query(query, self.connection)
            print(f"✅ Fetched {len(df)} event types from database")
            return df
        except Exception as e:
            print(f"❌ Error fetching event data: {e}")
            return None

    def categorize_events(self, events_data):
        """Simple rule-based event categorization"""
        categorization = {
            "browsing": [],
            "consideration": [], 
            "conversion": [],
            "retention": []
        }
        
        for _, row in events_data.iterrows():
            event_type = row['event_type'].lower()
            
            if any(keyword in event_type for keyword in ['view', 'browse', 'search']):
                categorization["browsing"].append(row['event_type'])
            elif any(keyword in event_type for keyword in ['cart', 'wishlist']):
                categorization["consideration"].append(row['event_type'])
            elif any(keyword in event_type for keyword in ['purchase', 'checkout', 'payment']):
                categorization["conversion"].append(row['event_type'])
            elif any(keyword in event_type for keyword in ['return', 'review']):
                categorization["retention"].append(row['event_type'])
            else:
                categorization["browsing"].append(row['event_type'])
        
        return categorization

    def analyze_categories(self, categorization):
        """Enhanced analysis with detailed event types per category"""
        total_events = sum(len(category) for category in categorization.values())
        
        analysis = {
            "analysis_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "summary": {
                "total_events": total_events,
                "category_distribution": {
                    category: {
                        "count": len(events),
                        "percentage": round((len(events) / total_events) * 100, 1),
                        "event_types": events
                    }
                    for category, events in categorization.items()
                }
            },
            "insights": []
        }
        
        # Add detailed insights
        for category, events in categorization.items():
            if events:
                percentage = (len(events) / total_events) * 100
                analysis["insights"].append({
                    "category": category.title(),
                    "event_count": len(events),
                    "percentage": round(percentage, 1),
                    "events": events
                })
        
        # Save analysis to JSON file
        output_file = "event_analysis_results.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=4)
        print(f"\n💾 Analysis saved to {output_file}")
        
        return analysis

    def run_analysis(self):
        """Main analysis workflow"""
        print("🚀 Starting E-commerce Event Analysis...")
        
        if not self.connect_db():
            return
        
        event_data = self.fetch_event_data()
        if event_data is None:
            return
        
        print("\n📊 Event Types Found:")
        for _, row in event_data.iterrows():
            print(f"  - {row['event_type']}: {row['event_count']} events")
        
        categorization = self.categorize_events(event_data)
        analysis = self.analyze_categories(categorization)
        
        print("\n📈 Analysis Results:")
        for insight in analysis["insights"]:
            print(f"  - {insight}")
    
    def close_connection(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("\n🔐 Database connection closed")

def main():
    analyzer = EcommerceEventAnalyzer()
    try:
        analyzer.run_analysis()
    finally:
        analyzer.close_connection()

if __name__ == "__main__":
    main()