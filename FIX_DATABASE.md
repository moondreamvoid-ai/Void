# 🛠️ 修復資料庫 `author` 列缺失問題

## 問題描述
```
Error: Could not find the 'author' column of 'user_scripts' in the schema cache
Code: PGRST204
```

## ✅ 解決方案

### 方案 A：添加缺失的 `author` 列（推薦）

在 [Supabase Dashboard](https://app.supabase.com) SQL Editor 中執行以下命令：

```sql
-- 1️⃣ 檢查表結構
\d user_scripts;

-- 2️⃣ 添加 author 列（如果不存在）
ALTER TABLE user_scripts 
ADD COLUMN IF NOT EXISTS author TEXT;

-- 3️⃣ 設定現有記錄的 author 值（可選）
UPDATE user_scripts 
SET author = 'Unknown' 
WHERE author IS NULL;

-- 4️⃣ 驗證列已添加
SELECT column_name FROM information_schema.columns 
WHERE table_name = 'user_scripts';
```

### 方案 B：添加所有缺失的列（完整修復）

如果您的表還缺少其他列，請執行完整的 SQL 腳本：

```sql
-- 刪除舊表（警告：會失去所有數據！）
-- DROP TABLE IF EXISTS user_scripts CASCADE;

-- 創建完整的新表
CREATE TABLE IF NOT EXISTS user_scripts (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT DEFAULT '',
    script_text TEXT NOT NULL,
    tags TEXT[] DEFAULT '{}',
    author TEXT DEFAULT 'Unknown',
    likes INT DEFAULT 0,
    views INT DEFAULT 0,
    rating DECIMAL(3,2) DEFAULT 0.00,
    is_favorite BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 啟用 RLS
ALTER TABLE user_scripts ENABLE ROW LEVEL SECURITY;

-- 創建 RLS 政策
CREATE POLICY "Users can view own scripts" ON user_scripts
    FOR SELECT USING (user_id = auth.uid()::text);

CREATE POLICY "Users can insert own scripts" ON user_scripts
    FOR INSERT WITH CHECK (user_id = auth.uid()::text);

CREATE POLICY "Users can update own scripts" ON user_scripts
    FOR UPDATE USING (user_id = auth.uid()::text);

CREATE POLICY "Users can delete own scripts" ON user_scripts
    FOR DELETE USING (user_id = auth.uid()::text);

-- 創建索引以提高查詢性能
CREATE INDEX idx_user_scripts_user_id ON user_scripts(user_id);
CREATE INDEX idx_user_scripts_created_at ON user_scripts(created_at DESC);
CREATE INDEX idx_user_scripts_likes ON user_scripts(likes DESC);
```

### 方案 C：在應用程式中跳過 author 列（臨時方案）

如果您暫時不想修改資料庫，編輯 `app.py` 的第 427 行，移除 `author` 欄位：

```python
# ❌ 舊代碼
data = {
    "author": st.session_state.user.email.split('@')[0],
    ...
}

# ✅ 新代碼（移除 author 行）
data = {
    ...
    # 移除 author 行
}
```

## 📋 驗證修復

執行以下步驟確認修復成功：

1. 在 Supabase Dashboard 中查看 `user_scripts` 表結構
2. 確認 `author` 列存在
3. 重新啟動應用：`streamlit run app.py`
4. 嘗試創建新腳本，應該不再出現錯誤

## 🚀 推薦步驟

1. ✅ 執行方案 A（簡單快速）
2. ✅ 重新啟動應用
3. ✅ 測試創建新腳本
4. ✅ 如有其他列缺失，執行方案 B

---

**需要幫助？** 檢查 Supabase 日誌中是否有其他錯誤信息。
