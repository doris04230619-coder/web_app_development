from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET: 渲染登入表單 (auth/login.html)
    POST: 接收 username 與 password 進行驗證，成功則寫入 Session 並重導向首頁，失敗則回傳錯誤
    """
    pass

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    GET: 渲染註冊表單 (auth/register.html)
    POST: 接收 username 與 password，雜湊加密後建立新帳號，成功後導回登入頁
    """
    pass

@auth_bp.route('/logout')
def logout():
    """
    GET: 清除目前的 Session 登入狀態 ('user_id')，重導向至登入頁面
    """
    pass
