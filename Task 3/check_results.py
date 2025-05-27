from elasticsearch import Elasticsearch

def check_elasticsearch_data():
    # Connect to Elasticsearch
    es = Elasticsearch(
        "https://localhost:9200",
        basic_auth=("Your_username", "Your_pass"),# Updated with your password and username
        verify_certs=False,
        ssl_show_warn=False
    )

    # 1. Check user_sessions data
    print("\n=== User Sessions Data ===")
    sessions = es.search(
        index="user_sessions",
        body={
            "size": 10,
            "_source": ["user_id", "search_query", "clicked_product_ids"]
        }
    )
    for hit in sessions['hits']['hits']:
        print(f"\nUser ID: {hit['_source']['user_id']}")
        print(f"Search Query: {hit['_source']['search_query']}")
        print(f"Clicked Products: {hit['_source']['clicked_product_ids']}")

    # 2. Check user segments
    print("\n=== User Segments Data ===")
    segments = es.search(
        index="user_segments",
        body={
            "size": 10,
            "_source": ["segment", "updated_at"]
        }
    )
    for hit in segments['hits']['hits']:
        print(f"\nUser ID: {hit['_id']}")
        print(f"Segment: {hit['_source']['segment']}")
        print(f"Updated At: {hit['_source']['updated_at']}")

if __name__ == "__main__":
    check_elasticsearch_data()
