import os
import json
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import requests
from datetime import datetime

# Load environment variables
load_dotenv()

class EcommerceAnalyzer:
    def __init__(self):
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('DB_NAME', 'your_database'),
            'user': os.getenv('DB_USER', 'your_username'),
            'password': os.getenv('DB_PASSWORD'),
            'port': os.getenv('DB_PORT', '5432')
        }
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.connection = None
        
        # Event categorization
        self.event_categories = {
            'browsing': ['view_item', 'view_item_list'],
            'consideration': ['add_to_cart', 'view_cart', 'add_to_wishlist', 'remove_from_cart'],
            'conversion': ['begin_checkout', 'add_shipping_info', 'add_payment_info', 'purchase']
        }
        
    def connect_db(self):
        """Connect to PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(**self.db_config)
            print("✅ Database connected successfully")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
    
    def get_event_data(self):
        """Fetch event data from database"""
        if not self.connection:
            print("❌ No database connection")
            return None
            
        query = """
        SELECT 
            event_type,
            COUNT(*) as count,
            user_id,
            timestamp,
            session_id
        FROM events 
        GROUP BY event_type, user_id, timestamp, session_id
        ORDER BY count DESC;
        """
        
        try:
            df = pd.read_sql_query(query, self.connection)
            print("✅ Data fetched successfully")
            return df
        except Exception as e:
            print(f"❌ Error fetching data: {e}")
            return None
    
    def analyze_event_distribution(self):
        """Analyze the current event distribution"""
        # Current data from your example
        data = {
            'event_type': ['view_item', 'view_item_list', 'add_to_cart', 'view_cart', 
                          'add_to_wishlist', 'remove_from_cart', 'begin_checkout', 
                          'add_payment_info', 'add_shipping_info', 'purchase'],
            'count': [3043, 2514, 1579, 762, 489, 515, 360, 279, 266, 193]
        }
        
        df = pd.DataFrame(data)
        
        # Categorize events
        df['category'] = df['event_type'].apply(self.categorize_event)
        
        # Calculate percentages
        total_events = df['count'].sum()
        df['percentage'] = (df['count'] / total_events * 100).round(2)
        
        return df
    
    def categorize_event(self, event_type):
        """Categorize event into behavioral groups"""
        for category, events in self.event_categories.items():
            if event_type in events:
                return category
        return 'other'
    
    def create_funnel_analysis(self):
        """Create funnel analysis with conversion rates"""
        funnel_data = {
            'stage': ['Product Views', 'Cart Additions', 'Cart Views', 'Checkout Started', 
                     'Payment Info', 'Shipping Info', 'Purchase Complete'],
            'events': [3043, 1579, 762, 360, 279, 266, 193],
            'event_types': ['view_item', 'add_to_cart', 'view_cart', 'begin_checkout',
                           'add_payment_info', 'add_shipping_info', 'purchase']
        }
        
        df = pd.DataFrame(funnel_data)
        
        # Calculate conversion rates
        df['conversion_rate'] = 0.0
        for i in range(1, len(df)):
            df.loc[i, 'conversion_rate'] = (df.loc[i, 'events'] / df.loc[i-1, 'events'] * 100).round(2)
        
        # Overall conversion rate
        df.loc[0, 'conversion_rate'] = 100.0  # Starting point
        
        return df
    
    def identify_patterns(self):
        """Identify patterns and anomalies"""
        patterns = {
            'cart_abandonment_rate': ((1579 - 193) / 1579 * 100),  # 87.8%
            'checkout_abandonment': ((360 - 193) / 360 * 100),     # 46.4%
            'view_to_cart_conversion': (1579 / 3043 * 100),        # 51.9%
            'wishlist_usage': (489 / 3043 * 100),                  # 16.1%
            'cart_removal_rate': (515 / 1579 * 100),               # 32.6%
        }
        
        anomalies = []
        if patterns['cart_abandonment_rate'] > 80:
            anomalies.append("High cart abandonment rate detected")
        if patterns['checkout_abandonment'] > 40:
            anomalies.append("High checkout abandonment - payment/shipping issues?")
        if patterns['cart_removal_rate'] > 30:
            anomalies.append("High cart removal rate - pricing concerns?")
            
        return patterns, anomalies
    
    def suggest_derived_events(self):
        """Suggest new derived event categories for deeper insights"""
        return {
            'hesitant_checkout': {
                'description': 'Users who view cart multiple times before checkout',
                'logic': 'view_cart_count > 2 AND time_to_checkout > avg_time'
            },
            'price_sensitive': {
                'description': 'Users who add/remove items frequently',
                'logic': 'remove_from_cart_count >= add_to_cart_count * 0.5'
            },
            'research_intensive': {
                'description': 'High view-to-action ratio users',
                'logic': 'view_item_count > 10 AND add_to_cart_count <= 2'
            },
            'quick_deciders': {
                'description': 'Users who purchase within one session',
                'logic': 'time_from_first_view_to_purchase < 30_minutes'
            },
            'wishlist_collectors': {
                'description': 'High wishlist usage without purchase',
                'logic': 'add_to_wishlist_count > 3 AND purchase_count = 0'
            }
        }
    
    def generate_json_structure(self):
        """Generate JSON structure for Gemini API"""
        return {
            "analysis_request": {
                "data_source": "ecommerce_events",
                "event_distribution": {
                    "browsing_events": {"view_item": 3043, "view_item_list": 2514},
                    "consideration_events": {
                        "add_to_cart": 1579, "view_cart": 762, 
                        "add_to_wishlist": 489, "remove_from_cart": 515
                    },
                    "conversion_events": {
                        "begin_checkout": 360, "add_shipping_info": 266,
                        "add_payment_info": 279, "purchase": 193
                    }
                },
                "funnel_metrics": {
                    "view_to_cart_rate": 51.9,
                    "cart_to_checkout_rate": 22.8,
                    "checkout_to_purchase_rate": 53.6,
                    "overall_conversion_rate": 6.3
                },
                "behavioral_patterns": {
                    "cart_abandonment_rate": 87.8,
                    "checkout_abandonment_rate": 46.4,
                    "wishlist_usage_rate": 16.1,
                    "cart_removal_rate": 32.6
                }
            }
        }
    
    def create_gemini_prompt(self):
        """Create detailed prompt for Gemini API analysis"""
        return """
Analyze this e-commerce behavioral data and provide a comprehensive report:

DATA:
- Total Events: 9,800
- Conversion Funnel: View Item (3,043) → Add to Cart (1,579) → Begin Checkout (360) → Purchase (193)
- Supporting Events: View Cart (762), Wishlist (489), Remove from Cart (515)
- Conversion Rates: View→Cart (51.9%), Cart→Checkout (22.8%), Checkout→Purchase (53.6%)

PROVIDE ANALYSIS ON:

1. CUSTOMER SEGMENTATION (classify into 4-5 behavioral segments):
   - Segment characteristics and size
   - Behavioral patterns for each segment
   - Revenue potential ranking

2. CONVERSION BOTTLENECKS (identify top 3 critical issues):
   - Specific funnel stage problems
   - Quantified impact on revenue
   - Root cause hypotheses

3. IMPROVEMENT RECOMMENDATIONS (5 actionable strategies):
   - Priority ranking (High/Medium/Low)
   - Expected conversion lift %
   - Implementation difficulty
   - Specific tactics

4. HIGH-VALUE BEHAVIOR PATTERNS:
   - Identify power user behaviors
   - Cross-selling opportunities
   - Retention indicators

5. BUSINESS IMPACT METRICS:
   - Revenue loss from abandonment
   - Opportunity sizing
   - ROI potential for fixes

Format as a structured business report with clear headers, bullet points, and specific numbers/percentages.
"""
    
    def call_gemini_api(self, prompt):
        """Call Gemini API for analysis"""
        if not self.gemini_api_key:
            print("❌ Gemini API key not found in .env file")
            return None
            
        url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 2048
            }
        }
        
        params = {
            'key': self.gemini_api_key
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, params=params)
            if response.status_code == 200:
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                print(f"❌ API Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"❌ Error calling Gemini API: {e}")
            return None
    
    def run_complete_analysis(self):
        """Run complete analysis and generate report"""
        print("🚀 Starting E-commerce Event Analysis...")
        
        # 1. Basic Analysis
        print("\n📊 Event Distribution Analysis:")
        df = self.analyze_event_distribution()
        print(df.to_string(index=False))
        
        # 2. Funnel Analysis
        print("\n🔄 Funnel Analysis:")
        funnel = self.create_funnel_analysis()
        print(funnel.to_string(index=False))
        
        # 3. Pattern Identification
        print("\n🔍 Pattern Analysis:")
        patterns, anomalies = self.identify_patterns()
        for key, value in patterns.items():
            print(f"  {key}: {value:.2f}%")
        
        print("\n⚠️  Anomalies Detected:")
        for anomaly in anomalies:
            print(f"  • {anomaly}")
        
        # 4. Derived Events
        print("\n💡 Suggested Derived Events:")
        derived = self.suggest_derived_events()
        for event, details in derived.items():
            print(f"  {event}: {details['description']}")
        
        # 5. Gemini API Analysis
        print("\n🤖 Calling Gemini API for Advanced Analysis...")
        prompt = self.create_gemini_prompt()
        gemini_response = self.call_gemini_api(prompt)
        
        if gemini_response:
            print("\n📋 GEMINI AI ANALYSIS REPORT:")
            print("=" * 50)
            print(gemini_response)
        
        # Save results
        self.save_results(df, funnel, patterns, derived, gemini_response)
        
    def save_results(self, df, funnel, patterns, derived, gemini_response):
        """Save analysis results to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save to JSON
        results = {
            'timestamp': timestamp,
            'event_distribution': df.to_dict('records'),
            'funnel_analysis': funnel.to_dict('records'),
            'patterns': patterns,
            'derived_events': derived,
            'gemini_analysis': gemini_response
        }
        
        with open(f'analysis_results_{timestamp}.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results saved to: analysis_results_{timestamp}.json")

def main():
    """Main execution function"""
    analyzer = EcommerceAnalyzer()
    
    # Try to connect to database (optional)
    if analyzer.connect_db():
        print("Database connection successful - you can now fetch live data")
    else:
        print("Using sample data for analysis")
    
    # Run analysis
    analyzer.run_complete_analysis()

if __name__ == "__main__":
    main()