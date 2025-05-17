# filepath: c:\Users\Shwetha\OneDrive\Desktop\my full stack pro\db\__init__.py
import pymysql
from flask import abort


def get_db_connection():
    conn = pymysql.connect(
        host='database-1.cobgmm6euz11.us-east-1.rds.amazonaws.com',  # Replace with your RDS endpoint
        user='jyothi',      # Replace with your RDS username
        password='Janu123456789',  # Replace with your RDS password
        database='blogs',  # Replace with your RDS database name
        port=3306,
        cursorclass=pymysql.cursors.DictCursor  # Use DictCursor to return rows as dictionaries
                         # Default MySQL port
    )
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post