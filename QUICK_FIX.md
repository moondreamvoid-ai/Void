# ⚡ 快速修復指南 - author 列缺失

## 🎯 3 步快速修復

### Step 1️⃣：打開 Supabase SQL Editor
訪問：https://app.supabase.com → 選擇您的項目 → SQL Editor

### Step 2️⃣：複製並執行以下代碼

```sql
-- 檢查表是否存在
SELECT EXISTS (
   SELECT 1 FROM information_schema.tables 
   WHERE table_name = 'user_scripts'
);

-- 添加 author 列
ALTER TABLE user_scripts 
ADD COLUMN IF NOT EXISTS author TEXT DEFAULT 'Unknown';

-- 驗證修復成功
SELECT column_name FROM information_schema.columns 
WHERE table_name = 'user_scripts' 
ORDER BY ordinal_position;
```

### Step 3️⃣：重新啟動應用
```bash
# 終止當前運行（Ctrl+C）
# 然後運行：
streamlit run app.py
```

---

## ✅ 驗證修復

運行此 SQL 檢查是否成功：
```sql
-- 應該看到 author 列在列表中
\d user_scripts;
```

或查看表詳情：
```sql
SELECT 
    column_name, 
    data_type, 
    column_default
FROM information_schema.columns
WHERE table_name = 'user_scripts'
ORDER BY ordinal_position;
```

---

## 🆘 如果還有問題

### 症狀 1️⃣：執行後仍有錯誤
**解決方案**：
1. 檢查 Supabase 連接是否有效
2. 確認您有修改表結構的權限
3. 檢查 RLS 政策是否正確啟用

```sql
-- 檢查 RLS 狀態
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE tablename = 'user_scripts';
```

### 症狀 2️⃣：新增腳本時出現 "Column not found" 
**解決方案**：
1. 驗證 author 列已正確添加
2. 刷新瀏覽器（Ctrl+F5）
3. 重新啟動 Streamlit 應用

### 症狀 3️⃣：表完全損壞
**終極解決方案**（警告：會失去數據）：

```sql
-- 備份舊表
CREATE TABLE user_scripts_backup AS 
SELECT * FROM user_scripts;

-- 刪除舊表
DROP TABLE IF EXISTS user_scripts CASCADE;

-- 創建新表
CREATE TABLE user_scripts (
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

-- 設置 RLS 政策
CREATE POLICY "Users can view own scripts" ON user_scripts
    FOR SELECT USING (user_id = auth.uid()::text);

CREATE POLICY "Users can insert own scripts" ON user_scripts
    FOR INSERT WITH CHECK (user_id = auth.uid()::text);

CREATE POLICY "Users can update own scripts" ON user_scripts
    FOR UPDATE USING (user_id = auth.uid()::text);

CREATE POLICY "Users can delete own scripts" ON user_scripts
    FOR DELETE USING (user_id = auth.uid()::text);

-- 創建性能索引
CREATE INDEX idx_user_scripts_user_id ON user_scripts(user_id);
CREATE INDEX idx_user_scripts_created_at ON user_scripts(created_at DESC);
CREATE INDEX idx_user_scripts_likes ON user_scripts(likes DESC);
```

---

## 📋 檢查清單

- [ ] 已打開 Supabase SQL Editor
- [ ] 已執行 ADD COLUMN 命令
- [ ] 已驗證列已添加（\d user_scripts）
- [ ] 已重新啟動 Streamlit 應用
- [ ] 已測試新增腳本
- [ ] 新增成功，無錯誤 ✅

---

## 🎉 完成！

現在您可以：
- ✅ 新增腳本
- ✅ 查看「最高評分」頁面
- ✅ 查看「最多下載」頁面
- ✅ 享受所有新功能

祝您使用愉快！🚀
