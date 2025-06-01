import os
import json
import pandas as pd
import psycopg2
import requests
from dotenv import load_dotenv
from datetime import datetime
from collections import Counter, defaultdict
import time

# Load environment variables
load_dotenv()

class DynamicEcommerceEventAnalyzer:
    def __init__(self):
        self.db_params = {
            'dbname': 'e-commerce_platform',
            'user': 'postgres',
            'password': 'YourPasswordHere',
            'host': 'localhost'
        }
        self.connection = None
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model_name = "tinyllama"
        self.valid_categories = {
            "Browsing", "Consideration", "Conversion", "Removal"
        }
        
    def connect_db(self):
        """Connect to PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(**self.db_params)
            print("✅ Connected to database")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
    
    def fetch_event_data(self):
        """Fetch event types with their counts from database"""
        query = """
        SELECT 
            event_type, 
            COUNT(*) as event_count
        FROM events 
        GROUP BY event_type 
        ORDER BY event_count DESC;
        """
        
        try:
            df = pd.read_sql_query(query, self.connection)
            print(f"✅ Fetched {len(df)} unique event types with counts")
            return df
        except Exception as e:
            print(f"❌ Error fetching events: {e}")
            return None

    def analyze_event_pattern(self, event_type):
        """Let TinyLlama analyze the event and suggest a category name"""
        
        prompt = f"""Categorize this e-commerce event into exactly one of these four categories:
- Browsing: Viewing products or pages without clear intent to purchase
- Consideration: Showing interest in products but not yet committing
- Conversion: Actions that directly lead to or represent a purchase
- Removal: Removing items from cart or wishlist

Event: "{event_type}"
Respond with only the category name (Browsing, Consideration, Conversion, or Removal) and nothing else."""

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "top_p": 0.9,
                "max_tokens": 15,
                "repeat_penalty": 1.2
            }
        }
        
        try:
            response = requests.post(self.ollama_url, json=payload, timeout=30)
            response.raise_for_status()
            raw_response = response.json()['response'].strip()
            
            # Clean and standardize the response
            clean_response = raw_response.split('\n')[0].strip().title()
            
            # Validate against our strict categories
            for category in self.valid_categories:
                if category.lower() in clean_response.lower():
                    return category
            
            # If no clear match found, use a fallback strategy
            return self.fallback_categorization(event_type)
                
        except Exception as e:
            print(f"❌ Ollama Error: {e}")
            return self.fallback_categorization(event_type)

    def fallback_categorization(self, event_type):
        """Fallback categorization when LLM response isn't clear"""
        event_lower = event_type.lower()
        
        # Browsing patterns
        if any(verb in event_lower for verb in ['view', 'look', 'browse', 'search']):
            return "Browsing"
            
        # Consideration patterns
        elif any(verb in event_lower for verb in ['add', 'save', 'wishlist', 'compare']):
            return "Consideration"
            
        # Conversion patterns
        elif any(verb in event_lower for verb in ['purchase', 'buy', 'checkout', 'pay', 'complete']):
            return "Conversion"
            
        # Removal patterns
        elif any(verb in event_lower for verb in ['remove', 'delete', 'cancel']):
            return "Removal"
            
        return "Consideration"  # Default fallback

    def consolidate_similar_categories(self, categorizations):
        """Ensure all categories are in our strict set"""
        for cat_record in categorizations:
            if cat_record['category'] not in self.valid_categories:
                # Re-categorize using our fallback method
                cat_record['category'] = self.fallback_categorization(cat_record['event_type'])
                cat_record['was_corrected'] = True
            else:
                cat_record['was_corrected'] = False
        return categorizations

    def run_analysis(self):
        """Main workflow: Strict categorization with four classes"""
        print("🚀 Starting Strict Event Categorization Analysis")
        print("   🤖 Using only: Browsing, Consideration, Conversion, Removal")
        
        # Step 1: Connect to database
        if not self.connect_db():
            return
        
        # Step 2: Fetch event data with counts
        event_data = self.fetch_event_data()
        if event_data is None or event_data.empty:
            return
        
        print(f"\n🔍 Analyzing {len(event_data)} unique event types...")
        
        # Step 3: Categorize each event
        categorizations = []
        
        for idx, row in event_data.iterrows():
            event_type = row['event_type']
            event_count = row['event_count']
            
            print(f"  [{idx+1}/{len(event_data)}] Analyzing: {event_type}")
            
            suggested_category = self.analyze_event_pattern(event_type)
            
            categorizations.append({
                "event_type": event_type,
                "event_count": int(event_count),
                "category": suggested_category,
                "discovery_order": idx + 1
            })
            
            print(f"    → {suggested_category}")
            time.sleep(0.1)
        
        # Step 4: Ensure strict categorization
        categorizations = self.consolidate_similar_categories(categorizations)
        
        # Step 5: Generate analysis
        total_events = sum(row['event_count'] for _, row in event_data.iterrows())
        category_totals = Counter()
        category_type_counts = Counter()
        
        for cat_record in categorizations:
            category = cat_record['category']
            category_totals[category] += cat_record['event_count']
            category_type_counts[category] += 1
        
        analysis_summary = {
            "total_unique_event_types": len(event_data),
            "total_events_processed": int(total_events),
            "category_distribution": dict(category_totals),
            "category_type_counts": dict(category_type_counts),
            "top_categories": category_totals.most_common(),
            "category_insights": self.generate_category_insights(categorizations)
        }
        
        # Prepare final results
        results = {
            "analysis_metadata": {
                "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "categories_used": list(self.valid_categories),
                "model_used": self.model_name
            },
            "analysis_summary": analysis_summary,
            "detailed_categorizations": sorted(categorizations, key=lambda x: x['event_count'], reverse=True)
        }
        
        # Save results
        output_filename = "strict_event_categorization.json"
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        self.print_analysis_summary(analysis_summary)
        print(f"\n💾 Results saved to '{output_filename}'")
        
        return results

    def generate_category_insights(self, categorizations):
        """Generate insights about category distribution"""
        insights = {}
        category_events = defaultdict(list)
        
        for cat_record in categorizations:
            category_events[cat_record['category']].append({
                'event_type': cat_record['event_type'],
                'count': cat_record['event_count']
            })
        
        for category, events in category_events.items():
            events.sort(key=lambda x: x['count'], reverse=True)
            total = sum(e['count'] for e in events)
            
            insights[category] = {
                'total_events': total,
                'unique_types': len(events),
                'top_events': events[:3]
            }
        
        return insights

    def print_analysis_summary(self, summary):
        """Print analysis summary"""
        print(f"\n✅ Analysis Complete!")
        print(f"📊 Category Distribution:")
        
        for category, count in summary['top_categories']:
            pct = (count / summary['total_events_processed']) * 100
            types = summary['category_type_counts'][category]
            print(f"   • {category}: {count:,} events ({pct:.1f}%) from {types} event types")
        
        print("\n🔍 Top Events by Category:")
        for category, insights in summary['category_insights'].items():
            top_events = ", ".join([f"{e['event_type']} ({e['count']})" for e in insights['top_events']])
            print(f"   • {category}: {top_events}")

    def close_connection(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("🔐 Database connection closed")

def main():
    """Main function to run analysis"""
    print("🔍 E-commerce Event Categorization")
    print("📌 Strict Categories: Browsing, Consideration, Conversion, Removal")
    print("=" * 60)
    
    analyzer = DynamicEcommerceEventAnalyzer()
    try:
        analyzer.run_analysis()
    except KeyboardInterrupt:
        print("\n⚠️ Analysis interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    finally:
        analyzer.close_connection()

if __name__ == "__main__":
    main()