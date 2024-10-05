import redis

def producer():
    client = redis.StrictRedis(host='localhost', port=6379, db=0)
    while True:
        message = input("Enter a message for the queue: ")
        client.rpush('my_queue', message)
        print(f"Queued: {message}")

if __name__ == '__main__':
    producer()