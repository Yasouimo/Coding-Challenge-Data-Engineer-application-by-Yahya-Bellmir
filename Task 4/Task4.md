# Task 4: E-commerce Event Analysis with Database Integration

## 1. Event Data Overview

### Raw Event Distribution
| Event Type          | Count | Percentage |
|---------------------|-------|------------|
| view_item          | 3,043 | 31.05% |
| view_item_list     | 2,514 | 25.65% |
| add_to_cart        | 1,579 | 16.11% |
| view_cart          | 762  | 7.78%  |
| remove_from_cart   | 515  | 5.26%  |
| add_to_wishlist    | 489  | 4.99%  |
| begin_checkout     | 360  | 3.67%  |
| add_payment_info   | 279  | 2.85%  |
| add_shipping_info  | 266  | 2.71%  |
| purchase           | 193  | 1.97%  |

Total events analyzed: 9,800

Note: Event types sourced from GA4 E-commerce event specifications.

## 2. Implementation Overview

This project implements an e-commerce event analysis system that connects to a PostgreSQL database to fetch and analyze user behavior events. The system categorizes events into meaningful behavioral groups and provides detailed analytics.

### Technologies Used
- Python for data processing
- PostgreSQL for data storage
- Pandas for data manipulation
- JSON for results storage

### Integration with AI Services (TinyLlama via Ollama)
For improved control and local inference, we will be using the TinyLlama model running on Ollama. This allows for fast, local LLM-powered event categorization.

#### How TinyLlama Categorization Works
- The system sends each event type to the TinyLlama model via the Ollama API.
- A strict prompt is used to ensure the model returns only one of four categories: Browsing, Consideration, Conversion, or Removal.
- If the model's response is unclear, a keyword-based fallback categorization is applied for reliability.


### Data Fetching
```sql
SELECT 
    event_type,
    COUNT(*) as event_count,
    COUNT(DISTINCT user_id) as unique_users
FROM events 
GROUP BY event_type
ORDER BY event_count DESC;
```

#### Categorization Prompt Used
```text
Categorize this e-commerce event into exactly one of these four categories:
- Browsing: Viewing products or pages without clear intent to purchase
- Consideration: Showing interest in products but not yet committing
- Conversion: Actions that directly lead to or represent a purchase
- Removal: Removing items from cart or wishlist

Event: "{event_type}"
Respond with only the category name (Browsing, Consideration, Conversion, or Removal) and nothing else.
```

#### Example Categorization Output
```
🔍 Analyzing 10 unique event types...
  [1/10] Analyzing: view_item
    → Browsing
  [2/10] Analyzing: view_item_list
    → Browsing
  [3/10] Analyzing: add_to_cart
    → Consideration
  [4/10] Analyzing: view_cart
    → Browsing
  [5/10] Analyzing: remove_from_cart
    → Removal
  [6/10] Analyzing: add_to_wishlist
    → Consideration
  [7/10] Analyzing: begin_checkout
    → Conversion
  [8/10] Analyzing: add_payment_info
    → Conversion
  [9/10] Analyzing: add_shipping_info
    → Conversion
  [10/10] Analyzing: purchase
    → Conversion
```

#### Improved Categorization with Keywords
To further enhance accuracy, we use keyword-based rules as a fallback. For example:
- "view", "browse", "search" → Browsing
- "add", "wishlist", "cart" → Consideration
- "purchase", "checkout", "payment" → Conversion
- "remove", "delete" → Removal


## 4. Core Components

### Database Integration
- PostgreSQL connection handling
- Event data retrieval using SQL aggregation
- Error handling and connection management

### Event Categorization System
The system categorizes events into four main behavioral groups:

1. **Browsing Events**
   - Keywords: 'view', 'browse', 'search'
   - Captures product discovery behavior
   - Examples: view_item, view_item_list, view_cart

2. **Consideration Events**
   - Keywords: 'cart', 'wishlist'
   - Tracks shopping cart interactions
   - Examples: add_to_cart, remove_from_cart, add_to_wishlist

3. **Conversion Events**
   - Keywords: 'purchase', 'checkout', 'payment', 'shipping'
   - Monitors purchase completion
   - Examples: begin_checkout, add_payment_info, add_shipping_info, purchase

4. **Removal Events**
   - Keywords: 'remove', 'delete'
   - Tracks removal actions
   - Examples: remove_from_cart


## 4. Analysis Results

Based on our latest analysis using TinyLlama (timestamp: 2025-06-01), the system identified the following distribution:

### Event Distribution
- Total Events Analyzed: 10
- Category Breakdown:
  - Browsing: 30% (3 events)
  - Consideration: 20% (2 events)
  - Conversion: 40% (4 events)
  - Removal: 10% (1 event)

### Detailed Event Categorization

1. **Browsing Category (30%)**
   - view_item
   - view_item_list
   - view_cart

2. **Consideration Category (20%)**
   - add_to_cart
   - add_to_wishlist

3. **Conversion Category (40%)**
   - begin_checkout
   - add_payment_info
   - add_shipping_info
   - purchase

<<<<<<< HEAD
4. **Removal Category (10%)**
   - remove_from_cart

## 5. Technical Implementation

### Data Fetching
```sql
SELECT 
    event_type,
    COUNT(*) as event_count,
    COUNT(DISTINCT user_id) as unique_users
FROM events 
GROUP BY event_type
ORDER BY event_count DESC;
```
=======
>>>>>>> dc0b9fa55c8edc4fa2edafd928856a17761e850c

### Analysis Storage
Results are stored in JSON format containing:
- Analysis timestamp
- Event summaries
- Category distribution
- Detailed insights per category

## 6. Key Insights

### Behavioral Patterns
1. **Discovery Phase**
   - High event concentration in browsing actions
   - Multiple viewing events before cart addition
   - Important for initial user engagement

2. **Shopping Intent**
   - Consideration events show intent but not commitment
   - Clear progression from cart addition to purchase

3. **Purchase Behavior**
   - Strong presence of payment and checkout events
   - Complete purchase journey tracking

4. **Removal Actions**
   - Removal events are less frequent but important for understanding friction points

## 7. System Benefits

1. **Real-time Analysis**
   - Direct database connectivity
   - Immediate event processing
   - Up-to-date insights

2. **Scalable Architecture**
   - SQL-based aggregation
   - Efficient data handling
   - Robust error management

3. **Actionable Insights**
   - Clear event categorization
   - Percentage-based analysis
   - JSON-formatted results

## Conclusion

The implementation successfully provides a clear picture of user behavior patterns in the e-commerce platform. By leveraging TinyLlama via Ollama for event categorization, combined with keyword-based rules, the system offers robust, explainable, and scalable analytics for understanding the user journey and improving conversion rates.

### Future Enhancements
1. Advanced pattern recognition
2. Time-based analysis
3. User segment identification
4. Custom event categorization rules
