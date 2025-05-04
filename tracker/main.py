from fastapi import FastAPI
from tracker.routers.application import router as application_router
from tracker.database import database
from contextlib import asynccontextmanager
import subprocess


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    print("Connected to the database")
    yield
    await database.disconnect()
    print("Disconnected from the database")
    subprocess.run(["sudo", "systemctl", "stop", "postgresql"])

app = FastAPI(lifespan=lifespan)
app.include_router(application_router, prefix="/api")

