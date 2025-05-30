# Data Engineering Challenge for E-commerce Platform

![Image](https://github.com/user-attachments/assets/be8d1bbd-8f09-4e03-a018-e2d400e2ae40)

## Project Overview
This repository contains a comprehensive implementation of data engineering tasks for an e-commerce platform, focusing on performance optimization, user behavior analysis, and AI-driven segmentation.

## Project Structure
```
├── README.md
├── e-commerce_platform.sql    # Database initialization file
├── Coding_Challenge_Summary.pdf  # One-page technical summary
├── Task 1/
│   ├── Task1.md
│   ├── generate_sample.py
│   └── analysis.py
├── Task 2/
│   ├── Task2.md
│   └── Task2.ipynb
├── Task 3/
│   ├── Task3.md
│   ├── behavioral_segmentation.py
│   ├── check_results.py
│   └── requirements.txt
└── Task 4/
    ├── Task4.md
    ├── .env
    ├── analysis_results_20250530_225757.json
    ├── event_type_categorizer.py
    └── requirements.txt
```

## Tasks Implementation

### Task 1: Data Exploration & SQL Optimization
- Query optimization for e-commerce analytics
- Performance benchmarking
- Documentation: [Task 1/Task1.md](Task%201/Task1.md)

### Task 2: Cohort Analysis
- User retention analysis
- Visualization of cohort patterns
- Documentation: [Task 2/Task2.md](Task%202/Task2.md)

### Task 3: Behavioral Segmentation
- Elasticsearch integration
- AI-driven user segmentation
- Documentation: [Task 3/Task3.md](Task%203/Task3.md)

### Task 4: Event Analysis with LLM Integration
- E-commerce event tracking analysis
- Gemini API integration for advanced insights
- Customer behavior pattern recognition
- Documentation: [Task 4/Task4.md](Task%204/Task4.md)

## Technical Stack
- PostgreSQL
- Python (pandas, numpy, scikit-learn)
- Elasticsearch
- Visualization tools (matplotlib, seaborn)
- AI APIs (OpenAI/Hugging Face)

## Getting Started
1. Clone the repository
2. Set up PostgreSQL database using `e-commerce_platform.sql`
3. Install required Python packages
4. Follow individual task documentation

## Documentation
Each task has detailed documentation in its respective folder:
- Task 1: Database optimization
- Task 2: User retention analysis
- Task 3: AI segmentation

### Technical Summary
The `Coding_Challenge_Summary.pdf` provides a one-page overview of:
- Key optimizations achieved (64.34% improvement in WAU queries)
- Retention analysis insights
- User segmentation strategy using AI
- Technical implementation details

## Database Setup
The project includes `e-commerce_platform.sql` which contains:
- Table structures
- Sample data
- Initial indexes
- Required database configurations
