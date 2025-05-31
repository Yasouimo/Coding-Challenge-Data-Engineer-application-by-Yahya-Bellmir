# Task 4: E-commerce Event Analysis with LLM Integration

## 1. Event Analysis Overview

We analyzed a dataset containing 9,800 e-commerce events that track user behavior across the shopping journey. Here's the distribution of events:

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

## 2. Implementation Details

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
   - Primary Events: view_item, view_item_list
   - Behavioral Indicator: Initial product discovery and browsing
   - User Intent: Research and exploration

2. **Consideration Phase**
   - Primary Events: add_to_cart, view_cart, add_to_wishlist, remove_from_cart
   - Behavioral Indicator: Active product evaluation
   - User Intent: Product comparison and decision-making

3. **Conversion Phase**
   - Primary Events: begin_checkout, add_shipping_info, add_payment_info, purchase
   - Behavioral Indicator: Purchase commitment
   - User Intent: Transaction completion

### Derived Event Categories
The analysis identified additional behavioral patterns:

1. **Hesitant Buyers**
   - Trigger: Multiple cart views before checkout
   - Business Value: Identifying price sensitivity
   - Optimization Target: Checkout confidence

2. **Research-Intensive Users**
   - Trigger: High view-to-action ratio
   - Business Value: Content effectiveness measurement
   - Optimization Target: Product information

3. **Quick Decision Makers**
   - Trigger: Rapid view-to-purchase journey
   - Business Value: Optimal user experience patterns
   - Optimization Target: Streamlined conversion

4. **Collection Builders**
   - Trigger: High wishlist-to-purchase ratio
   - Business Value: Long-term purchase intent
   - Optimization Target: Retention marketing

## 4. Key Metrics & Insights

### Funnel Analysis
1. Product Views: 3,043 (100%)
2. Cart Additions: 1,579 (51.89%)
3. Cart Views: 762 (48.26%)
4. Checkout Started: 360 (47.24%)
5. Purchase Complete: 193 (6.34% overall conversion)

### Critical Patterns
- Cart Abandonment Rate: 87.77%
- Checkout Abandonment: 46.39%
- View-to-Cart Conversion: 51.89%
- Wishlist Usage: 16.07%
- Cart Removal Rate: 32.62%

## 5. Generated Insights

The LLM analysis provided actionable insights for improvement:

### High-Priority Recommendations
1. Optimize checkout process (Expected lift: 15-20%)
2. Implement cart abandonment emails (Expected lift: 10-15%)
3. Improve product information display (Expected lift: 5-10%)
4. Enhance website UX/UI (Expected lift: 8-12%)
5. Target wishlist users with promotions (Expected lift: 3-5%)

### Bottleneck Analysis
1. Add to Cart → Checkout (77.2% drop)
2. Checkout → Purchase (46.4% drop)
3. View Item → Add to Cart (48.1% drop)

## 6. Results Storage

All analysis results are stored in JSON format with timestamp-based naming:
- Event distribution data
- Funnel analysis metrics
- Pattern identification
- Derived events
- LLM analysis results

## Conclusion

The implementation successfully leveraged LLM technology to provide deeper insights into e-commerce behavior patterns. The combination of traditional analytics with AI-driven analysis offers actionable recommendations for improving conversion rates and user experience.