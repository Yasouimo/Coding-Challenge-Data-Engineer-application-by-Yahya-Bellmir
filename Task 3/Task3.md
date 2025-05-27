# Task 3: Behavioral Segmentation with Elasticsearch & AI

## Project Overview
This project implements user behavioral segmentation by analyzing search patterns and using AI to cluster users into meaningful segments. The implementation uses Elasticsearch for data storage and retrieval, and Hugging Face's sentence-transformers for AI vector embeddings.

## About Elasticsearch
Elasticsearch is a distributed, RESTful search and analytics engine built on Apache Lucene. It's designed to handle large volumes of data with near real-time search capabilities. Perfect for this project's needs of storing and querying user behavior data, it provides powerful full-text search, structured search, analytics, and vector search capabilities. Download Elasticsearch from the official website: [Elasticsearch Download Page](https://www.elastic.co/downloads/elasticsearch). For Windows users, download the .zip file, extract it, and run `elasticsearch.bat` from the bin directory.

## Requirements

### Prerequisites
- Python 3.8+
- Elasticsearch 8.x running on localhost:9200
- Python packages listed in requirements.txt

### Installation Steps
1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Start Elasticsearch:
```bash
# Ensure Elasticsearch is running on localhost:9200
# Note the elastic user password from initial setup
```

## Implementation Details

### 1. Data Structure
The project uses two Elasticsearch indices:

#### User Sessions Index
```json
{
  "user_id": "user_0",
  "search_query": "gaming laptop",
  "clicked_product_ids": ["product_0", "product_1"]
}
```

#### User Segments Index
```json
{
  "user_id": "user_0",
  "segment": "tech_enthusiast",
  "updated_at": "2025-05-27T20:31:22.899686"
}
```

### 2. Technical Implementation
- **Vector Conversion**: Using Sentence-Transformers model 'all-MiniLM-L6-v2'
- **Clustering**: K-means algorithm with 5 clusters
- **Storage**: Elasticsearch with two custom indices

### 3. User Segments
Five distinct user segments identified:
- Tech Enthusiast
- Budget Conscious
- Fashion Oriented
- Luxury Seeker
- Home Improvement

## Results

### Sample Data Processing Results
```
=== User Sessions Data ===
User_0: "gaming laptop" -> tech_enthusiast
User_1: "budget smartphone" -> budget_conscious
User_2: "designer shoes" -> fashion_oriented
User_3: "luxury watch" -> luxury_seeker
User_4: "home renovation" -> home_improvement
```

### Performance Metrics
- Successfully processed: 5 users
- Elasticsearch indices created: 2
- Vector embedding dimension: 384 (MiniLM model)

## Running the Project

1. Update Elasticsearch credentials in `behavioral_segmentation.py`

2. Run the main segmentation script:
```bash
python behavioral_segmentation.py
```

3. View results:
```bash
python check_results.py
```

## Conclusion
This behavioral segmentation system demonstrates the power of combining modern search infrastructure (Elasticsearch) with AI capabilities (Hugging Face transformers) to understand user behavior at scale. By automatically categorizing users into meaningful segments based on their search patterns, the system enables:

- **Personalized User Experience**: Better product recommendations and search results based on user segments
- **Business Intelligence**: Deep insights into user interests and shopping patterns
- **Marketing Optimization**: Targeted campaigns for different user segments
- **Inventory Planning**: Better understanding of product demand across different user groups

The solution provides a foundation for data-driven decision making while being scalable and maintainable for production environments.