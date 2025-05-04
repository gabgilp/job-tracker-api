#!/bin/bash

# Load the .env file and export the variables
export $(cat .env | xargs)

# Check if PostgreSQL is running
if ! pg_isready -q -h $DB_HOST -p $DB_PORT; then
    echo "PostgreSQL is not running. Starting the PostgreSQL server..."
    sudo service postgresql start
else
    echo "PostgreSQL is already running."
fi

# Check if the database exists
DB_EXISTS=$(psql -U $DB_USER -h $DB_HOST -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'")

if [ -z "$DB_EXISTS" ]; then
    echo "Creating database $DB_NAME..."
    psql -U $DB_USER -h $DB_HOST -c "CREATE DATABASE $DB_NAME;"
else
    echo "Database $DB_NAME already exists."
fi
