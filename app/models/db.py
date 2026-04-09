import sqlite3
import os

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
    'instance', 
    'database.db'
)

def get_db():
    """取得資料庫連線，如果 instance 目錄不存在則建立"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    # 將回傳結果設為可以像 dict 一樣讀取欄位名稱的 Row 物件
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化資料庫並載入 schema.sql 建表語法"""
    schema_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'database',
        'schema.sql'
    )
    db = get_db()
    with open(schema_path, mode='r', encoding='utf-8') as f:
        db.executescript(f.read())
    db.commit()
    db.close()
