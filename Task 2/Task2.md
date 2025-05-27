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

## Files
- `Task2.ipynb`: Jupyter notebook with implementation
- `Task2.md`: Documentation and explanation
- Generated visualizations in 'visualizations' directory

## Usage
1. Configure database connection
2. Run cells in sequence in Task2.ipynb
3. Review generated visualizations and metrics