from .db import get_db

class TaskModel:
    @staticmethod
    def create(user_id, title, category_id=None, status='pending', priority='medium', due_date=None):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """INSERT INTO tasks (user_id, title, category_id, status, priority, due_date)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, title, category_id, status, priority, due_date)
        )
        db.commit()
        task_id = cursor.lastrowid
        db.close()
        return task_id

    @staticmethod
    def get_all_by_user(user_id):
        db = get_db()
        tasks = db.execute(
            "SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC", 
            (user_id,)
        ).fetchall()
        db.close()
        return [dict(t) for t in tasks]

    @staticmethod
    def get_by_id(task_id, user_id):
        db = get_db()
        task = db.execute(
            "SELECT * FROM tasks WHERE id = ? AND user_id = ?", 
            (task_id, user_id)
        ).fetchone()
        db.close()
        return dict(task) if task else None

    @staticmethod
    def update(task_id, user_id, title=None, category_id=None, status=None, priority=None, due_date=None):
        db = get_db()
        task = db.execute(
            "SELECT * FROM tasks WHERE id = ? AND user_id = ?", 
            (task_id, user_id)
        ).fetchone()
        
        if not task:
            db.close()
            return False
            
        update_fields = []
        params = []
        if title is not None:
            update_fields.append("title = ?")
            params.append(title)
        if category_id is not None:
            update_fields.append("category_id = ?")
            params.append(category_id)
        if status is not None:
            update_fields.append("status = ?")
            params.append(status)
        if priority is not None:
            update_fields.append("priority = ?")
            params.append(priority)
        if due_date is not None:
            update_fields.append("due_date = ?")
            params.append(due_date)
            
        if not update_fields:
            db.close()
            return True
            
        query = f"UPDATE tasks SET {', '.join(update_fields)} WHERE id = ? AND user_id = ?"
        params.extend([task_id, user_id])
        
        db.execute(query, tuple(params))
        db.commit()
        db.close()
        return True

    @staticmethod
    def delete(task_id, user_id):
        db = get_db()
        cursor = db.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
        db.commit()
        deleted = cursor.rowcount > 0
        db.close()
        return deleted

    @staticmethod
    def toggle_status(task_id, user_id):
        db = get_db()
        task = db.execute(
            "SELECT status FROM tasks WHERE id = ? AND user_id = ?", 
            (task_id, user_id)
        ).fetchone()
        
        if not task:
            db.close()
            return False
        
        new_status = 'completed' if task['status'] == 'pending' else 'pending'
        db.execute(
            "UPDATE tasks SET status = ? WHERE id = ? AND user_id = ?", 
            (new_status, task_id, user_id)
        )
        db.commit()
        db.close()
        return True
