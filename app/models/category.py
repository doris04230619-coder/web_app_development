import sqlite3
from app.models.database import get_db_connection

class Category:
    """提供 categories 表格的 CRUD 操作"""

    @staticmethod
    def create(data):
        """
        新增一筆分類記錄
        data 應包含: user_id, name
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO categories (user_id, name) VALUES (?, ?)",
                (data['user_id'], data['name'])
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error creating category: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all(user_id=None):
        """取得所有記錄 (可依照 user_id 過濾)"""
        conn = get_db_connection()
        try:
            if user_id:
                return conn.execute("SELECT * FROM categories WHERE user_id = ?", (user_id,)).fetchall()
            return conn.execute("SELECT * FROM categories").fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching categories: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(id):
        """取得單筆記錄"""
        conn = get_db_connection()
        try:
            return conn.execute("SELECT * FROM categories WHERE id = ?", (id,)).fetchone()
        except sqlite3.Error as e:
            print(f"Error fetching category by id: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def update(id, data):
        """
        更新記錄
        data 可包含: name
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE categories SET name = ? WHERE id = ?",
                (data['name'], id)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error updating category: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(id):
        """刪除記錄"""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM categories WHERE id = ?", (id,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error deleting category: {e}")
            return False
        finally:
            conn.close()
