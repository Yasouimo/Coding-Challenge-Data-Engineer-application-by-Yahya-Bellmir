import psycopg2
import json
import requests
import os
from typing import Dict, List
import time

class EventCategorizer:
    def __init__(self, db_config: Dict, api_key: str):
        self.db_config = db_config
        self.api_key = api_key
        # Updated to Gemini 1.5 Pro endpoint
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={self.api_key}"
        self.headers = {
            'Content-Type': 'application/json'
        }
        
    def connect_db(self):
        """Create database connection"""
        return psycopg2.connect(**self.db_config)

    def get_current_events(self) -> List[str]:
        """Get current event types from database"""
        conn = self.connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT DISTINCT event_type FROM events")
            return [row[0] for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()

    def call_llm_api(self, prompt: str) -> str:
        """Call LLM API to get event categorization"""
        payload = {
            "contents": {
                "role": "user",
                "parts": [{"text": prompt}]
            },
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024,
            }
        }

        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 401:
                print("❌ Invalid API key. Please check your credentials.")
                return None
            elif response.status_code == 404:
                print("❌ API endpoint not found. Trying fallback...")
                return self.get_fallback_categorization()
                
            response.raise_for_status()
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API request failed: {str(e)}")
            return self.get_fallback_categorization()
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return None

    def get_fallback_categorization(self) -> Dict:
        """Provide fallback categorization when API fails"""
        return {
            "current_events": {
                "viewed": {
                    "category": "product_interaction",
                    "description": "User viewed a product page",
                    "journey_stage": "discovery"
                },
                "add-to-cart": {
                    "category": "cart_interaction",
                    "description": "User added item to shopping cart",
                    "journey_stage": "consideration"
                },
                "purchased": {
                    "category": "transaction",
                    "description": "User completed purchase",
                    "journey_stage": "conversion"
                }
            },
            "suggested_events": {
                "search": {
                    "category": "discovery",
                    "description": "User performed product search",
                    "journey_stage": "discovery"
                },
                "wishlist_add": {
                    "category": "engagement",
                    "description": "User added item to wishlist",
                    "journey_stage": "consideration"
                }
            }
        }

    def categorize_events(self):
        """Get event categorization from LLM"""
        current_events = self.get_current_events()
        
        prompt = f"""
        As an e-commerce analytics expert, analyze these event types:
        {', '.join(current_events)}

        1. Suggest additional relevant event types for better tracking
        2. Categorize all events (current and new) into meaningful groups
        3. Explain what each event represents
        4. Indicate the customer journey stage for each event

        Format response as JSON:
        {{
            "current_events": {{
                "event_type": {{
                    "category": "category_name",
                    "description": "what this event means",
                    "journey_stage": "stage name"
                }}
            }},
            "suggested_events": {{
                "new_event_type": {{
                    "category": "category_name",
                    "description": "what this event means",
                    "journey_stage": "stage name"
                }}
            }}
        }}
        """

        print("🤖 Calling LLM API for event analysis...")
        response = self.call_llm_api(prompt)

        if response:
            try:
                # Check if response is already a dictionary (fallback case)
                if isinstance(response, dict):
                    return response
                    
                # Otherwise parse the API response
                clean_response = response.strip()
                if clean_response.startswith('```json'):
                    clean_response = clean_response[7:]
                if clean_response.endswith('```'):
                    clean_response = clean_response[:-3]

                categorization = json.loads(clean_response.strip())
                return categorization
            except json.JSONDecodeError as e:
                print(f"❌ Error parsing LLM response: {e}")
                return self.get_fallback_categorization()
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                return self.get_fallback_categorization()
        
        return self.get_fallback_categorization()

    def display_results(self, categorization: Dict):
        """Display categorization results"""
        if not categorization:
            return

        print("\n📊 Current Event Analysis:")
        print("-" * 50)
        for event, data in categorization.get('current_events', {}).items():
            print(f"\n🔹 {event}")
            print(f"   Category: {data['category']}")
            print(f"   Stage: {data['journey_stage']}")
            print(f"   Description: {data['description']}")

        print("\n🆕 Suggested New Events:")
        print("-" * 50)
        for event, data in categorization.get('suggested_events', {}).items():
            print(f"\n🔸 {event}")
            print(f"   Category: {data['category']}")
            print(f"   Stage: {data['journey_stage']}")
            print(f"   Description: {data['description']}")

if __name__ == "__main__":
    db_config = {
        'host': 'localhost',
        'database': 'e-commerce_platform',
        'user': 'postgres',
        'password': '789456123'
    }

    api_key = os.getenv('LLM_API_KEY')
    if not api_key:
        print("❌ Please set LLM_API_KEY environment variable")
        exit(1)

    categorizer = EventCategorizer(db_config, api_key)
    results = categorizer.categorize_events()
    categorizer.display_results(results)