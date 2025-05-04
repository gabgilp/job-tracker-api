from fastapi import FastAPI
from tracker.routers.application import router as application_router
import tracker.database as db
from contextlib import asynccontextmanager
import subprocess
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await db.database.connect()
        print("Connected to the database")

        await db.init_db()
        print("Database initialized")
        
        yield
    finally:
        await db.database.disconnect()
        print("Disconnected from the database")

        if os.getenv("SHUTDOWN_POSTGRES") == "1":
            try:
                subprocess.run(["sudo", "systemctl", "stop", "postgresql"])
                print("PostgreSQL stopped")
            except Exception as e:
                print(f"Error stopping PostgreSQL: {e}")

app = FastAPI(lifespan=lifespan)
app.include_router(application_router, prefix="/api")

