import sqlite3
import os


DATABASE_FOLDER = "database"
DATABASE_FILE = os.path.join(DATABASE_FOLDER, "quynhanh.db")


def get_connection():
    """
    Tạo kết nối SQLite
    """
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """
    Khởi tạo database và bảng
    """

    if not os.path.exists(DATABASE_FOLDER):
        os.makedirs(DATABASE_FOLDER)

    conn = get_connection()
    cursor = conn.cursor()


    # Bảng sản phẩm
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        product_code TEXT UNIQUE NOT NULL,

        name TEXT NOT NULL,

        price REAL DEFAULT 0,

        stock INTEGER DEFAULT 0,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)


    conn.commit()
    conn.close()



def execute(query, params=()):
    """
    Chạy lệnh INSERT / UPDATE / DELETE
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(query, params)

    conn.commit()

    last_id = cursor.lastrowid

    conn.close()

    return last_id



def fetch_all(query, params=()):
    """
    Lấy nhiều dòng dữ liệu
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(query, params)

    rows = cursor.fetchall()

    conn.close()

    return rows



def fetch_one(query, params=()):
    """
    Lấy một dòng dữ liệu
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(query, params)

    row = cursor.fetchone()

    conn.close()

    return row