# Task 2: Cohort Analysis & User Retention

## Overview
This task focuses on analyzing user retention patterns through cohort analysis, using Python and SQL to process and visualize e-commerce platform data.

## Implementation Details

### 1. Data Extraction
- Connected to PostgreSQL database
- Extracted user activity data using SQL
- Implemented cohort grouping by signup month

### 2. Cohort Analysis
- Created cohort matrix for 8-week retention tracking
- Calculated retention rates
- Handled edge cases and data validation

### 3. Visualizations
- **Heatmap**: Shows retention patterns across cohorts
- **Line Graph**: Displays retention trends over time
- Used Seaborn and Matplotlib for clear visual representation

### 4. Key Metrics
- Initial cohort sizes
- Weekly retention rates
- Retention decay analysis
- Week-over-week changes

## Technical Stack
- Python (pandas, numpy)
- PostgreSQL
- Visualization libraries (seaborn, matplotlib)
- Data processing tools (psycopg2)

## Results
The analysis provides insights into:
- User retention patterns
- Cohort performance comparison
- Weekly engagement trends
- Long-term user behavior

## Key Findings & Interpretation

### Churn Analysis
- **Early Churn Pattern**: The data shows significant user drop-off in the second month (weeks 4-8)
- **Initial Engagement**: Strong user activity in weeks 0-3 suggests effective onboarding
- **Critical Period**: The transition between weeks 3-4 appears to be a crucial retention point

### Limitations of Analysis
- Two-month data window may not be sufficient for long-term patterns
- Need to investigate:
  - User experience during weeks 3-4
  - Product-market fit indicators
  - Specific features or issues triggering churn
  - Seasonal effects on user behavior

### Recommendations
1. **Short-term Actions**:
   - Conduct user surveys at week 3
   - Analyze user journey pain points
   - Review product features used before churning

2. **Further Analysis Needed**:
   - Extend cohort tracking beyond 8 weeks
   - Segment users by engagement level
   - Correlate churn with specific product interactions
   - Compare with industry benchmarks

### Data Quality Notes
- Limited to two months of data (April-May 2025)
- Need longer timeframe for seasonal patterns
- Consider adding qualitative user feedback

## Files
- `Task2.ipynb`: Jupyter notebook with implementation
- `Task2.md`: Documentation and explanation

## Usage
1. Configure database connection
2. Run cells in sequence in Task2.ipynb
3. Review generated visualizations and metrics