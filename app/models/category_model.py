from .db import get_db

class CategoryModel:
    @staticmethod
    def create(user_id, name):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO categories (user_id, name) VALUES (?, ?)",
            (user_id, name)
        )
        db.commit()
        category_id = cursor.lastrowid
        db.close()
        return category_id

    @staticmethod
    def get_all_by_user(user_id):
        db = get_db()
        categories = db.execute(
            "SELECT * FROM categories WHERE user_id = ? ORDER BY created_at DESC", 
            (user_id,)
        ).fetchall()
        db.close()
        return [dict(c) for c in categories]

    @staticmethod
    def get_by_id(category_id, user_id):
        db = get_db()
        category = db.execute(
            "SELECT * FROM categories WHERE id = ? AND user_id = ?", 
            (category_id, user_id)
        ).fetchone()
        db.close()
        return dict(category) if category else None

    @staticmethod
    def delete(category_id, user_id):
        db = get_db()
        cursor = db.execute("DELETE FROM categories WHERE id = ? AND user_id = ?", (category_id, user_id))
        db.commit()
        deleted = cursor.rowcount > 0
        db.close()
        return deleted
