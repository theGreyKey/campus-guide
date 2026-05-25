"""
湖南大学金融科技导航系统 - 主入口
"""


import streamlit as st
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from src.utils.helpers import load_css, render_header, init_session
from src.pages import course_page, job_page, skill_page, cert_page, search_page, roadmap_page

# 页面配置
st.set_page_config(
    page_title="湖南大学金融科技导航系统",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 加载样式
load_css()

# 渲染头部
render_header()

# 初始化session
init_session()

# 导航栏样式 - 浅蓝色背景
st.markdown("""
<style>
/* 隐藏默认侧边栏 */
[data-testid="stSidebar"] {
    display: none !important;
}
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}
/* 主内容区域全宽 */
.main .block-container {
    padding-top: 1rem;
    max-width: 100%;
}

/* 顶部导航栏容器样式 - 浅蓝色背景 */
.top-nav {
    background: linear-gradient(135deg, #5BA0C8, #4A90B8) !important;
    border-radius: 50px;
    padding: 10px 20px;
    margin-bottom: 25px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

/* 导航栏内所有按钮的容器 */
.top-nav .stButton {
    display: inline-block;
}

/* 导航按钮样式 */
.top-nav .stButton button {
    transition: all 0.3s ease !important;
    border-radius: 40px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    padding: 8px 20px !important;
    border: none !important;
    cursor: pointer !important;
}

/* primary 按钮样式（激活状态）- 白色背景深色文字 */
.top-nav .stButton button[kind="primary"] {
    background: #FFFFFF !important;
    color: #2A5C8A !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}

.top-nav .stButton button[kind="primary"]:hover {
    background: #E8EEF5 !important;
    color: #2A5C8A !important;
    transform: translateY(-2px);
}

/* secondary 按钮样式（未激活状态）- 使用 C0D9E8 */
.top-nav .stButton button[kind="secondary"] {
    background: #C0D9E8 !important;
    color: #1E2A3A !important;
}

.top-nav .stButton button[kind="secondary"]:hover {
    background: #A8C8D8 !important;
    color: #1E2A3A !important;
    transform: translateY(-2px);
}
</style>
""", unsafe_allow_html=True)

# 导航栏容器
st.markdown('<div class="top-nav">', unsafe_allow_html=True)

# 创建导航栏的列布局
nav_cols = st.columns(6)

# 导航栏选项
nav_options = [
    {"name": "课程地图", "icon": "📚", "page_key": "course"},
    {"name": "技能图谱", "icon": "🧠", "page_key": "skill"},
    {"name": "证书导航", "icon": "🎓", "page_key": "cert"},
    {"name": "职业生态", "icon": "💼", "page_key": "job"},
    {"name": "成长路线", "icon": "🌱", "page_key": "roadmap"},
    {"name": "智能搜索", "icon": "🔍", "page_key": "search"}
]

for idx, option in enumerate(nav_options):
    with nav_cols[idx]:
        is_active = st.session_state.nav_selected == option["name"]
        button_label = f"{option['icon']} {option['name']}"
        
        if st.button(
            button_label, 
            key=f"top_nav_{option['page_key']}", 
            use_container_width=True, 
            type="primary" if is_active else "secondary"
        ):
            if st.session_state.nav_selected != option["name"]:
                st.session_state.nav_selected = option["name"]
                st.session_state.selected_job = None
                st.session_state.selected_cert = None
                st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("---")

# 获取 URL 参数中的页面
try:
    query_params = st.query_params
    page_param = query_params.get("page", "")
    valid_pages = ["课程地图", "技能图谱", "证书导航", "职业生态", "成长路线", "智能搜索"]
    if page_param in valid_pages:
        st.session_state.nav_selected = page_param
except:
    pass

page = st.session_state.nav_selected

# 页面路由
if page == "课程地图":
    course_page.render()
elif page == "技能图谱":
    skill_page.render()
elif page == "证书导航":
    cert_page.render()
elif page == "职业生态":
    job_page.render()
elif page == "成长路线":
    roadmap_page.render()
elif page == "智能搜索":
    search_page.render()
else:
    course_page.render()