#!/usr/bin/env python3
"""
Lua Script Hub - 主啟動腳本
執行此腳本以啟動 Streamlit 應用
"""

import subprocess
import sys
import os

def main():
    """啟動 Streamlit 應用"""
    
    # 檢查必要的環境變數
    required_secrets = ['SUPABASE_URL', 'SUPABASE_KEY']
    
    # 嘗試從 .streamlit/secrets.toml 讀取
    secrets_file = os.path.join('.streamlit', 'secrets.toml')
    
    if os.path.exists(secrets_file):
        print(f"✅ 找到 secrets 配置文件：{secrets_file}")
    else:
        print(f"⚠️  未找到 {secrets_file}，請確保已設定 Supabase 金鑰")
    
    # 啟動 Streamlit 應用
    print("🚀 啟動 Lua Script Hub...")
    print("-" * 50)
    
    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "app.py", "--logger.level=error"],
            check=True
        )
    except KeyboardInterrupt:
        print("\n\n👋 應用已關閉")
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 應用啟動失敗：{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
