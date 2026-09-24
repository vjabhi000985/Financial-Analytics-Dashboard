# Financial Analytics Dashboard

A high-performance, real-time financial data processing and visualization pipeline. This project ingests historical market data, processes it using Pandas, caches heavy calculations with Redis, and serves interactive charts via a FastAPI + Plotly Dash frontend.

## 🚀 Tech Stack

* **Backend Engine:** [FastAPI](https://fastapi.tiangolo.com/)
* **Data Lake:** [MongoDB](https://www.mongodb.com/)
* **Caching Layer:** [Redis](https://redis.io/)
* **Analytics & Processing:** [Pandas](https://pandas.pydata.org/)
* **Visualization & Frontend:** [Plotly Dash](https://dash.plotly.com/)
* **Containerization:** [Docker & Docker Compose](https://www.docker.com/)

## 📂 Project Structure

```text
financial-analytics-dashboard/
├── docker-compose.yml       # Orchestrates the API, MongoDB, and Redis containers
├── Dockerfile               # FastAPI environment build instructions
├── requirements.txt         # Python dependencies
├── scripts/
│   └── seed_data.py         # Script to generate sample historical prices
└── app/
    ├── __init__.py
    ├── main.py              # Application entry point & Dash mount
    ├── database.py          # MongoDB and Redis dependency injection
    ├── dashboard.py         # Plotly Dash frontend UI
    └── routes/
        ├── __init__.py
        └── charts.py        # REST API endpoints and Pandas processing

## 🛠️ Local Setup & Installation
### Prerequisites: Ensure you have Docker and Docker Compose installed on your machine.

1. Clone the repository and navigate to the directory:

```
git clone <your-repo-url>
cd financial-analytics-dashboard
```

2. Build and start the Docker containers:

```
docker-compose up -d --build
This spins up MongoDB on port 27017, Redis on port 6379, and the FastAPI/Dash app on port 8000.
```

3. Generate sample data:
Run the seeding script inside the active API container to populate MongoDB with 90 days of simulated market data (BTC and AAPL).

```
docker exec -it analytics_api python scripts/seed_data.py
```

## 🌐 Usage & Endpoints
Once the stack is running and the database is seeded, access the application at the following local URLs:

### Interactive Dashboard: http://localhost:8000/dashboard/

### Raw JSON API Endpoint: http://localhost:8000/api/chart/BTC

### API Documentation (Swagger): http://localhost:8000/docs

(Note: The dashboard URL requires the trailing slash for correct routing).

## 🛑 Stopping the Application
- To shut down the containers while preserving your database data:
```
docker-compose down
```

- To shut down the containers and completely wipe the MongoDB database:
```
docker-compose down -v
```

<FollowUp label="Need help pushing to GitHub?" query="Walk me through the exact git commands to initialize this folder, commit the files, and upload them to a new GitHub repository."/>