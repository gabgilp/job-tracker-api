#!/bin/bash

# Start PostgreSQL service (via the start_postgresql.sh script)
./start_postgresql.sh

# Run FastAPI using Uvicorn
uvicorn tracker.main:app --reload
