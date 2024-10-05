
CONTAINER_NAME="redis-broker"

REDIS_PORT=6382

if ! command -v docker &> /dev/null
then
    echo "Docker is not installed. Please install Docker first."
    exit
fi

if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
    echo "Redis container is already running."
else
    if [ "$(docker ps -aq -f status=exited -f name=$CONTAINER_NAME)" ]; then
        echo "Starting the existing Redis container..."
        docker start $CONTAINER_NAME
    else
        echo "Pulling the Redis image and creating the container..."
        docker run --name $CONTAINER_NAME -p $REDIS_PORT:6379 -d redis
    fi
fi

echo "Current running Redis containers:"
docker ps | grep redis

echo "To view Redis container logs, use the following command:"
echo "docker logs $CONTAINER_NAME"

echo "To enter Redis CLI, use the following command:"
echo "docker exec -it $CONTAINER_NAME redis-cli"