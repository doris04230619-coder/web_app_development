from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.task import Task
from app.models.category import Category

main_bp = Blueprint('main', __name__)

def login_required(f):
    def wrap(*args, **kwargs):
        if 'user_id' not in session:
            flash('請先登入。', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

@main_bp.route('/')
@login_required
def index():
    user_id = session['user_id']
    tasks = Task.get_all(user_id=user_id)
    categories = Category.get_all(user_id=user_id)
    return render_template('index.html', tasks=tasks, categories=categories)

@main_bp.route('/tasks/create', methods=['POST'])
@login_required
def create_task():
    user_id = session['user_id']
    title = request.form.get('title')
    category_id = request.form.get('category_id')
    priority = request.form.get('priority', 'medium')
    due_date = request.form.get('due_date')

    if not title:
        flash('任務標題為必填欄位。', 'error')
        return redirect(url_for('main.index'))

    # If category_id is empty string, set it to None
    if category_id == '':
        category_id = None

    data = {
        'user_id': user_id,
        'title': title,
        'category_id': category_id,
        'priority': priority,
        'due_date': due_date
    }
    
    if Task.create(data):
        flash('任務建立成功！', 'success')
    else:
        flash('任務建立失敗。', 'error')

    return redirect(url_for('main.index'))

@main_bp.route('/tasks/<int:id>/edit')
@login_required
def edit_task(id):
    user_id = session['user_id']
    task = Task.get_by_id(id)
    
    if not task or task['user_id'] != user_id:
        flash('找不到該任務或無權限編輯。', 'error')
        return redirect(url_for('main.index'))
        
    categories = Category.get_all(user_id=user_id)
    return render_template('tasks/edit.html', task=task, categories=categories)

@main_bp.route('/tasks/<int:id>/update', methods=['POST'])
@login_required
def update_task(id):
    user_id = session['user_id']
    task = Task.get_by_id(id)
    
    if not task or task['user_id'] != user_id:
        flash('找不到該任務或無權限操作。', 'error')
        return redirect(url_for('main.index'))

    title = request.form.get('title')
    category_id = request.form.get('category_id')
    priority = request.form.get('priority', 'medium')
    due_date = request.form.get('due_date')

    if not title:
        flash('任務標題為必填欄位。', 'error')
        return redirect(url_for('main.edit_task', id=id))
        
    # If category_id is empty string, set it to None
    if category_id == '':
        category_id = None

    data = {
        'title': title,
        'category_id': category_id,
        'priority': priority,
        'due_date': due_date
    }
    
    if Task.update(id, data):
        flash('任務更新成功！', 'success')
    else:
        flash('任務更新失敗。', 'error')
        
    return redirect(url_for('main.index'))

@main_bp.route('/tasks/<int:id>/delete', methods=['POST'])
@login_required
def delete_task(id):
    user_id = session['user_id']
    task = Task.get_by_id(id)
    
    if not task or task['user_id'] != user_id:
        flash('找不到該任務或無權限操作。', 'error')
        return redirect(url_for('main.index'))

    if Task.delete(id):
        flash('任務已刪除。', 'success')
    else:
        flash('任務刪除失敗。', 'error')

    return redirect(url_for('main.index'))

@main_bp.route('/tasks/<int:id>/toggle', methods=['POST'])
@login_required
def toggle_task(id):
    user_id = session['user_id']
    task = Task.get_by_id(id)
    
    if not task or task['user_id'] != user_id:
        flash('找不到該任務或無權限操作。', 'error')
        return redirect(url_for('main.index'))

    new_status = 'completed' if task['status'] == 'pending' else 'pending'
    
    if Task.update(id, {'status': new_status}):
        flash(f"任務標示為 {'已完成' if new_status == 'completed' else '未完成'}。", 'success')
    else:
        flash('狀態更新失敗。', 'error')

    return redirect(url_for('main.index'))

@main_bp.route('/categories/create', methods=['POST'])
@login_required
def create_category():
    user_id = session['user_id']
    name = request.form.get('name')

    if not name:
        flash('分類名稱為必填欄位。', 'error')
        return redirect(url_for('main.index'))

    data = {
        'user_id': user_id,
        'name': name
    }
    
    if Category.create(data):
        flash('分類建立成功！', 'success')
    else:
        flash('分類建立失敗。', 'error')

    return redirect(url_for('main.index'))

@main_bp.route('/categories/<int:id>/delete', methods=['POST'])
@login_required
def delete_category(id):
    user_id = session['user_id']
    category = Category.get_by_id(id)
    
    if not category or category['user_id'] != user_id:
        flash('找不到該分類或無權限操作。', 'error')
        return redirect(url_for('main.index'))

    if Category.delete(id):
        flash('分類已刪除。', 'success')
    else:
        flash('分類刪除失敗。', 'error')

    return redirect(url_for('main.index'))
