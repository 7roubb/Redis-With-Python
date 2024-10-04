import redis
import psycopg2
import time

def connect_to_postgresql():
    return psycopg2.connect(
        host="localhost",  
        port=5434,
        database="demo",      
        user="admin",    
        password="pass12312"
    )

def fetch_user_from_db(user_id):
    time.sleep(3) # here to simulate a real case 
    conn = connect_to_postgresql()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, age FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if user:
        return {"id": user[0], "name": user[1], "age": user[2]}
    else:
        return None

cache = redis.StrictRedis(
    host='localhost',
    port=6381,  
    db=0,
    password='pass123' 
)

def get_user_data(user_id):
    cached_user = cache.get(f"user:{user_id}")
    
    if cached_user:
        print("Fetching from cache...")
        return eval(cached_user.decode('utf-8')) 
    
    user_data = fetch_user_from_db(user_id)
    
    if user_data:
        cache.setex(f"user:{user_id}", 60, str(user_data))  # Cache user data for 60 seconds
        print("Fetching from database and caching...")
    
    return user_data

user_id = 1

user = get_user_data(user_id)
print(user)

user = get_user_data(user_id)
print(user)

time.sleep(60)

user = get_user_data(user_id)
print(user)
