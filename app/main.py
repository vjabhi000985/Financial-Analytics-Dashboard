from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.routes import charts
from app.dashboard import dash_mount

app = FastAPI(title="Financial Analytics API")

# 1. Include REST API Routes
app.include_router(charts.router)

# 2. Mount Dash on /dashboard
app.mount("/dashboard", dash_mount)

# 3. Optional: redirect root URL to /dashboard/
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/dashboard/")