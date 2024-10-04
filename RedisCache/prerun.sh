#Pre Run the Code run this script to install all dependencies and create the database and redis cache 

pip install redis --break-system-packages
pip install redis psycopg2-binary --break-system-packages


DB_NAME="demo"
DB_USER="admin"
DB_PASSWORD="pass12312"
DB_PORT=5434
DB_HOST="localhost"

docker run --name postgres-container -e POSTGRES_DB=$DB_NAME -e POSTGRES_USER=$DB_USER -e POSTGRES_PASSWORD=$DB_PASSWORD -p $DB_PORT:5432 -d postgres

echo "Waiting for PostgreSQL to start..."
sleep 5 

SQL_COMMAND="
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    age INT
);

INSERT INTO users (name, age) VALUES
('John Doe', 30),
('Jane Smith', 25),
('Alice Johnson', 35)
ON CONFLICT DO NOTHING;  -- This avoids duplicate entries if rerun
"
docker exec -i postgres-container psql -U $DB_USER -d $DB_NAME -c "$SQL_COMMAND"

if [ $? -eq 0 ]; then
  echo "Database and table created successfully, and data inserted."
else
  echo "An error occurred while setting up the database."
fi

REDIS_CONTAINER_NAME="redis-cache"
REDIS_PORT=6381
REDIS_PASSWORD="pass123"  

docker run --name $REDIS_CONTAINER_NAME -p $REDIS_PORT:6379 -d redis redis-server --requirepass $REDIS_PASSWORD

echo "Waiting for Redis to start..."
sleep 5  

if docker ps | grep -q "$REDIS_CONTAINER_NAME"; then
  echo "Redis cache created successfully and is running."
else
  echo "An error occurred while setting up the Redis cache."
  exit 1
fi
