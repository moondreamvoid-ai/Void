import streamlit as st
from st_supabase_connection import SupabaseConnection
from code_editor import code_editor
from datetime import datetime

# 頁面配置
st.set_page_config(
    page_title="Lua Script Hub",
    page_icon="🌙",
    layout="centered",
    initial_sidebar_state="auto"
)

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

# 初始化 Session State
def init_session_state():
    if "supabase" not in st.session_state:
        try:
            st.session_state.supabase = st.connection(
                "supabase",
                type=SupabaseConnection,
                url=st.secrets["SUPABASE_URL"],
                key=st.secrets["SUPABASE_KEY"]
            )
        except Exception as e:
            st.error(f"❌ Supabase 連線失敗：{str(e)}")
            st.stop()
    
    if "user" not in st.session_state:
        st.session_state.user = None
    if "lua_code" not in st.session_state:
        st.session_state.lua_code = "-- 開始寫你的 Lua 腳本\nprint('Hello from Void!')"

init_session_state()
supabase = st.session_state.supabase

def login_page():
    """登入頁面"""
    st.title("🌙 Lua Script Hub")
    st.write("分享你的 Lua 腳本到雲端！")
    
    tab1, tab2 = st.tabs(["登入", "註冊"])
    
    with tab1:
        st.subheader("登入帳號")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("密碼", type="password", key="login_password")
        
        if st.button("✅ 登入", use_container_width=True):
            if not email or not password:
                st.error("❌ 請輸入 Email 和密碼")
            else:
                try:
                    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    if res.user:
                        st.session_state.user = res.user
                        st.success("✅ 登入成功！")
                        st.rerun()
                    else:
                        st.error("❌ 登入失敗，請檢查帳號密碼")
                except Exception as e:
                    st.error(f"❌ 登入錯誤：{str(e)}")
    
    with tab2:
        st.subheader("建立新帳號")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("密碼", type="password", key="signup_password")
        confirm_password = st.text_input("確認密碼", type="password", key="signup_confirm")
        
        if st.button("✅ 註冊", use_container_width=True):
            if not email or not password:
                st.error("❌ 請輸入 Email 和密碼")
            elif password != confirm_password:
                st.error("❌ 密碼不相符")
            elif len(password) < 6:
                st.error("❌ 密碼至少 6 個字符")
            else:
                try:
                    res = supabase.auth.sign_up({"email": email, "password": password})
                    st.success("✅ 註冊成功！請檢查信箱驗證後登入")
                except Exception as e:
                    st.error(f"❌ 註冊錯誤：{str(e)}")

def main_page():
    """主頁面"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🌙 Lua Script Hub")
    with col3:
        if st.button("🚪 登出", use_container_width=True):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.rerun()
    
    username = st.session_state.user.email.split('@')[0]
    st.write(f"👋 歡迎，**{username}**！")
    st.divider()
    
    # 側邊欄選單
    with st.sidebar:
        st.header("📂 選單")
        page = st.radio(
            "選擇功能：",
            ["📝 新增腳本", "📚 我的腳本庫", "🔍 搜尋腳本"],
            label_visibility="collapsed"
        )
    
    # 新增腳本頁面
    if page == "📝 新增腳本":
        st.subheader("📝 新增腳本")
        
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("標題 *", placeholder="輸入腳本標題")
        with col2:
            tags = st.text_input("標籤（用逗號分隔）", placeholder="例：遊戲, 工具")
        
        desc = st.text_area("描述（選填）", height=60, placeholder="說明你的腳本用途...")
        
        # 編輯器
        response = code_editor(
            st.session_state.lua_code,
            lang="lua",
            theme="vs-dark",
            height=400,
            options={"fontSize": 15, "lineNumbers": "on", "wordWrap": "on"}
        )
        
        if response.get("type") == "submit":
            st.session_state.lua_code = response.get("text", st.session_state.lua_code)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 儲存到雲端", use_container_width=True):
                if not title.strip():
                    st.error("❌ 標題不能空白！")
                elif not st.session_state.lua_code.strip():
                    st.error("❌ 腳本內容不能空白！")
                else:
                    try:
                        data = {
                            "user_id": st.session_state.user.id,
                            "title": title.strip(),
                            "description": desc.strip(),
                            "script_text": st.session_state.lua_code,
                            "tags": [t.strip() for t in tags.split(",") if t.strip()]
                        }
                        supabase.table("user_scripts").insert(data).execute()
                        st.success("✅ 腳本已儲存到雲端！")
                        st.session_state.lua_code = "-- 開始寫你的 Lua 腳本\nprint('Hello from Void!')"
                        st.balloons()
                    except Exception as e:
                        st.error(f"❌ 儲存失敗：{str(e)}")
        with col2:
            if st.button("🔄 清空", use_container_width=True):
                st.session_state.lua_code = "-- 開始寫你的 Lua 腳本\nprint('Hello from Void!')"
                st.rerun()
    
    # 我的腳本庫頁面
    elif page == "📚 我的腳本庫":
        st.subheader("📚 我的腳本庫")
        
        try:
            scripts = supabase.table("user_scripts").select("*").eq("user_id", st.session_state.user.id).order("created_at", desc=True).execute().data
        except Exception as e:
            st.error(f"❌ 讀取腳本失敗：{str(e)}")
            scripts = []
        
        if not scripts:
            st.info("🎯 還沒有腳本，點擊左側菜單開始新增一個吧！")
        else:
            st.write(f"📊 共有 **{len(scripts)}** 個腳本")
            
            for s in scripts:
                with st.expander(f"🔹 {s.get('title', '未命名')} ({s.get('created_at', '')[:10]})"):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        if s.get('description'):
                            st.caption(f"📝 {s['description']}")
                        if s.get('tags'):
                            tags_str = " | ".join([f"🏷️ {tag}" for tag in s['tags']])
                            st.caption(tags_str)
                    
                    with col2:
                        if st.button("✏️ 編輯", key=f"edit_{s['id']}", use_container_width=True):
                            st.session_state.lua_code = s['script_text']
                            st.info("ℹ️ 已複製到編輯器！")
                    
                    with col3:
                        if st.button("🗑️ 刪除", key=f"delete_{s['id']}", use_container_width=True):
                            try:
                                supabase.table("user_scripts").delete().eq("id", s['id']).execute()
                                st.success("✅ 腳本已刪除")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ 刪除失敗：{str(e)}")
                    
                    st.code(s.get('script_text', ''), language="lua")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            "📥 下載",
                            data=s.get('script_text', ''),
                            file_name=f"{s.get('title', 'script')}.lua",
                            mime="text/plain",
                            use_container_width=True
                        )
                    with col2:
                        if st.button("📋 複製", key=f"copy_{s['id']}", use_container_width=True):
                            st.text_area("複製程式碼", s.get('script_text', ''), height=100, disabled=True, key=f"textarea_{s['id']}")
    
    # 搜尋腳本頁面
    elif page == "🔍 搜尋腳本":
        st.subheader("🔍 搜尋所有腳本")
        
        search_query = st.text_input("🔎 搜尋標題或標籤...")
        
        try:
            all_scripts = supabase.table("user_scripts").select("*").order("created_at", desc=True).execute().data
        except Exception as e:
            st.error(f"❌ 讀取腳本失敗：{str(e)}")
            all_scripts = []
        
        if search_query:
            query_lower = search_query.lower()
            filtered = [s for s in all_scripts if query_lower in s.get('title', '').lower() or any(query_lower in tag.lower() for tag in s.get('tags', []))]
        else:
            filtered = all_scripts
        
        if not filtered:
            st.info("🎯 沒有找到相符的腳本")
        else:
            st.write(f"📊 找到 **{len(filtered)}** 個腳本")
            
            for s in filtered:
                with st.expander(f"🔹 {s.get('title', '未命名')}"):
                    if s.get('description'):
                        st.caption(f"📝 {s['description']}")
                    if s.get('tags'):
                        tags_str = " | ".join([f"🏷️ {tag}" for tag in s['tags']])
                        st.caption(tags_str)
                    
                    st.code(s.get('script_text', ''), language="lua")
                    
                    st.download_button(
                        "📥 下載",
                        data=s.get('script_text', ''),
                        file_name=f"{s.get('title', 'script')}.lua",
                        mime="text/plain",
                        use_container_width=True
                    )

# 主應用邏輯
if not st.session_state.user:
    login_page()
else:
    main_page()
