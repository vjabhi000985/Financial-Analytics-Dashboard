from fastapi import FastAPI
from app.routes import charts

app = FastAPI(title="Financial Analytics API")

# Register the routes from charts.py
app.include_router(charts.router)