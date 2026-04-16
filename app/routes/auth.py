from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('請填寫所有必填欄位。', 'error')
            return render_template('auth/register.html')

        # Check if username already exists
        all_users = User.get_all()
        if any(u['username'] == username for u in all_users):
            flash('該使用者名稱已被使用。', 'error')
            return render_template('auth/register.html')

        password_hash = generate_password_hash(password)
        user_id = User.create({'username': username, 'password_hash': password_hash})
        
        if user_id:
            flash('註冊成功！請登入。', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('註冊失敗，請稍後再試。', 'error')

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('請填寫所有必填欄位。', 'error')
            return render_template('auth/login.html')

        # To authenticate, we fetch the user by username. 
        # Unfortunately, our User model only has get_by_id and get_all. 
        # We can find the user from get_all for simplicity since this is a small MVP.
        all_users = User.get_all()
        user = next((u for u in all_users if u['username'] == username), None)

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            flash('登入成功！', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('使用者名稱或密碼錯誤。', 'error')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('您已成功登出。', 'success')
    return redirect(url_for('auth.login'))
