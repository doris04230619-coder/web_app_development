# 流程圖 (Flowcharts)

## 1. 使用者流程圖 (User Flow)
這張圖展示了使用者在系統中可能的操作路徑。由進入首頁開始，進行註冊、登入，以及登入後的各項任務管理操作。

```mermaid
flowchart LR
    Start([進入網站]) --> CheckAuth{是否已登入?}
    CheckAuth -- 否 --> Login[登入頁面]
    Login --> RegisterLink[點擊註冊] --> RegPage[註冊頁面]
    RegPage --> SubmitReg[送出註冊] --> Login
    Login --> SubmitLogin[送出登入] --> Home
    CheckAuth -- 是 --> Home[首頁 - 任務列表]
    
    Home --> Action{要執行什麼操作?}
    
    Action -- "點擊新增" --> CreateModal[填寫新增任務表單]
    CreateModal --> Home_Update[更新後的任務列表]
    
    Action -- "點擊編輯" --> EditModal[修改任務表單]
    EditModal --> Home_Update
    
    Action -- "點擊完成/取消完成" --> ToggleStatus[標記狀態]
    ToggleStatus --> Home_Update
    
    Action -- "點擊刪除" --> ConfirmDel[確認刪除視窗]
    ConfirmDel --> Home_Update
    
    Action -- "點擊登出" --> Logout([登出並返回登入頁])
    Logout --> Login
```

## 2. 系統序列圖 (Sequence Diagram)
這張序列圖描述了以「新增任務」為例時，使用者、前端介面、後端路由與資料庫之間的詳細互動過程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (HTML/JS)
    participant Flask as Flask (後端)
    participant DB as SQLite (資料庫)
    
    User->>Browser: 填寫「新增任務」欄位後點擊送出
    Browser->>Flask: POST /tasks (攜帶標題、到期日等資料)
    
    activate Flask
    Flask->>Flask: 驗證使用者是否已登入
    Flask->>Flask: 驗證接收到的資料格式是否合法
    
    alt 資料無效或未登入
        Flask-->>Browser: 回傳錯誤訊息並重整
        Browser-->>User: 顯示提示 (例如「標題不能為空」)
    else 資料正確
        Flask->>DB: INSERT INTO tasks (user_id, title, status)
        activate DB
        DB-->>Flask: 執行成功
        deactivate DB
        Flask-->>Browser: 重導向 (Redirect) 至首頁 /
    end
    deactivate Flask
    
    Browser->>Flask: GET / (重新要求首頁)
    Flask->>DB: SELECT * FROM tasks WHERE user_id=?
    DB-->>Flask: 回傳最新的任務列表
    Flask-->>Browser: 渲染 index.html (包含新任務的清單)
    Browser-->>User: 看到畫面已更新
```

## 3. 功能清單對照表

每個主要功能所對應的 URL 路徑與 HTTP 方法整理如下：

| 功能名稱 | HTTP 方法 | URL 路徑 | Controller / Route 說明 |
| --- | --- | --- | --- |
| 顯示登入頁面 | GET | `/login` | 渲染 `login.html` |
| 處理使用者登入 | POST | `/login` | 驗證帳密，成功則寫入 Session 並重導向回首頁 |
| 顯示註冊頁面 | GET | `/register` | 渲染 `register.html` |
| 處理使用者註冊 | POST | `/register` | 建立新帳號，重導向至登入頁 |
| 顯示首頁/任務列表| GET | `/` | 驗證登入狀態，渲染 `index.html` 帶入任務資料 |
| 處理新增任務 | POST | `/tasks` | 接收表單資料存入資料庫，並重導向至 `/` |
| 處理更新任務狀態 | POST | `/tasks/<id>/toggle` | 切換對應的任務狀態 (完成/未完成) |
| 處理編輯任務 | POST | `/tasks/<id>/edit` | 更新對應的任務資訊 |
| 處理刪除任務 | POST | `/tasks/<id>/delete` | 從資料庫刪除對應的任務 |
| 處理登出 | GET | `/logout` | 清除 Session 並導向登入頁面 |
