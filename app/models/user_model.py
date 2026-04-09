from .db import get_db

class UserModel:
    @staticmethod
    def create(username, password_hash):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        db.commit()
        user_id = cursor.lastrowid
        db.close()
        return user_id

    @staticmethod
    def get_by_username(username):
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        db.close()
        return dict(user) if user else None

    @staticmethod
    def get_by_id(user_id):
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        db.close()
        return dict(user) if user else None
