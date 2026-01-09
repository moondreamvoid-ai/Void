import streamlit as st
from st_supabase_connection import SupabaseConnection
from code_editor import code_editor

# 手機優化 CSS
st.markdown("""
<style>
    .stApp { font-size: 16px !important; }
    .stButton > button { font-size: 18px; padding: 14px 24px; width: 100%; margin: 8px 0; }
    .stTextInput > div > div > input, .stTextArea > div > div > textarea { font-size: 16px; }
    section[data-testid="stSidebar"] { width: 100% !important; }
    .block-container { padding: 1rem !important; }
</style>
""", unsafe_allow_html=True)

# Supabase 連線 - 正確寫法
if "supabase" not in st.session_state:
    st.session_state.supabase = st.connection(
        "supabase",
        type=SupabaseConnection,
        url=st.secrets["SUPABASE_URL"],
        key=st.secrets["SUPABASE_KEY"]
    )

supabase = st.session_state.supabase

# 登入狀態
if "user" not in st.session_state:
    st.session_state.user = None

if not st.session_state.user:
    st.title("Lua Script Hub - 登入")
    email = st.text_input("Email")
    password = st.text_input("密碼", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("登入"):
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                if res.user:
                    st.session_state.user = res.user
                    st.rerun()
                else:
                    st.error("登入失敗，請檢查帳號密碼")
            except Exception as e:
                st.error(f"登入錯誤：{str(e)}")
    
    with col2:
        if st.button("註冊"):
            try:
                res = supabase.auth.sign_up({"email": email, "password": password})
                st.success("註冊成功！請檢查信箱驗證（若需要）後登入")
            except Exception as e:
                st.error(f"註冊錯誤：{str(e)}")

else:
    st.title("你的 Lua Script Hub")
    st.write(f"歡迎，{st.session_state.user.email.split('@')[0]}！")

    if st.button("登出"):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.rerun()

    # 新增腳本區
    st.subheader("新增腳本")
    title = st.text_input("標題（必填）")
    desc = st.text_area("描述（選填）", height=80)
    tags = st.text_input("標籤（用逗號分隔）")

    # 預設或上次編輯的 code
    lua_code = st.session_state.get("lua_code", "-- 開始寫你的 Lua 腳本\nprint('Hello from mobile!')")

    # 編輯器
    response = code_editor(
        lua_code,
        lang="lua",
        theme="vs-dark",
        height=400,  # 手機上固定高度較穩，之後可加 toggle
        options={"fontSize": 15, "lineNumbers": "on", "wordWrap": "on"}
    )

    if response["type"] == "submit":
        lua_code = response["text"]
        st.session_state.lua_code = lua_code  # 保留編輯內容

    if st.button("儲存到雲端"):
        if not title.strip():
            st.error("標題不能空白！")
        else:
            try:
                data = {
                    "user_id": st.session_state.user.id,
                    "title": title,
                    "description": desc,
                    "script_text": lua_code,
                    "tags": [t.strip() for t in tags.split(",") if t.strip()]
                }
                supabase.table("user_scripts").insert(data).execute()
                st.success("腳本已儲存到雲端！")
                # 可選：清空輸入欄位
                # st.session_state.lua_code = "-- 新腳本開始"
            except Exception as e:
                st.error(f"儲存失敗：{str(e)}")

    # 顯示我的腳本
    st.subheader("我的腳本庫")
    try:
        scripts = supabase.table("user_scripts").select("*").eq("user_id", st.session_state.user.id).order("updated_at", desc=True).execute().data
    except Exception as e:
        st.error(f"讀取腳本失敗：{str(e)}")
        scripts = []

    for s in scripts or []:
        with st.expander(f"{s['title']} ({s['updated_at'][:10]})"):
            if s['description']:
                st.caption(s['description'])
            if s['tags']:
                st.caption("標籤：" + ", ".join(s['tags']))
            st.code(s['script_text'], language="lua")
            if st.button("複製腳本", key=f"copy_{s['id']}"):
                st.info("已顯示腳本，可長按複製文字！（Streamlit 無法自動複製到剪貼簿）")
                # 可選：顯示大塊文字方便複製
                st.text_area("點這裡長按複製", s['script_text'], height=150, disabled=True)