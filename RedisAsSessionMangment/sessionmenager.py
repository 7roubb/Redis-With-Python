import redis 
import psycopg2
from datetime import datetime, timedelta
import json

def connect_to_postgresql():
    return psycopg2.connect(
        host="localhost",  
        port=5434,
        database="demo",      
        user="admin",    
        password="pass12312"
    )

cache = redis.StrictRedis(
    host='localhost',
    port=6381,  #here u can change the port as u want 
    db=0,
    password='pass123'
)

def create_session(userId,sessionData,expire_in=3600):
    sessionm_id = f"session:_{userId}:{datetime.now().timestamp()}"
    expires_at = datetime.now() + timedelta(seconds=expire_in)

    conn = connect_to_postgresql()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sessions (session_id, user_id, data, expires_at)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (session_id) DO UPDATE
        SET data = %s, expires_at = %s;
    """, (session_id, user_id, json.dumps(session_data), expires_at, json.dumps(session_data), expires_at))
    
    conn.commit()
    cursor.close()
    conn.close()

    cache.setex(session_id, expires_in, json.dumps(session_data))
    
    return session_id


def get_session(sessionId):
    cached_session = cache.get(sessionId)
    if cached_session :
        print("Fetching Session From Cache")
        return json.loads(cached_session)
    
    conn = connect_to_postgresql()
    cursor = conn.cursor()
    cursor.execute("SELECT data FROM sessions WHERE session_id = %s", (sessionId,))
    session = cursor.fetchone()

    cursor.close()
    conn.close()

    if session:
        cache.setex(sessionId, 3600, session[0])  
        print("Fetching Session From Database and Cache")
        return json.loads(session[0])
    else:
        return None


def update_session(sessionId,sessionData):
    conn = connect_to_postgresql()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE sessions
        SET data = %s, expires_at = %s
        WHERE session_id = %s;
    """, (json.dumps(sessionData), datetime.now() + timedelta(seconds=3600), sessionId))
    
    conn.commit()
    cursor.close()
    conn.close()

    cache.setex(sessionId, 3600, json.dumps(sessionData))
    print("Updating Session in Cache")


def delete_session(sessionId):
    conn = connect_to_postgresql()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sessions WHERE session_id = %s;", (sessionId,))
    
    conn.commit()
    cursor.close()
    conn.close()

    cache.delete(sessionId)
    print("Deleting Session from Cache")


if __name__ == "__main__":
    user_id = 1
    session_data = {"username": "john_doe", "email": "john@example.com"}
    
    session_id = create_session(user_id, session_data)
    print(f"Session created: {session_id}")
    retrieved_session = get_session(session_id)
    print("Retrieved session:", retrieved_session)
    
    updated_data = {"username": "john_doe_updated", "email": "john_updated@example.com"}
    update_session(session_id, updated_data)
    
    updated_session = get_session(session_id)
    print("Updated session:", updated_session)
    
    delete_session(session_id)