import json
import pandas as pd
import plotly.express as px
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db, get_cache

router = APIRouter()

@router.get("/api/chart/{symbol}")
def get_asset_chart(symbol: str, db = Depends(get_db), cache = Depends(get_cache)):
    symbol = symbol.upper()
    cache_key = f"chart_data_{symbol}"
    
    # 1. Check Redis Cache
    cached_chart = cache.get(cache_key)
    if cached_chart:
        return {"source": "redis_cache", "chart": json.loads(cached_chart)}
        
    # 2. Fetch from MongoDB
    collection = db["prices"]
    cursor = collection.find({"symbol": symbol}, {"_id": 0, "date": 1, "price": 1})
    data = list(cursor)
    
    if not data:
        raise HTTPException(status_code=404, detail=f"No data found for symbol {symbol}")
        
    # 3. Process with Pandas
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    df['moving_avg'] = df['price'].rolling(window=7).mean()
    
    # 4. Generate Plotly Chart
    fig = px.line(
        df, 
        x='date', 
        y=['price', 'moving_avg'], 
        title=f"{symbol} Price & 7-Day Moving Average"
    )
    chart_json = fig.to_json()
    
    # 5. Cache in Redis
    cache.setex(cache_key, 300, chart_json)
    
    return {"source": "mongodb_pandas", "chart": json.loads(chart_json)}