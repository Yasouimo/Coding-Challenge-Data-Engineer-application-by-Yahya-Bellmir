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
            'dbname': 'e-commerce_platform', # Replace with your DB name if different
            'user': 'postgres',             # Replace with your DB user if different
            'password': 'Your_Pass', # Replace with your actual DB password
            'host': 'localhost'             # Replace with your DB host if different
        }
        self.connection = None
        
        # Mistral AI Configuration
        self.mistral_api_url = "https://api.mistral.ai/v1/chat/completions"
        self.mistral_api_key = os.getenv("MISTRAL_API_KEY")
        if not self.mistral_api_key:
            print("❌ MISTRAL_API_KEY not found in environment variables. Please set it in your .env file.")
            # Analysis will be impacted if key is missing
        self.mistral_model_name = "mistral-small-latest" # Recommended for balance

        self.valid_categories = {
            "Browse", "Consideration", "Conversion", "Removal"
        }
        # To track specific failure types or non-LLM assigned categories
        self.error_categories = { 
            "Uncategorized", # LLM response not in valid_categories
            "API_Timeout_Error", 
            "API_Request_Error", 
            "API_JSON_Decode_Error", 
            "API_Response_Format_Error",
            "API_Unknown_Error"
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
        """Let Mistral AI analyze the event and suggest a category name with an improved prompt"""
        
        if not self.mistral_api_key:
            print(f"⚠️ Mistral API key not configured. Skipping API call for event '{event_type}'. Will be marked as API_Request_Error.")
            return "API_Request_Error"

        # Enhanced Prompt:
        prompt = f"""Your task is to categorize an e-commerce event into ONLY ONE of the following four specific categories.
It is crucial that you use the exact category names provided: "Browse", "Consideration", "Conversion", or "Removal".

Detailed Category Definitions and Examples:

1.  **Browse**:
    * Description: User is viewing lists of products, product categories, or general site pages. They are exploring without showing deep interest in a *specific* item or having an immediate intent to purchase.
    * Examples: 'view_homepage', 'search_for_product', 'view_category_page', 'view_item_list', 'scroll_product_listings', 'filter_search_results', 'view_promotions_page'.

2.  **Consideration**:
    * Description: User is actively showing interest in *specific* products or is reviewing their selected items before final commitment. This stage is about evaluation before initiating the active checkout process.
    * Examples: 'view_item' (viewing specific product details), 'add_to_wishlist', 'compare_products', 'read_reviews', 'view_cart' (reviewing items selected before checkout), 'view_wishlist_items', 'product_quick_view'.

3.  **Conversion**:
    * Description: User is performing actions that are part of the *active checkout process*, or actions that directly lead to or represent a purchase or a key business goal. This signifies a clear intent to acquire.
    * Examples: 'add_to_cart' (initiating a collection for purchase), 'begin_checkout', 'proceed_to_checkout', 'add_payment_info', 'add_shipping_info', 'purchase', 'complete_order', 'apply_discount_code_in_checkout'.

4.  **Removal**:
    * Description: User is actively removing items they previously showed interest in from potential purchase paths.
    * Examples: 'remove_from_cart', 'remove_from_wishlist', 'clear_cart', 'empty_wishlist'.

E-commerce Event Type to Categorize: "{event_type}"

Instructions for your response:
1.  Analyze the "{event_type}" based on the definitions and examples above.
2.  Choose the single most appropriate category: "Browse", "Consideration", "Conversion", or "Removal".
3.  Your entire response MUST BE ONLY the chosen category name. For example, if you decide the category is Browse, your response is exactly:
Browse

Do not add any other words, explanations, numbers, or punctuation. Just the single category name.
Category:"""

        payload = {
            "model": self.mistral_model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0, # Keep at 0.0 for maximum consistency
            "max_tokens": 20,   # Ample for a single category name, slightly more buffer
            "stream": False
        }
        
        headers = {
            "Authorization": f"Bearer {self.mistral_api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        try:
            response = requests.post(self.mistral_api_url, headers=headers, json=payload, timeout=45) # Increased timeout slightly
            response.raise_for_status()  # Raises HTTPError for bad responses (4XX or 5XX)
            api_response_json = response.json()

            if 'choices' not in api_response_json or not api_response_json['choices'] or \
               'message' not in api_response_json['choices'][0] or \
               'content' not in api_response_json['choices'][0]['message']:
                print(f"❌ Mistral API Error: Unexpected response structure for event '{event_type}'. Response: {json.dumps(api_response_json)}")
                return "API_Response_Format_Error"

            raw_response = api_response_json['choices'][0]['message']['content'].strip()
            # Robust cleaning based on prompt instructions
            raw_response = raw_response.replace("Category:", "").replace("*", "").strip() 
            clean_response = raw_response.title() # Standardize to "Browse", "Consideration", etc.
            
            if clean_response in self.valid_categories:
                return clean_response
            else:
                # Log the unexpected response from the LLM
                print(f"⚠️ LLM response '{raw_response}' (cleaned: '{clean_response}') is not a valid category for event '{event_type}'. Marked as Uncategorized.")
                return "Uncategorized"
                
        except requests.exceptions.Timeout:
            print(f"❌ Mistral API Timeout for event '{event_type}'.")
            return "API_Timeout_Error"
        except requests.exceptions.HTTPError as http_err:
            # More specific error logging for HTTP errors
            error_content = "No content"
            try:
                error_content = response.json() # Try to get JSON error details from Mistral
            except json.JSONDecodeError:
                error_content = response.text[:500] # Fallback to text if not JSON
            print(f"❌ Mistral API HTTP Error for event '{event_type}': {http_err}. Response: {error_content}")
            return "API_Request_Error" # Or a more specific error code like API_HTTP_Error
        except requests.exceptions.RequestException as e:
            print(f"❌ Mistral API Request Error for event '{event_type}': {e}")
            return "API_Request_Error"
        except json.JSONDecodeError:
            # This can happen if the response is not valid JSON (e.g. HTML error page after an HTTPError was not caught by raise_for_status somehow)
            print(f"❌ Mistral API Error: Failed to decode JSON response for event '{event_type}'. Response text: {response.text[:200]}...") 
            return "API_JSON_Decode_Error"
        except Exception as e: # Catch any other unexpected errors during API interaction
            print(f"❌ Unexpected error during Mistral API call for event '{event_type}': {e}")
            return "API_Unknown_Error"

    def run_analysis(self):
        """Main workflow: Strict categorization with four classes using Mistral AI"""
        print("🚀 Starting Strict Event Categorization Analysis with Mistral AI")
        print(f"   🤖 Using Model: {self.mistral_model_name}")
        print(f"   🎯 Target Categories: {', '.join(sorted(list(self.valid_categories)))}")
        
        if not self.mistral_api_key:
             print("🚨 CRITICAL ERROR: Mistral API key is missing. Analysis cannot proceed effectively.")
             # Allow to proceed to see DB connection/fetch, but API calls will fail.
             # return None # Uncomment to stop analysis if API key is absolutely mandatory upfront

        if not self.connect_db():
            return None
        
        event_data = self.fetch_event_data()
        if event_data is None or event_data.empty:
            print("ℹ️ No event data to analyze.")
            self.close_connection() # Close DB if no data
            return None
        
        print(f"\n🔍 Analyzing {len(event_data)} unique event types...")
        
        categorizations = []
        
        for idx, row in event_data.iterrows():
            event_type = row['event_type']
            event_count = row['event_count']
            
            print(f"   [{idx+1}/{len(event_data)}] Analyzing: {event_type}")
            
            suggested_category = self.analyze_event_pattern(event_type)
            
            categorizations.append({
                "event_type": event_type,
                "event_count": int(event_count),
                "category": suggested_category, 
                "discovery_order": idx + 1
            })
            
            print(f"     → {suggested_category}")
            # time.sleep(0.05) # Small delay if needed, but Mistral API usually handles concurrent requests well.
                           # For very large number of unique events, consider batching or more robust rate limit handling.
        
        total_events_sum = sum(rec['event_count'] for rec in categorizations) # Use categorized data for sum
        category_totals = Counter()
        category_type_counts = Counter()
        
        for cat_record in categorizations:
            category = cat_record['category']
            category_totals[category] += cat_record['event_count']
            category_type_counts[category] += 1
        
        analysis_summary = {
            "total_unique_event_types": len(event_data),
            "total_events_processed": int(total_events_sum),
            "category_distribution": dict(category_totals), 
            "category_type_counts": dict(category_type_counts),
            "top_categories_by_event_volume": category_totals.most_common(),
            "category_insights": self.generate_category_insights(categorizations)
        }
        
        results = {
            "analysis_metadata": {
                "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "target_categories": sorted(list(self.valid_categories)),
                "error_and_unhandled_categories_tracked": sorted(list(self.error_categories)),
                "model_used": self.mistral_model_name
            },
            "analysis_summary": analysis_summary,
            "detailed_categorizations": sorted(categorizations, key=lambda x: x['event_count'], reverse=True)
        }
        
        output_filename = "mistral_strict_event_categorization.json"
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Results saved to '{output_filename}'")
        except IOError as e:
            print(f"❌ Error saving results to '{output_filename}': {e}")
        
        self.print_analysis_summary(analysis_summary)
        
        return results

    def generate_category_insights(self, categorizations):
        """Generate insights about category distribution (includes Uncategorized/Error states)"""
        insights = {}
        category_events_map = defaultdict(list) # Renamed for clarity
        
        for cat_record in categorizations:
            category_events_map[cat_record['category']].append({
                'event_type': cat_record['event_type'],
                'count': cat_record['event_count']
            })
        
        for category, events_list in category_events_map.items():
            events_list.sort(key=lambda x: x['count'], reverse=True)
            total_event_count_for_category = sum(e['count'] for e in events_list)
            
            insights[category] = {
                'total_events_in_category': total_event_count_for_category,
                'unique_event_types_in_category': len(events_list),
                'top_event_types_in_category': events_list[:3] # Show top 3 event types for this category
            }
        return insights

    def print_analysis_summary(self, summary):
        """Print analysis summary, including Uncategorized/Error counts"""
        print(f"\n✅ Analysis Complete!")
        total_processed = summary['total_events_processed']
        print(f"📊 Category Distribution (Total Events Processed: {total_processed:,}):")
        
        # Sort keys: valid categories first, then error categories, then any others alphabetically
        all_category_keys_sorted = sorted(
            summary['category_distribution'].keys(), 
            key=lambda k: (
                0 if k in self.valid_categories else (1 if k in self.error_categories else 2), 
                k 
            )
        )

        for category_key in all_category_keys_sorted:
            count = summary['category_distribution'][category_key]
            types = summary['category_type_counts'][category_key]
            pct = (count / total_processed) * 100 if total_processed > 0 else 0
            
            prefix_char = "•" # Default bullet
            if category_key in self.error_categories:
                prefix_char = "⚠️" # Warning for error/unhandled
            
            print(f"   {prefix_char} {category_key}: {count:,} events ({pct:.1f}%) from {types} event type(s)")

        print("\n🔍 Top Event Types by Category:")
        # Use the same sorting for insights display
        sorted_insights_keys = sorted(
            summary['category_insights'].keys(), 
             key=lambda k: (
                0 if k in self.valid_categories else (1 if k in self.error_categories else 2), 
                k
            )
        )

        for category_key in sorted_insights_keys:
            insight_data = summary['category_insights'][category_key]
            if not insight_data['top_event_types_in_category']: 
                continue # Skip if no events (should not happen if category_distribution has it)

            top_events_str = ", ".join([f"{e['event_type']} ({e['count']:,})" for e in insight_data['top_event_types_in_category']])
            
            prefix_char = "•"
            if category_key in self.error_categories:
                 prefix_char = "⚠️"
            
            print(f"   {prefix_char} {category_key} (Total: {insight_data['total_events_in_category']:,}, Types: {insight_data['unique_event_types_in_category']}): {top_events_str}")

    def close_connection(self):
        """Close database connection"""
        if self.connection:
            try:
                self.connection.close()
                print("🔐 Database connection closed")
            except Exception as e:
                print(f"❌ Error closing database connection: {e}")
        else:
            print("ℹ️ No active database connection to close.")


def main():
    """Main function to run analysis"""
    print(" SSSSSS      IIIIIIIIII   GGGGGGGGGGGG       MMMMMMMM               MMMMMMMM         AAA               IIIIIIIIII")    
    print("SS::::::SS     I::::::::I  GGG::::::::::::G       M:::::::M             M:::::::M        A:::A              I::::::::I")  
    print("S:::::SS:::::SS  I::::::::I GG:::::::::::::::G       M::::::::M           M::::::::M       A:::::A             I::::::::I")  
    print("S:::::S S::::S  II::::::IIG:::::GGGGGGGG::::G       M:::::::::M         M:::::::::M      A:::::::A            II::::::II")  
    print("S:::::S         I::::I G:::::G    GGGGG::::G       M::::::::::M       M::::::::::M     A:::::::::A           I::::I  ")  
    print("S:::::S         I::::I G:::::G            G       M:::::::::::M     M:::::::::::M    A:::::A:::::A          I::::I  ")  
    print("S::::SSSS    I::::I G:::::G            G       M:::::::M::::M  M::::M:::::::M   A:::::A A:::::A         I::::I  ")  
    print("SS::::::::::::S I::::I G:::::G    GGGGGGGGG       M::::::M M::::M M::::M M::::::M  A:::::A   A:::::A        I::::I  ")  
    print("SSS::::::::SS I::::I G:::::G    G::::::::G       M::::::M  M::::M::::M  M::::::M A:::::A     A:::::A       I::::I  ")  
    print(" SSSSOURAV SSS I::::I G:::::G    GGGGG::::G       M::::::M   M:::::::M   M::::::MA:::::::::::::::::A      I::::I  ")  
    print("      S:::::S I::::I G:::::G            G       M::::::M    M:::::M    M::::::MA:::::::A:::::::A     I::::I  ")  
    print("      S:::::S I::::I G:::::G            G       M::::::M     MMMMM     M::::::MA:::::::A A:::::::A    I::::I  ")  
    print("S S:::::S:::::SII::::::IIG:::::GGGGGGGG::::G       M::::::M               M::::::MA:::::A   A:::::A   II::::::II")  
    print("S:::::SS:::::S I::::::::I GG:::::::::::::::G       M::::::M               M::::::MA:::::A     A:::::A  I::::::::I")  
    print(" SS:::::::::::S  I::::::::I  GGG::::::::::::G       M::::::M               M::::::MA:::::A       A:::::A I::::::::I")  
    print("   SSSSSSSSSS    IIIIIIIIII   GGGGGGGGGGGG       MMMMMMMM               MMMMMMMAAAAAAA         AAAAAAAIIIIIIIIII")  
    print("\n=========================================================================================================")
    print("        🤖 E-COMMERCE EVENT CATEGORIZATION ENGINE (POWERED BY MISTRAL AI) 🚀")
    print("=========================================================================================================")
    print(f"Initialization Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Analysis Objective: Strictly categorize e-commerce events into:")
    print("    -> Browse, Consideration, Conversion, Removal")
    print("Reporting: Failures in categorization (API issues, unexpected LLM output) will be distinctly reported.")
    print("---------------------------------------------------------------------------------------------------------")

    analyzer = DynamicEcommerceEventAnalyzer()
    try:
        analyzer.run_analysis()
    except KeyboardInterrupt:
        print("\n⚠️ Analysis interrupted by user.")
    except Exception as e:
        print(f"\n❌ An unexpected critical error occurred in the main execution block: {e}")
        import traceback
        traceback.print_exc() # Print full traceback for critical errors
    finally:
        print("---------------------------------------------------------------------------------------------------------")
        print(f"Analysis Concluded: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        analyzer.close_connection()
        print("=========================================================================================================")


if __name__ == "__main__":
    main()