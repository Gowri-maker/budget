import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "users.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            phone TEXT UNIQUE,
            password_hash TEXT,
            is_setup_complete INTEGER DEFAULT 0
        )
    """)

    # MONTHLY FINANCIALS TABLE (NEW)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_monthly_financials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            month INTEGER,
            year INTEGER,
            income REAL,
            budget REAL,
            expected_expenditure REAL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # CATEGORY TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            category_name TEXT,
            priority_level INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # DAILY EXPENSE TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            expense_date TEXT,
            product_name TEXT,
            category TEXT,
            amount REAL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()