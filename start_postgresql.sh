#!/bin/bash

# Load the .env file and export the variables
export $(cat .env | xargs)

# Determine which database name to use based on ENV_STATE
if [ "$ENV_STATE" == "dev" ]; then
    SELECTED_DB_NAME=$DB_NAME
elif [ "$ENV_STATE" == "test" ]; then
    SELECTED_DB_NAME=$TEST_DB_NAME
else
    echo "Invalid ENV_STATE: $ENV_STATE. Must be 'dev' or 'test'."
    exit 1
fi

echo "Using database: $SELECTED_DB_NAME"

# Check if PostgreSQL is running
if ! pg_isready -q -h $DB_HOST -p $DB_PORT; then
    echo "PostgreSQL is not running. Starting the PostgreSQL server..."
    sudo service postgresql start
else
    echo "PostgreSQL is already running."
fi

# Check if the database exists
DB_EXISTS=$(psql -U $DB_USER -h $DB_HOST -tAc "SELECT 1 FROM pg_database WHERE datname='$SELECTED_DB_NAME'")

if [ -z "$DB_EXISTS" ]; then
    echo "Creating database $SELECTED_DB_NAME..."
    psql -U $DB_USER -h $DB_HOST -c "CREATE DATABASE $SELECTED_DB_NAME;"
else
    echo "Database $SELECTED_DB_NAME already exists."
fi
