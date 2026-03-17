import hashlib
from .db import get_connection

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(email, phone, password):
    conn = get_connection()
    cursor = conn.cursor()

    password_hash = hash_password(password)

    try:
        cursor.execute(
            "INSERT INTO users (email, phone, password_hash) VALUES (?, ?, ?)",
            (email, phone, password_hash)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_user(identifier, password):
    conn = get_connection()
    cursor = conn.cursor()

    password_hash = hash_password(password)

    cursor.execute(
        """
        SELECT id, is_setup_complete 
        FROM users 
        WHERE (email=? OR phone=?) AND password_hash=?
        """,
        (identifier, identifier, password_hash)
    )

    user = cursor.fetchone()
    conn.close()
    return user

def reset_password(identifier, new_password):
    conn = get_connection()
    cursor = conn.cursor()

    new_hash = hash_password(new_password)

    cursor.execute(
        """
        UPDATE users 
        SET password_hash=? 
        WHERE email=? OR phone=?
        """,
        (new_hash, identifier, identifier)
    )

    conn.commit()
    conn.close()