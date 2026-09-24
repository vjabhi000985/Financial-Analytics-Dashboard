import os
from pymongo import MongoClient
import redis

# Fetch environment variables with fallbacks for local testing
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

# Global client instances (reused across requests)
mongo_client = MongoClient(MONGO_URI)
redis_client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

def get_db():
    """Dependency to get the MongoDB database instance."""
    db = mongo_client["market_db"]
    try:
        yield db
    finally:
        # Pymongo handles connection pooling automatically, 
        # so we just yield the db reference.
        pass

def get_cache():
    """Dependency to get the Redis cache instance."""
    try:
        yield redis_client
    finally:
        pass