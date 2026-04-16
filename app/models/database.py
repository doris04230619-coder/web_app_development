import sqlite3
import os

def get_db_connection():
    """
    建立並回傳與 SQLite 資料庫的連線。
    使用 sqlite3.Row 讓查詢結果可以用欄位名稱存取。
    """
    db_path = os.path.join('instance', 'database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
