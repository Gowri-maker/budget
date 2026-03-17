import pandas as pd
from utils.db import get_connection


def get_user_expenses(user_id):
    conn = get_connection()

    query = """
    SELECT expense_date, product_name, category, amount
    FROM user_expenses
    WHERE user_id = ?
    """

    df = pd.read_sql(query, conn, params=(user_id,))
    conn.close()

    return df


def insert_expense(user_id, expense_date, product_name, category, amount):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO user_expenses (user_id, expense_date, product_name, category, amount)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, expense_date, product_name, category, amount)
    )

    conn.commit()
    conn.close()