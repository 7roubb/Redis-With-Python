import redis

def consumer():
    client = redis.StrictRedis(host='localhost', port=6379, db=0)
    print("Waiting for messages from the queue...")
    while True:
        message = client.blpop('my_queue', timeout=0)
        print(f"Consumed: {message[1].decode('utf-8')}")

if __name__ == '__main__':
    consumer()