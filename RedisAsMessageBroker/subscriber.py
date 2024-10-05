import redis 

def subsriber():
    client = redis.StrictRedis(
        host = 'localhost', 
        port = 6382,
        db=0
    )

    p = client.pubsub()
    p.subscribe('my_channel')

    while True:
        message = p.get_message()
        if message:
            print(f"Received: {message['data'].decode('utf-8')}")

if __name__ == '__main__':
    subsriber()