import json
from app.db.db_config import get_connection
from app.models import UserCreate

def create_new_user(user: UserCreate):
    """
    Saves a new user to the database.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Convert preferences dict to a JSON string to store in the database
        preferences_json = json.dumps(user.preferences)

        query = "INSERT INTO users (name, email, preferences) VALUES (%s, %s, %s)"
        cursor.execute(query, (user.name, user.email, preferences_json))
        
        conn.commit()
        user_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        return {"user_id": user_id, "email": user.email, "message": "User created successfully"}
    
    except Exception as e:
        # Handle errors, like a duplicate email
        return {"error": str(e)}
    


def get_user_by_id(user_id: int):
    """
    Fetches a single user from the database by their ID.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True) # dictionary=True returns rows as dicts

        query = "SELECT id, name, email, preferences FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()

        if user and user.get('preferences'):
            # Convert the JSON string from DB back to a Python dict
            user['preferences'] = json.loads(user['preferences'])
        
        return user

    except Exception as e:
        return {"error": str(e)}
    

def get_all_users():
    """
    Fetches all users from the database.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT id, name, email FROM users"
        cursor.execute(query)
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return users
    except Exception as e:
        print(f"Error fetching all users: {e}")
        return []