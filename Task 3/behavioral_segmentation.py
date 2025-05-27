from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import numpy as np
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def connect_to_elasticsearch():
    """Create Elasticsearch connection"""
    try:
        print("Attempting to connect to Elasticsearch...")
        es = Elasticsearch(
            "https://localhost:9200",
            basic_auth=("Your_username", "Your_Pass"),  # Updated with your password and username
            verify_certs=False,
            request_timeout=30,
            retry_on_timeout=True,
            max_retries=3,
            ssl_show_warn=False
        )
        
        if not es.ping():
            print("\nElasticsearch connection test failed. Please check:")
            raise Exception("Connection test failed")
            
        print("Successfully connected to Elasticsearch!")
        return es
        
    except Exception as e:
        print(f"\nConnection Error: {str(e)}")
        print("\nTroubleshooting steps:")
        raise

def extract_search_history(es):
    """Extract user search history from Elasticsearch"""
    query = {
        "size": 1000,  # Adjust based on your needs
        "_source": ["user_id", "search_query", "clicked_product_ids"]
    }
    
    response = es.search(index="user_sessions", body=query)
    return response['hits']['hits']

def get_embeddings(search_queries):
    """Convert search queries to embeddings using Sentence-Transformers"""
    model = SentenceTransformer('all-MiniLM-L6-v2')  # Free and lightweight model
    embeddings = model.encode(search_queries)
    return embeddings

def cluster_users(embeddings, n_clusters=5):
    """Cluster users based on their search embeddings"""
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(embeddings)
    return clusters

def assign_segment_labels(cluster_id):
    """Map cluster IDs to meaningful segment labels"""
    segment_mapping = {
        0: "tech_enthusiast",
        1: "budget_conscious",
        2: "fashion_oriented",
        3: "luxury_seeker",
        4: "home_improvement"
    }
    return segment_mapping.get(cluster_id, "undefined")

def update_elasticsearch_with_segments(es, user_segments):
    """Store user segments back to Elasticsearch"""
    for user_id, segment in user_segments.items():
        doc = {
            "segment": segment,
            "updated_at": datetime.now().isoformat()
        }
        es.update(
            index="user_segments",
            id=user_id,
            body={"doc": doc, "doc_as_upsert": True}
        )

def create_required_indices(es):
    """Create required Elasticsearch indices if they don't exist"""
    try:
        # Define mappings for user_sessions index
        user_sessions_mapping = {
            "mappings": {
                "properties": {
                    "user_id": {"type": "keyword"},
                    "search_query": {"type": "text"},
                    "clicked_product_ids": {"type": "keyword"}
                }
            }
        }
        
        # Define mappings for user_segments index
        user_segments_mapping = {
            "mappings": {
                "properties": {
                    "segment": {"type": "keyword"},
                    "updated_at": {"type": "date"}
                }
            }
        }
        
        # Create indices if they don't exist
        if not es.indices.exists(index="user_sessions"):
            es.indices.create(index="user_sessions", body=user_sessions_mapping)
            print("Created user_sessions index")
            
            # Add sample data for testing
            sample_data = [
                {
                    "user_id": f"user_{i}",
                    "search_query": query,
                    "clicked_product_ids": [f"product_{j}" for j in range(2)]
                }
                for i, query in enumerate([
                    "gaming laptop",
                    "budget smartphone",
                    "designer shoes",
                    "luxury watch",
                    "home renovation"
                ])
            ]
            
            # Bulk index sample data
            for doc in sample_data:
                es.index(index="user_sessions", document=doc)
            print("Added sample data to user_sessions")
            
        if not es.indices.exists(index="user_segments"):
            es.indices.create(index="user_segments", body=user_segments_mapping)
            print("Created user_segments index")
            
    except Exception as e:
        print(f"Error creating indices: {str(e)}")
        raise

def main():
    # Connect to Elasticsearch
    es = connect_to_elasticsearch()
    
    # Create required indices and sample data
    create_required_indices(es)
    
    # Extract search history
    search_data = extract_search_history(es)
    
    # Prepare data for processing
    user_ids = []
    search_queries = []
    
    for hit in search_data:
        user_ids.append(hit['_source']['user_id'])
        search_queries.append(hit['_source']['search_query'])
    
    # Generate embeddings
    embeddings = get_embeddings(search_queries)
    
    # Perform clustering
    clusters = cluster_users(embeddings)
    
    # Create user segments dictionary
    user_segments = {}
    for user_id, cluster_id in zip(user_ids, clusters):
        segment = assign_segment_labels(cluster_id)
        user_segments[user_id] = segment
    
    # Update Elasticsearch with segments
    update_elasticsearch_with_segments(es, user_segments)
    
    print(f"Successfully processed {len(user_ids)} users")

if __name__ == "__main__":
    main()
