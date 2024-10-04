# Redis with PostgreSQL and Python

This project demonstrates how to integrate **Redis** and **PostgreSQL** in a Python application. Redis is used to cache user data, reducing the load on PostgreSQL and improving the speed of data retrieval.

## Key Features

- **PostgreSQL Integration**: User data is stored in a PostgreSQL database.
- **Redis Caching**: Caches user data to reduce the number of database queries.
- **Cache Expiry**: Cached data expires after a set time (e.g., 60 seconds) to ensure freshness.
- **Dockerized Setup**: The project uses Docker to set up PostgreSQL and Redis containers easily.

## Prerequisites

- **Python 3.x**
- **Docker**
- **pip** (for Python package management)

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/7roubb/Redis-With-Python.git
   cd Redis-With-Python
Install dependencies: Use pip to install the required Python packages:
    pip install redis psycopg2-binary --break-system-packages
    
Set up PostgreSQL and Redis containers using Docker:

   
     DB_NAME="demo"
     DB_USER="admin"
     DB_PASSWORD="pass12312"
     DB_PORT=5434
     DB_HOST="localhost"

# Start PostgreSQL container
    
      docker run --name postgres-container -e POSTGRES_DB=$DB_NAME -e POSTGRES_USER=$DB_USER -e POSTGRES_PASSWORD=$DB_PASSWORD -p $DB_PORT:5432 -d postgres

# Start Redis container
    REDIS_CONTAINER_NAME="redis-cache"
    REDIS_PORT=6381
    REDIS_PASSWORD="pass123"

    docker run --name $REDIS_CONTAINER_NAME -p $REDIS_PORT:6379 -d redis redis-server --requirepass $REDIS_PASSWORD
Run the Python script: After setting up the environment, execute the Python script to fetch and cache user data:


      python main.py
