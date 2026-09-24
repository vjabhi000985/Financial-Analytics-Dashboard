import os
import random
from datetime import datetime, timedelta
from pymongo import MongoClient

# Connect to the local MongoDB exposed by Docker on port 27017
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["market_db"]
collection = db["prices"]

def generate_data(symbol, start_price, volatility, days=90):
    data = []
    current_price = start_price
    base_date = datetime.utcnow() - timedelta(days=days)
    
    for i in range(days):
        # Add random daily price movement
        change = current_price * random.uniform(-volatility, volatility)
        current_price += change
        
        data.append({
            "symbol": symbol,
            "date": (base_date + timedelta(days=i)).strftime("%Y-%m-%d"),
            "price": round(current_price, 2)
        })
    return data

if __name__ == "__main__":
    print("Clearing old data...")
    collection.delete_many({})
    
    print("Generating mock data...")
    btc_data = generate_data("BTC", 60000.0, 0.04)
    aapl_data = generate_data("AAPL", 175.0, 0.02)
    
    print("Inserting into MongoDB...")
    collection.insert_many(btc_data + aapl_data)
    
    print(f"Success! Inserted {collection.count_documents({})} records.")