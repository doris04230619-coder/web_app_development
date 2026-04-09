from flask import Blueprint

# tasks_bp 將作為首頁的主要邏輯整合
tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def index():
    """
    GET: 驗證使用者登入狀態。若已登入，撈取其全部 Tasks 與 Categories，渲染 index.html；若未登入則導向 /auth/login。
    """
    pass

@tasks_bp.route('/tasks/create', methods=['POST'])
def create_task():
    """
    POST: 接收表單資料 (title, category_id, priority, due_date等)，
          寫入 TaskModel 後，重導向至首頁 `/`
    """
    pass

@tasks_bp.route('/tasks/<int:task_id>/edit', methods=['GET'])
def edit_task(task_id):
    """
    GET: 確保使用者有權限，根據 task_id 取得該筆任務詳細資料，並渲染編輯頁面 (tasks/edit.html)
    """
    pass

@tasks_bp.route('/tasks/<int:task_id>/update', methods=['POST'])
def update_task(task_id):
    """
    POST: 接收修改後的標題、期限與優先級等資料，更新資料庫，完成後導向首頁
    """
    pass

@tasks_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """
    POST: 驗證擁有權，將對應 task_id 的任務從 DB 刪除，並導向首頁
    """
    pass

@tasks_bp.route('/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    """
    POST: 切換任務狀態 (pending 至 completed 或是反過來)，並導向首頁
    """
    pass
