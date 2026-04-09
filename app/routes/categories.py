from flask import Blueprint

categories_bp = Blueprint('categories', __name__, url_prefix='/categories')

@categories_bp.route('/create', methods=['POST'])
def create_category():
    """
    POST: 接收表單傳入的分類名稱 (name)，寫入 CategoryModel 建立新分類，重導向至首頁
    """
    pass

@categories_bp.route('/<int:category_id>/delete', methods=['POST'])
def delete_category(category_id):
    """
    POST: 將指定的 category_id 的分類刪除，重導向至首頁
    """
    pass
