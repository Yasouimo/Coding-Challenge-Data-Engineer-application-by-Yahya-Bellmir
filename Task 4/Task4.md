# Task 4: E-commerce Event Analysis with Database Integration

## 1. Event Analysis Overview

We analyzed a dataset containing 9,800 e-commerce events that track user behavior across the shopping journey. Here's the distribution of events:

We got the events from this website : 

https://magefan.com/blog/ecommerce-events-to-track-in-ga4?srsltid=AfmBOorOpulfrGQ1gmZPtd0LjLdLWmvQOqusoJCYQwP1z-jHZOFFTaGF

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
- Gemini API for advanced analysis
- Pandas for data manipulation

### Key Components
- EcommerceAnalyzer class for data processing
- Database connectivity
- Event categorization system
- Gemini API integration
- Results storage in JSON format

## 3. LLM-Based Categorization

Using the Gemini API, we categorized events into behavioral segments and analyzed patterns:

### Customer Segments Identified

1. **Browsers (60%)**
   - Primary events: `view_item` (3,043), `view_item_list` (2,514)
   - High view-item rate
   - Low add-to-cart conversion
   - Primarily browsing behavior

2. **Cart Abandoners (20%)**
   - Primary events: `add_to_cart` (1,579), `remove_from_cart` (515)
   - Drop-off before `begin_checkout` (360)
   - High cart abandonment rate (87.77%)
   - Significant revenue opportunity

3. **Completers (10%)**
   - Event sequence: `begin_checkout` → `add_payment_info` → `add_shipping_info` → `purchase`
   - Complete purchase journey (193 purchases)
   - Core revenue generators
   - Full funnel conversion

4. **View Cart Users (8%)**
   - Primary event: `view_cart` (762)
   - Multiple cart views without proceeding to `begin_checkout`
   - Hesitant behavior
   - Price-sensitive group

5. **Wishlist Users (5%)**
   - Primary event: `add_to_wishlist` (489)
   - Low `purchase` conversion rate
   - High wishlist-to-cart ratio
   - Potential for targeted marketing

### Gemini API Prompt
The following structured prompt was used to generate the LLM analysis:

```text
Analyze this e-commerce behavioral data and provide a comprehensive report:

DATA:
- Total Events: 9,800
- Conversion Funnel: View Item (3,043) → Add to Cart (1,579) → Begin Checkout (360) → Purchase (193)
- Supporting Events: View Cart (762), Wishlist (489), Remove from Cart (515)
- Conversion Rates: View→Cart (51.9%), Cart→Checkout (22.8%), Checkout→Purchase (53.6%)

PROVIDE ANALYSIS ON:

1. CUSTOMER SEGMENTATION (classify into behavioral segments):
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
```

### Event Categorization Strategy
The events were systematically categorized into three main behavioral phases:

1. **Discovery Phase**
   - Highest event concentration (40%)
   - Multiple viewing events before cart addition
   - Important for initial user engagement

2. **Shopping Intent**
   - Equal distribution between consideration and conversion (30% each)
   - Clear progression from cart addition to purchase
   - Balanced conversion funnel

3. **Purchase Behavior**
   - Strong presence of payment and checkout events
   - Complete purchase journey tracking
   - Clear conversion path identification

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

The implementation successfully provides a clear picture of user behavior patterns in the e-commerce platform. The system's ability to categorize and analyze events offers valuable insights for understanding user journey and improving conversion rates.

### Future Enhancements
1. Advanced pattern recognition
2. Time-based analysis
3. User segment identification
4. Custom event categorization rules
