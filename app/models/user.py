import sqlite3
from app.models.database import get_db_connection

class User:
    """提供 users 表格的 CRUD 操作"""

    @staticmethod
    def create(data):
        """
        新增一筆使用者記錄
        data 應包含: username, password_hash
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (data['username'], data['password_hash'])
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error creating user: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """取得所有記錄"""
        conn = get_db_connection()
        try:
            return conn.execute("SELECT * FROM users").fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching users: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(id):
        """取得單筆記錄"""
        conn = get_db_connection()
        try:
            return conn.execute("SELECT * FROM users WHERE id = ?", (id,)).fetchone()
        except sqlite3.Error as e:
            print(f"Error fetching user by id: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def update(id, data):
        """
        更新記錄
        data 可包含: username, password_hash
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET username = ?, password_hash = ? WHERE id = ?",
                (data['username'], data['password_hash'], id)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error updating user: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(id):
        """刪除記錄"""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (id,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error deleting user: {e}")
            return False
        finally:
            conn.close()
