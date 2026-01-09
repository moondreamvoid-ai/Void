# 🌙 Lua Script Hub

一個基於 Streamlit 和 Supabase 的雲端 Lua 腳本分享平台，最佳化手機使用體驗。

## ✨ 功能

### 核心功能
- 🔐 **多語言支持** - 完整的繁體中文和英文翻譯
- 🔐 **用戶認證** - 註冊、登入、登出
- 📝 **編輯腳本** - 線上 Lua 代碼編輯器，語法高亮
- ☁️ **雲端儲存** - 將腳本儲存到 Supabase 資料庫
- 📚 **腳本庫** - 查看、編輯、刪除個人腳本
- 🔍 **搜尋功能** - 按標題或標籤搜尋所有腳本

### 新增功能 ⭐
- 🔥 **熱門腳本** - 查看點讚數最多的腳本
- ⭐ **收藏夾** - 標記喜歡的腳本為收藏
- 🕐 **最近瀏覽** - 快速查看最近的腳本
- 👍 **點讚系統** - 給喜歡的腳本點讚
- 🔗 **分享功能** - 分享腳本的訊息
- 📥 **下載** - 下載腳本為 .lua 文件
- 📋 **複製** - 輕鬆複製腳本代碼
- 📊 **統計信息** - 查看腳本的瀏覽數、點讚數、評分
- 📱 **行動優化** - 為手機和平板最佳化的界面
- 💬 **Discord 按鈕** - 快速加入 Discord 社群

## 🚀 快速開始

### 1. 安裝依賴
```bash
pip install -r requirements.txt
```

### 2. 設定 Supabase 金鑰

編輯 `.streamlit/secrets.toml`：
```toml
SUPABASE_URL = "你的-supabase-url"
SUPABASE_KEY = "你的-supabase-anon-key"
```

> 從 [Supabase Dashboard](https://app.supabase.com) 的 **Settings → API** 取得這些值

### 3. 建立資料庫表

在 Supabase 資料庫中執行以下 SQL：

```sql
CREATE TABLE user_scripts (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    script_text TEXT NOT NULL,
    tags TEXT[] DEFAULT '{}',
    author TEXT,
    likes INT DEFAULT 0,
    views INT DEFAULT 0,
    rating DECIMAL(3,2) DEFAULT 0,
    is_favorite BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 啟用 RLS（行層級安全）
ALTER TABLE user_scripts ENABLE ROW LEVEL SECURITY;

-- 用戶只能看到自己的腳本
CREATE POLICY "Users can view own scripts" ON user_scripts
    FOR SELECT USING (user_id = auth.uid()::text);

-- 用戶只能新增自己的腳本
CREATE POLICY "Users can insert own scripts" ON user_scripts
    FOR INSERT WITH CHECK (user_id = auth.uid()::text);

-- 用戶只能更新自己的腳本
CREATE POLICY "Users can update own scripts" ON user_scripts
    FOR UPDATE USING (user_id = auth.uid()::text);

-- 用戶只能刪除自己的腳本
CREATE POLICY "Users can delete own scripts" ON user_scripts
    FOR DELETE USING (user_id = auth.uid()::text);
```

### 4. 啟動應用

#### 方法 1：使用 Python 腳本
```bash
python main.py
```

#### 方法 2：直接啟動 Streamlit
```bash
streamlit run app.py
```

應用將在 `http://localhost:8501` 開啟

## 📁 項目結構

```
Void/
├── app.py                    # 主 Streamlit 應用
├── main.py                   # 啟動腳本
├── requirements.txt          # Python 依賴
├── .streamlit/
│   └── secrets.toml         # Supabase 配置（不提交到 Git）
└── README.md                # 本文件
```

## 🔒 安全性

- ✅ 所有 Supabase 金鑰在 `.streamlit/secrets.toml` 中管理（在 .gitignore 中）
- ✅ 使用 Supabase 的行層級安全保護用戶數據
- ✅ 密碼最小要求 6 個字符
- ✅ 所有 API 調用都使用認證的用戶 ID

## 🛠️ 技術棧

- **前端框架**：[Streamlit](https://streamlit.io)
- **後端/資料庫**：[Supabase](https://supabase.com)
- **代碼編輯器**：[Streamlit Code Editor](https://github.com/not-nal/streamlit-code-editor)
- **認證**：Supabase Auth (JWT)
- **語言**：Python 3.8+

## 📝 使用說明

### 新增腳本
1. 登入或註冊帳號
2. 點擊「📝 新增腳本」
3. 輸入標題、描述和標籤
4. 在編輯器中編寫 Lua 代碼
5. 點擊「💾 儲存到雲端」

### 查看腳本
1. 點擊「📚 我的腳本庫」查看自己的腳本
2. 點擊「🔍 搜尋腳本」查看所有用戶的腳本

### 編輯/刪除
- 在「📚 我的腳本庫」中點擊「✏️ 編輯」或「🗑️ 刪除」

## 🐛 常見問題

**Q: Supabase 連線失敗**
- ✓ 檢查 `.streamlit/secrets.toml` 中的 URL 和 Key
- ✓ 確保 Supabase 項目已啟用
- ✓ 檢查網路連線

**Q: 無法登入**
- ✓ 確保使用註冊過的 Email
- ✓ 檢查密碼是否正確
- ✓ 如果忘記密碼，使用 Supabase Dashboard 重設

**Q: 查不到腳本**
- ✓ 等待一會讓資料庫同步
- ✓ 刷新頁面（F5）
- ✓ 檢查搜尋關鍵字

## 📞 支持

遇到問題？請提交 Issue 或 PR！

## 📄 授權

MIT License - 自由使用和修改

---

**Happy Scripting! 🎉**
