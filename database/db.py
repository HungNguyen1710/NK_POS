"""
=========================================================
 NK POS V1.0
 Database Layer
 SQLite Manager
=========================================================
"""

import sqlite3
from pathlib import Path
from contextlib import contextmanager
from typing import Any, Dict, List, Optional


class DBManager:
    """
    Database Manager
    """

    BASE_DIR = Path(__file__).resolve().parent
    DB_FILE = BASE_DIR / "nk.db"

    # =====================================================
    # INITIALIZE DATABASE
    # =====================================================
    @classmethod
    def initialize(cls):
        """
        Tạo database và các bảng nếu chưa tồn tại
        """

        cls.BASE_DIR.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(cls.DB_FILE) as conn:

            cursor = conn.cursor()

            # =================================================
            # PRODUCTS
            # =================================================

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS products(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                product_code TEXT UNIQUE NOT NULL,

                name TEXT NOT NULL,

                price REAL DEFAULT 0,

                stock INTEGER DEFAULT 0

            )
            """)

            # =================================================
            # INVOICES
            # =================================================

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS invoices(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                invoice_no TEXT NOT NULL,

                invoice_date TEXT,

                total REAL DEFAULT 0

            )
            """)

            # =================================================
            # INVOICE DETAILS
            # =================================================

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS invoice_details(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                invoice_id INTEGER NOT NULL,

                product_code TEXT,

                product_name TEXT,

                qty INTEGER DEFAULT 0,

                price REAL DEFAULT 0,

                amount REAL DEFAULT 0,

                FOREIGN KEY(invoice_id)
                    REFERENCES invoices(id)

            )
            """)

            conn.commit()

    # =====================================================
    # CONNECTION
    # =====================================================

    @classmethod
    @contextmanager
    def connection(cls):

        conn = sqlite3.connect(cls.DB_FILE)

        conn.row_factory = sqlite3.Row

        try:

            yield conn

            conn.commit()

        except sqlite3.Error:

            conn.rollback()

            raise

        finally:

            conn.close()
        # =====================================================
    # EXECUTE
    # =====================================================

    @classmethod
    def execute(cls, sql: str, params: tuple = ()) -> int:
        """
        INSERT / UPDATE / DELETE

        Trả về lastrowid
        """

        with cls.connection() as conn:

            cursor = conn.cursor()

            cursor.execute(sql, params)

            return cursor.lastrowid

    # =====================================================
    # EXECUTE MANY
    # =====================================================

    @classmethod
    def execute_many(cls, sql: str, data: list):
        """
        INSERT nhiều dòng
        """

        with cls.connection() as conn:

            cursor = conn.cursor()

            cursor.executemany(sql, data)

    # =====================================================
    # FETCH ONE
    # =====================================================

    @classmethod
    def fetch_one(
        cls,
        sql: str,
        params: tuple = ()
    ) -> Optional[Dict[str, Any]]:

        with cls.connection() as conn:

            cursor = conn.cursor()

            cursor.execute(sql, params)

            row = cursor.fetchone()

            if row is None:
                return None

            return dict(row)

    # =====================================================
    # FETCH ALL
    # =====================================================

    @classmethod
    def fetch_all(
        cls,
        sql: str,
        params: tuple = ()
    ) -> List[Dict[str, Any]]:

        with cls.connection() as conn:

            cursor = conn.cursor()

            cursor.execute(sql, params)

            rows = cursor.fetchall()

            return [dict(row) for row in rows]

    # =====================================================
    # TRANSACTION
    # =====================================================

    @classmethod
    def transaction(
        cls,
        queries: list
    ):
        """
        Transaction

        queries = [
            (sql, params),
            (sql, params),
            ...
        ]
        """

        with cls.connection() as conn:

            cursor = conn.cursor()

            for sql, params in queries:

                cursor.execute(sql, params)

    # =====================================================
    # CHECK DATABASE
    # =====================================================

    @classmethod
    def database_exists(cls) -> bool:

        return cls.DB_FILE.exists()

    # =====================================================
    # GET DATABASE PATH
    # =====================================================

    @classmethod
    def get_database_path(cls) -> str:

        return str(cls.DB_FILE)

    # =====================================================
    # CLOSE
    # =====================================================

    @classmethod
    def close(cls):
        """
        Placeholder để tương thích các module.
        SQLite sử dụng context manager nên không cần đóng.
        """
        pass
        # =====================================================
    # PRODUCT HELPERS
    # =====================================================

    @classmethod
    def get_product_count(cls) -> int:
        """
        Tổng số sản phẩm
        """

        row = cls.fetch_one(
            "SELECT COUNT(*) AS total FROM products"
        )

        return row["total"] if row else 0

    @classmethod
    def get_invoice_count(cls) -> int:
        """
        Tổng số hóa đơn
        """

        row = cls.fetch_one(
            "SELECT COUNT(*) AS total FROM invoices"
        )

        return row["total"] if row else 0

    @classmethod
    def clear_table(cls, table_name: str):
        """
        Xóa toàn bộ dữ liệu của một bảng.
        Chỉ dùng khi test.
        """

        allow_tables = (
            "products",
            "invoices",
            "invoice_details",
        )

        if table_name not in allow_tables:
            raise ValueError("Tên bảng không hợp lệ.")

        sql = f"DELETE FROM {table_name}"

        cls.execute(sql)


# =====================================================
# INITIALIZE DATABASE
# =====================================================

DBManager.initialize()


# =====================================================
# TEST DATABASE
# =====================================================

if __name__ == "__main__":

    print("=" * 50)
    print(" NK POS V1.0")
    print("=" * 50)

    print("Database :", DBManager.get_database_path())
    print("Exists   :", DBManager.database_exists())
    print("Products :", DBManager.get_product_count())
    print("Invoices :", DBManager.get_invoice_count())

    print("=" * 50)
    print("Database Ready.")
    print("=" * 50)
    
