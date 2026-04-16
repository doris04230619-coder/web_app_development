import sqlite3
from app.models.database import get_db_connection

class Task:
    """提供 tasks 表格的 CRUD 操作"""

    @staticmethod
    def create(data):
        """
        新增一筆任務記錄
        data 應包含: user_id, title
        可選: category_id, status, priority, due_date
        """
        conn = get_db_connection()
        try:
            category_id = data.get('category_id')
            status = data.get('status', 'pending')
            priority = data.get('priority', 'medium')
            due_date = data.get('due_date')
            
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO tasks (user_id, category_id, title, status, priority, due_date)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (data['user_id'], category_id, data['title'], status, priority, due_date)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error creating task: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all(user_id=None):
        """取得所有記錄 (可依照 user_id 過濾)"""
        conn = get_db_connection()
        try:
            if user_id:
                return conn.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,)).fetchall()
            return conn.execute("SELECT * FROM tasks").fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching tasks: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(id):
        """取得單筆記錄"""
        conn = get_db_connection()
        try:
            return conn.execute("SELECT * FROM tasks WHERE id = ?", (id,)).fetchone()
        except sqlite3.Error as e:
            print(f"Error fetching task by id: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def update(id, data):
        """
        更新記錄
        data 可包含: category_id, title, status, priority, due_date
        """
        conn = get_db_connection()
        try:
            # First, get the existing task to preserve fields if not provided
            existing = Task.get_by_id(id)
            if not existing:
                return False

            category_id = data.get('category_id', existing['category_id'])
            title = data.get('title', existing['title'])
            status = data.get('status', existing['status'])
            priority = data.get('priority', existing['priority'])
            due_date = data.get('due_date', existing['due_date'])

            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE tasks
                SET category_id = ?, title = ?, status = ?, priority = ?, due_date = ?
                WHERE id = ?
                """,
                (category_id, title, status, priority, due_date, id)
            )
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error updating task: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(id):
        """刪除記錄"""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error deleting task: {e}")
            return False
        finally:
            conn.close()
