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

# 多語言翻譯
TRANSLATIONS = {
    "zh-tw": {
        "title": "Lua Script Hub",
        "welcome": "分享你的 Lua 腳本到雲端！",
        "login": "登入",
        "signup": "註冊",
        "login_subtitle": "登入帳號",
        "signup_subtitle": "建立新帳號",
        "email": "Email",
        "password": "密碼",
        "confirm_password": "確認密碼",
        "sign_in_btn": "✅ 登入",
        "sign_up_btn": "✅ 註冊",
        "sign_out_btn": "🚪 登出",
        "welcome_msg": "👋 歡迎，",
        "menu": "📂 選單",
        "choose_feature": "選擇功能：",
        "add_script": "📝 新增腳本",
        "my_scripts": "📚 我的腳本庫",
        "search_scripts": "🔍 搜尋腳本",
        "title_label": "標題 *",
        "title_placeholder": "輸入腳本標題",
        "tags_label": "標籤（用逗號分隔）",
        "tags_placeholder": "例：遊戲, 工具",
        "description_label": "描述（選填）",
        "description_placeholder": "說明你的腳本用途...",
        "save_btn": "💾 儲存到雲端",
        "clear_btn": "🔄 清空",
        "edit_btn": "✏️ 編輯",
        "delete_btn": "🗑️ 刪除",
        "download_btn": "📥 下載",
        "copy_btn": "📋 複製",
        "search_placeholder": "🔎 搜尋標題或標籤...",
        "language": "語言",
        "error_supabase": "❌ Supabase 連線失敗：",
        "error_email_password": "❌ 請輸入 Email 和密碼",
        "error_login_failed": "❌ 登入失敗，請檢查帳號密碼",
        "error_login": "❌ 登入錯誤：",
        "error_password_mismatch": "❌ 密碼不相符",
        "error_password_length": "❌ 密碼至少 6 個字符",
        "error_signup": "❌ 註冊錯誤：",
        "success_signup": "✅ 註冊成功！請檢查信箱驗證後登入",
        "success_login": "✅ 登入成功！",
        "success_save": "✅ 腳本已儲存到雲端！",
        "error_read_scripts": "❌ 讀取腳本失敗：",
        "no_scripts": "🎯 還沒有腳本，點擊左側菜單開始新增一個吧！",
        "scripts_count": "📊 共有 ",
        "scripts_count_suffix": " 個腳本",
        "untitled": "未命名",
        "info_copied": "ℹ️ 已複製到編輯器！",
        "success_deleted": "✅ 腳本已刪除",
        "error_delete": "❌ 刪除失敗：",
        "copy_code": "複製程式碼",
        "search_title": "🔍 搜尋所有腳本",
        "no_match": "🎯 沒有找到相符的腳本",
        "found_count": "📊 找到 ",
        "found_count_suffix": " 個腳本",
        "error_title_empty": "❌ 標題不能空白！",
        "error_code_empty": "❌ 腳本內容不能空白！",
        "start_lua": "-- 開始寫你的 Lua 腳本\nprint('Hello from Void!')",
    },
    "en": {
        "title": "Lua Script Hub",
        "welcome": "Share your Lua scripts to the cloud!",
        "login": "Login",
        "signup": "Sign Up",
        "login_subtitle": "Login to your account",
        "signup_subtitle": "Create a new account",
        "email": "Email",
        "password": "Password",
        "confirm_password": "Confirm Password",
        "sign_in_btn": "✅ Login",
        "sign_up_btn": "✅ Sign Up",
        "sign_out_btn": "🚪 Logout",
        "welcome_msg": "👋 Welcome, ",
        "menu": "📂 Menu",
        "choose_feature": "Choose a feature:",
        "add_script": "📝 Add Script",
        "my_scripts": "📚 My Scripts",
        "search_scripts": "🔍 Search Scripts",
        "title_label": "Title *",
        "title_placeholder": "Enter script title",
        "tags_label": "Tags (comma separated)",
        "tags_placeholder": "e.g.: Game, Tool",
        "description_label": "Description (Optional)",
        "description_placeholder": "Describe the purpose of your script...",
        "save_btn": "💾 Save to Cloud",
        "clear_btn": "🔄 Clear",
        "edit_btn": "✏️ Edit",
        "delete_btn": "🗑️ Delete",
        "download_btn": "📥 Download",
        "copy_btn": "📋 Copy",
        "search_placeholder": "🔎 Search title or tags...",
        "language": "Language",
        "error_supabase": "❌ Supabase connection failed: ",
        "error_email_password": "❌ Please enter Email and Password",
        "error_login_failed": "❌ Login failed, please check your credentials",
        "error_login": "❌ Login error: ",
        "error_password_mismatch": "❌ Passwords do not match",
        "error_password_length": "❌ Password must be at least 6 characters",
        "error_signup": "❌ Sign up error: ",
        "success_signup": "✅ Sign up successful! Please verify your email and login",
        "success_login": "✅ Login successful!",
        "success_save": "✅ Script saved to cloud!",
        "error_read_scripts": "❌ Failed to read scripts: ",
        "no_scripts": "🎯 No scripts yet, start by adding one from the left menu!",
        "scripts_count": "📊 You have ",
        "scripts_count_suffix": " scripts",
        "untitled": "Untitled",
        "info_copied": "ℹ️ Copied to editor!",
        "success_deleted": "✅ Script deleted",
        "error_delete": "❌ Delete failed: ",
        "copy_code": "Copy code",
        "search_title": "🔍 Search all scripts",
        "no_match": "🎯 No matching scripts found",
        "found_count": "📊 Found ",
        "found_count_suffix": " scripts",
        "error_title_empty": "❌ Title cannot be empty!",
        "error_code_empty": "❌ Script content cannot be empty!",
        "start_lua": "-- Start writing your Lua script\nprint('Hello from Void!')",
    }
}

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
    if "language" not in st.session_state:
        st.session_state.language = "zh-tw"

def t(key):
    """翻譯函數"""
    return TRANSLATIONS[st.session_state.language].get(key, key)

init_session_state()
supabase = st.session_state.supabase

def login_page():
    """登入頁面"""
    st.title(f"🌙 {t('title')}")
    st.write(t('welcome'))
    
    # 側邊欄語言選擇和 Discord 按鈕
    with st.sidebar:
        st.header(t('language'))
        lang = st.selectbox(
            t('language'),
            ["zh-tw", "en"],
            format_func=lambda x: "繁體中文" if x == "zh-tw" else "English",
            label_visibility="collapsed"
        )
        if lang != st.session_state.language:
            st.session_state.language = lang
            st.rerun()
        
        st.divider()
        st.markdown("""
        <div style="text-align: center;">
            <a href="https://discord.gg/qbBdERgaQ" target="_blank" style="text-decoration: none;">
                <button style="
                    background-color: #5865F2;
                    color: white;
                    padding: 12px 24px;
                    border: none;
                    border-radius: 8px;
                    font-size: 16px;
                    cursor: pointer;
                    width: 100%;
                    font-weight: bold;
                    transition: background-color 0.3s;
                " onmouseover="this.style.backgroundColor='#4752C4'" onmouseout="this.style.backgroundColor='#5865F2'">
                    💬 Discord
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs([t('login'), t('signup')])
    
    with tab1:
        st.subheader(t('login_subtitle'))
        email = st.text_input(t('email'), key="login_email")
        password = st.text_input(t('password'), type="password", key="login_password")
        
        if st.button(t('sign_in_btn'), use_container_width=True):
            if not email or not password:
                st.error(t('error_email_password'))
            else:
                try:
                    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    if res.user:
                        st.session_state.user = res.user
                        st.success(t('success_login'))
                        st.rerun()
                    else:
                        st.error(t('error_login_failed'))
                except Exception as e:
                    st.error(f"{t('error_login')}{str(e)}")
    
    with tab2:
        st.subheader(t('signup_subtitle'))
        email = st.text_input(t('email'), key="signup_email")
        password = st.text_input(t('password'), type="password", key="signup_password")
        confirm_password = st.text_input(t('confirm_password'), type="password", key="signup_confirm")
        
        if st.button(t('sign_up_btn'), use_container_width=True):
            if not email or not password:
                st.error(t('error_email_password'))
            elif password != confirm_password:
                st.error(t('error_password_mismatch'))
            elif len(password) < 6:
                st.error(t('error_password_length'))
            else:
                try:
                    res = supabase.auth.sign_up({"email": email, "password": password})
                    st.success(t('success_signup'))
                except Exception as e:
                    st.error(f"{t('error_signup')}{str(e)}")

def main_page():
    """主頁面"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title(f"🌙 {t('title')}")
    with col3:
        if st.button(t('sign_out_btn'), use_container_width=True):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.rerun()
    
    username = st.session_state.user.email.split('@')[0]
    st.write(f"{t('welcome_msg')}**{username}**！")
    st.divider()
    
    # 側邊欄選單
    with st.sidebar:
        st.header(t('menu'))
        page = st.radio(
            t('choose_feature'),
            [t('add_script'), t('my_scripts'), t('search_scripts')],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        # 語言選擇
        st.subheader(t('language'))
        lang = st.selectbox(
            t('language'),
            ["zh-tw", "en"],
            format_func=lambda x: "繁體中文" if x == "zh-tw" else "English",
            label_visibility="collapsed"
        )
        if lang != st.session_state.language:
            st.session_state.language = lang
            st.rerun()
        
        st.divider()
        
        # Discord 按鈕
        st.markdown("""
        <div style="text-align: center;">
            <a href="https://discord.gg/qbBdERgaQ" target="_blank" style="text-decoration: none;">
                <button style="
                    background-color: #5865F2;
                    color: white;
                    padding: 12px 24px;
                    border: none;
                    border-radius: 8px;
                    font-size: 16px;
                    cursor: pointer;
                    width: 100%;
                    font-weight: bold;
                    transition: background-color 0.3s;
                " onmouseover="this.style.backgroundColor='#4752C4'" onmouseout="this.style.backgroundColor='#5865F2'">
                    💬 Discord
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    # 新增腳本頁面
    if page == t('add_script'):
        st.subheader(t('add_script'))
        
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input(t('title_label'), placeholder=t('title_placeholder'))
        with col2:
            tags = st.text_input(t('tags_label'), placeholder=t('tags_placeholder'))
        
        desc = st.text_area(t('description_label'), height=60, placeholder=t('description_placeholder'))
        
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
            if st.button(t('save_btn'), use_container_width=True):
                if not title.strip():
                    st.error(t('error_title_empty'))
                elif not st.session_state.lua_code.strip():
                    st.error(t('error_code_empty'))
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
                        st.success(t('success_save'))
                        st.session_state.lua_code = t('start_lua')
                        st.balloons()
                    except Exception as e:
                        st.error(f"❌ {str(e)}")
        with col2:
            if st.button(t('clear_btn'), use_container_width=True):
                st.session_state.lua_code = t('start_lua')
                st.rerun()
    
    # 我的腳本庫頁面
    elif page == t('my_scripts'):
        st.subheader(t('my_scripts'))
        
        try:
            scripts = supabase.table("user_scripts").select("*").eq("user_id", st.session_state.user.id).order("created_at", desc=True).execute().data
        except Exception as e:
            st.error(f"{t('error_read_scripts')}{str(e)}")
            scripts = []
        
        if not scripts:
            st.info(t('no_scripts'))
        else:
            st.write(f"{t('scripts_count')}**{len(scripts)}**{t('scripts_count_suffix')}")
            
            for s in scripts:
                with st.expander(f"🔹 {s.get('title', t('untitled'))} ({s.get('created_at', '')[:10]})"):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        if s.get('description'):
                            st.caption(f"📝 {s['description']}")
                        if s.get('tags'):
                            tags_str = " | ".join([f"🏷️ {tag}" for tag in s['tags']])
                            st.caption(tags_str)
                    
                    with col2:
                        if st.button(t('edit_btn'), key=f"edit_{s['id']}", use_container_width=True):
                            st.session_state.lua_code = s['script_text']
                            st.info(t('info_copied'))
                    
                    with col3:
                        if st.button(t('delete_btn'), key=f"delete_{s['id']}", use_container_width=True):
                            try:
                                supabase.table("user_scripts").delete().eq("id", s['id']).execute()
                                st.success(t('success_deleted'))
                                st.rerun()
                            except Exception as e:
                                st.error(f"{t('error_delete')}{str(e)}")
                    
                    st.code(s.get('script_text', ''), language="lua")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            t('download_btn'),
                            data=s.get('script_text', ''),
                            file_name=f"{s.get('title', 'script')}.lua",
                            mime="text/plain",
                            use_container_width=True
                        )
                    with col2:
                        if st.button(t('copy_btn'), key=f"copy_{s['id']}", use_container_width=True):
                            st.text_area(t('copy_code'), s.get('script_text', ''), height=100, disabled=True, key=f"textarea_{s['id']}")
    
    # 搜尋腳本頁面
    elif page == t('search_scripts'):
        st.subheader(t('search_title'))
        
        search_query = st.text_input(t('search_placeholder'))
        
        try:
            all_scripts = supabase.table("user_scripts").select("*").order("created_at", desc=True).execute().data
        except Exception as e:
            st.error(f"{t('error_read_scripts')}{str(e)}")
            all_scripts = []
        
        if search_query:
            query_lower = search_query.lower()
            filtered = [s for s in all_scripts if query_lower in s.get('title', '').lower() or any(query_lower in tag.lower() for tag in s.get('tags', []))]
        else:
            filtered = all_scripts
        
        if not filtered:
            st.info(t('no_match'))
        else:
            st.write(f"{t('found_count')}**{len(filtered)}**{t('found_count_suffix')}")
            
            for s in filtered:
                with st.expander(f"🔹 {s.get('title', t('untitled'))}"):
                    if s.get('description'):
                        st.caption(f"📝 {s['description']}")
                    if s.get('tags'):
                        tags_str = " | ".join([f"🏷️ {tag}" for tag in s['tags']])
                        st.caption(tags_str)
                    
                    st.code(s.get('script_text', ''), language="lua")
                    
                    st.download_button(
                        t('download_btn'),
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
