# 路由與頁面設計 (Routes & Pages Design)

本文件描述了系統中所有的 URL 設計、對應的操作與使用到的 Jinja2 模板。依照 MVC 架構精神，我們將路由區分為 `auth` (驗證) 、 `tasks` (首頁/任務管理) 以及 `categories` (分類標籤) 三個模塊。

## 1. 路由總覽表格

| 功能模組 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| **【主頁面 (Tasks)】** | | | | |
| 任務列表(首頁) | GET | `/` | `index.html` | 顯示該使用者的所有任務與分類標籤 |
| **【會員驗證 (Auth)】** | | | | |
| 登入頁面 | GET | `/auth/login` | `auth/login.html` | 顯示登入表單 |
| 處理登入 | POST | `/auth/login` | — | 驗證帳密並寫入 Session，重導向至 `/` |
| 註冊頁面 | GET | `/auth/register` | `auth/register.html` | 顯示註冊表單 |
| 處理註冊 | POST | `/auth/register` | — | 建立密碼雜湊並寫入 DB，重導向至 `/auth/login` |
| 處理登出 | GET | `/auth/logout` | — | 清除 Session，重導向至 `/auth/login` |
| **【任務操作 (Tasks)】** | | | | |
| 建立任務 | POST | `/tasks/create` | — | 接收輸入存入 DB，重導向至 `/` |
| 編輯任務頁 | GET | `/tasks/<int:id>/edit`| `tasks/edit.html` | 顯示單一任務編輯表單頁 |
| 更新任務 | POST | `/tasks/<int:id>/update`| — | 修改並覆寫 DB 中的舊有資料，重導向 `/` |
| 刪除任務 | POST | `/tasks/<int:id>/delete`| — | 刪除單筆任務，重導向至 `/` |
| 狀態切換 | POST | `/tasks/<int:id>/toggle`| — | 切換完成/未完成狀態，重導向至 `/` |
| **【分類操作 (Categories)】** | | | | |
| 建立分類 | POST | `/categories/create` | — | 新增分類標籤，重導向至 `/` |
| 刪除分類 | POST | `/categories/<int:id>/delete`| — | 刪除分類標籤，重導向至 `/` |

---

## 2. 每個路由的詳細說明

### 2.1 首頁與任務模組 (`/` 與 `/tasks/...`)
- **GET `/`**
  - **輸入**：Session 中的 `user_id`。
  - **處理邏輯**：檢查是否有登入，未登入導回 `/auth/login`。若已登入，使用 `TaskModel.get_all_by_user()` 與 `CategoryModel.get_all_by_user()` 取回最新資料。
  - **輸出**：渲染 `index.html` 並傳遞變數 `tasks` 與 `categories`。
- **POST `/tasks/create`**
  - **輸入**：表單 `title`, `category_id`, `due_date`, `priority`。
  - **處理邏輯**：呼叫 `TaskModel.create(...)` 新增任務。
  - **輸出**：重導向至 `/`
- **GET `/tasks/<id>/edit`**
  - **處理邏輯**：呼叫 `TaskModel.get_by_id()` 檢查對應任務的擁有權。
  - **輸出**：渲染 `tasks/edit.html`。
- **POST `/tasks/<id>/update`, `/tasks/<id>/delete`, `/tasks/<id>/toggle`**
  - **處理邏輯**：分別操作 `TaskModel` 對應之更新、刪除、狀態反轉方法，確保更新前都有檢查請求者是否為擁有者 (user_id 相符)。
  - **輸出**：重導向回 `/`。

### 2.2 帳號驗證模組 (`/auth/...`)
- **GET `/auth/login`**
  - **輸出**：渲染 `auth/login.html` (登入畫面)。
- **POST `/auth/login`**
  - **輸入**：表單 `username`, `password`
  - **處理邏輯**：取得 DB 內雜湊密碼，使用 werkzeug 的 `check_password_hash` 驗證。成功則 `session['user_id'] = user.id`。
  - **輸出**：成功導向 `/`，失敗用 `flash` 發送「帳密錯誤」並重導向 `/auth/login`。
- **GET `/auth/register` 與 POST `/auth/register`**
  - **處理邏輯**：POST 收取資料後，用 `generate_password_hash` 加密密碼後寫入 DB。
  - **驗證失敗**：如果 username 已存在，重導向並以 `flash()` 顯示錯誤。

### 2.3 分類模組 (`/categories/...`)
- **POST `/categories/create`**
  - **輸入**：表單中的 `name`。
  - **處理邏輯**：呼叫 `CategoryModel.create()`。
  - **輸出**：重導向 `\`。

---

## 3. Jinja2 模板清單

這份專案我們建立共用的 `base.html` 基礎佈局，其他頁面皆透過 `{% extends "base.html" %}` 繼承。

1. `templates/base.html`：包含 HTML5 網頁標頭、置頂導覽列 (Navbar)、Flash 系統提示訊息顯示區塊、Bootstrap 或 Tailwind 的外部 CDN 引入。
2. `templates/auth/login.html`：包含一組精簡的帳密輸入表單與註冊連結。
3. `templates/auth/register.html`：註冊專用表單。
4. `templates/index.html`：系統首頁，包含：
   - 頂部：新增任務的小表單區塊與分類過濾器
   - 中部：所有任務列表，每個任務卡片右上角包含編輯、標記完成、刪除按鈕
   - 側邊/彈出層：新增與管理分類的小欄位
5. `templates/tasks/edit.html`：獨立一頁表單，用來進行資料的回填與任務詳細資訊的修改 (包含更改名稱、狀態、分類等)。
