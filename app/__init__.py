import os
from .models.database import get_db_connection

def init_db():
    """初始化資料庫：讀取 schema.sql 並執行建表"""
    conn = get_db_connection()
    try:
        # Schema SQL path relative to the project root
        schema_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'schema.sql')
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        conn.close()