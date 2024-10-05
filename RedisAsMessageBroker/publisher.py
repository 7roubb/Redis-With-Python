import redis 

def publisher():
    client = redis.StrictRedis(
        host = 'localhost', 
        port = 6382,
        db=0
    )
    while True : 
        message = input("Enter the message ")
        client.publish("my_channel", message)
        print(f"Published: {message}")

if __name__ == "__main__":
    publisher()


