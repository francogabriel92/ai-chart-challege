from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.db import init_db
from app.database.seed import seed_sales_from_csv
from app.api import charts
from app.middleware.timeout import add_timeout_middleware
from app.utils.config import get_settings


# Initialize FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    # Seed the database with initial data
    seed_sales_from_csv()
    yield


app = FastAPI(lifespan=lifespan)

# Per simplicity, we allow all origins, methods, and headers.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_timeout_middleware(app)

# Routes
app.include_router(charts.router, prefix="/charts", tags=["CHARTS"])


# Health check endpoint
@app.get("/health")
def read_health():
    return {"status": "healthy"}
