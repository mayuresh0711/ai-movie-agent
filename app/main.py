import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.routes import user_routes, recommend_routes
from app.ai_agent import ask_ai
from app.scheduler import send_recommendations_to_all_users

# Create a scheduler instance
scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup, add the job and start the scheduler
    print("Application startup...")
    # Schedule the job to run every 5 minutes for easy testing
    scheduler.add_job(send_recommendations_to_all_users, 'interval', minutes=5)
    scheduler.start()
    yield
    # On shutdown, stop the scheduler
    print("Application shutdown...")
    scheduler.shutdown()

app = FastAPI(
    title="AI Movie Recommendation Agent",
    lifespan=lifespan
)

# Include the routers
app.include_router(user_routes.router)
app.include_router(recommend_routes.router)

@app.get("/", tags=["Default"])
def home():
    return {"message": "Movie Recommendation Agent is running 🚀"}

@app.get("/ask-ai", tags=["AI"])
def ask_ai_endpoint(prompt: str):
    response = ask_ai(prompt)
    return {"prompt": prompt, "response": response}