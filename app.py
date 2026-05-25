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
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 加载样式
load_css()

# 渲染头部
render_header()

# 初始化session
init_session()

# 导航栏样式
st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: none !important;
}
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}

.top-nav {
    position: sticky;
    top: 0.6rem;
    z-index: 20;
    padding: 0.8rem;
    margin-bottom: 1.2rem;
    border: 1px solid var(--line) !important;
    border-radius: var(--radius-lg) !important;
    background: linear-gradient(180deg, rgba(12, 23, 39, 0.9) 0%, rgba(8, 16, 28, 0.92) 100%) !important;
    box-shadow: var(--shadow-soft) !important;
    backdrop-filter: blur(18px);
}

.top-nav-shell {
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
}

.top-nav-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    padding: 0.15rem 0.2rem 0;
}

.top-nav-title {
    color: var(--ink) !important;
    font-size: 0.96rem;
    font-weight: 680;
}

.top-nav-caption {
    color: var(--muted) !important;
    font-size: 0.82rem;
    margin-top: 0.18rem;
}

.top-nav-status {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.42rem 0.72rem;
    border-radius: 999px;
    background: rgba(62, 139, 255, 0.12);
    border: 1px solid rgba(62, 139, 255, 0.2);
    color: #A9CAFF !important;
    font-size: 0.76rem;
    font-weight: 700;
    white-space: nowrap;
}

.top-nav .stButton {
    display: inline-block;
}

.top-nav .stButton button {
    transition: all 160ms var(--ease-out) !important;
    border-radius: 14px !important;
    font-weight: 650 !important;
    font-size: 0.92rem !important;
    padding: 0.72rem 0.7rem !important;
    border: 1px solid transparent !important;
    cursor: pointer !important;
    min-height: 48px !important;
}

.top-nav .stButton button[kind="primary"] {
    background: linear-gradient(135deg, rgba(62, 139, 255, 0.2) 0%, rgba(62, 139, 255, 0.12) 100%) !important;
    color: #F7FBFF !important;
    border-color: rgba(62, 139, 255, 0.32) !important;
    box-shadow: inset 0 0 0 1px rgba(62, 139, 255, 0.12), 0 14px 28px rgba(18, 42, 82, 0.24) !important;
}

.top-nav .stButton button[kind="primary"]:hover {
    background: linear-gradient(135deg, rgba(62, 139, 255, 0.26) 0%, rgba(62, 139, 255, 0.16) 100%) !important;
    color: #FFFFFF !important;
    transform: translateY(-1px);
}

.top-nav .stButton button[kind="secondary"] {
    background: rgba(255,255,255,0.02) !important;
    color: var(--muted) !important;
    border-color: rgba(148, 175, 206, 0.12) !important;
}

.top-nav .stButton button[kind="secondary"]:hover {
    background: rgba(62, 139, 255, 0.1) !important;
    color: var(--ink) !important;
    transform: translateY(-1px);
}

@media (max-width: 768px) {
    .top-nav-meta {
        flex-direction: column;
        align-items: flex-start;
    }
}
</style>
""", unsafe_allow_html=True)

# 导航栏容器
st.markdown('<div class="top-nav"><div class="top-nav-shell">', unsafe_allow_html=True)
st.markdown(f"""
<div class="top-nav-meta">
    <div>
        <div class="top-nav-title">Navigation workspace</div>
        <div class="top-nav-caption">按模块切换课程、技能、证书、职业、路线与搜索视图。</div>
    </div>
    <div class="top-nav-status">Current · {st.session_state.nav_selected}</div>
</div>
""", unsafe_allow_html=True)

# 创建导航栏的列布局
nav_cols = st.columns(6)

# 导航栏选项
nav_options = [
    {"name": "课程地图", "page_key": "course"},
    {"name": "技能图谱", "page_key": "skill"},
    {"name": "证书导航", "page_key": "cert"},
    {"name": "职业生态", "page_key": "job"},
    {"name": "成长路线", "page_key": "roadmap"},
    {"name": "智能搜索", "page_key": "search"}
]

for idx, option in enumerate(nav_options):
    with nav_cols[idx]:
        is_active = st.session_state.nav_selected == option["name"]
        button_label = option["name"]

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

st.markdown('</div></div>', unsafe_allow_html=True)

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
