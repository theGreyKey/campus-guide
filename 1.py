import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import networkx as nx
# 在现有 import 后面添加
import numpy as np
import plotly.express as px
from scipy.spatial.distance import cosine
import re

# 页面基础设置
st.set_page_config(
    page_title="湖南大学金融科技导航系统",
    page_icon="📘",
    layout="wide"
)


# 主题色定义
THEME = {
    "primary": "#2A5C8A",
    "primary_light": "#4A7CAA",
    "primary_dark": "#1A4C7A",
    "secondary": "#5BA0C8",
    "accent": "#E8A87C",
    "bg": "#F5F7FA",
    "card_bg": "#FFFFFF",
    "text": "#1E2A3A",
    "text_light": "#6B7A8A",
    "border": "#E2E8F0"
}


# 全局样式
st.markdown("""
<style>
    /* 引入 Font Awesome 图标库 */
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');
    
    /* 全局背景 */
    .stApp {
        background: linear-gradient(135deg, #F5F7FA 0%, #E8EEF5 100%);
    }
    
    /* 隐藏默认的侧边栏元素 */
    [data-testid="stSidebarCollapsedControl"] {
        display: none !important;
    }
    
    /* 隐藏右上角菜单和底部 */
    #MainMenu {
        visibility: hidden;
    }
    footer {
        visibility: hidden;
    }
    header {
        visibility: hidden;
    }
    
    /* 侧边栏样式 */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1A4C7A 0%, #2A5C8A 100%) !important;
        padding-top: 0 !important;
    }
    
    /* 侧边栏内容区域 */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        padding: 0.5rem 0.5rem 1rem 0.5rem;
        gap: 0;
    }
    
    /* 侧边栏头部 */
    .sidebar-header {
        text-align: center;
        padding: 1.5rem 0 1rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.15);
        margin-bottom: 1rem;
    }
    .sidebar-header .icon {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        color: white;
    }
    .sidebar-header .title {
        font-weight: 700;
        font-size: 1.2rem;
        color: white;
        letter-spacing: 1px;
    }
    .sidebar-header .subtitle {
        font-size: 0.7rem;
        opacity: 0.7;
        color: white;
        margin-top: 0.25rem;
    }
    
    /* 可点击职业卡片样式 */
    .clickable-job-card {
        background: #F5F7FA;
        border-radius: 12px;
        padding: 12px;
        text-align: center;
        margin: 5px;
        cursor: pointer;
        transition: all 0.2s ease;
        border: 1px solid #E2E8F0;
    }
    .clickable-job-card:hover {
        background: #E8EEF5;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-color: #2A5C8A;
    }
    
    /* 自定义按钮样式 - 覆盖 Streamlit 默认按钮样式 */
    .stButton button {
        width: 100%;
        margin: 4px 0;
        border-radius: 12px !important;
        padding: 10px 16px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    
    /* 未选中按钮样式 - 半透明白色 */
    .stButton button[data-baseweb="button"] {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: none !important;
    }
    
    /* 未选中按钮悬停效果 */
    .stButton button[data-baseweb="button"]:hover {
        background: rgba(255, 255, 255, 0.2) !important;
        transform: translateX(4px);
    }
    
    /* 选中按钮样式 - 浅蓝色（适配主题） */
    .stButton button[kind="primary"] {
        background: #D6E6F5 !important;
        color: #2A5C8A !important;
        border: none !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* 选中按钮悬停效果 */
    .stButton button[kind="primary"]:hover {
        background: #C5D9EB !important;
        transform: translateX(4px);
    }
    
    /* 底部信息 */
    .sidebar-footer {
        text-align: center;
        font-size: 0.7rem;
        opacity: 0.5;
        padding: 1rem;
        border-top: 1px solid rgba(255,255,255,0.1);
        margin-top: 2rem;
        color: white;
    }
    .sidebar-footer i {
        margin-right: 6px;
    }
    
    /* 主标题样式 */
    .main-title {
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .main-title h1 {
        background: linear-gradient(135deg, #2A5C8A, #5BA0C8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.8rem !important;
        font-weight: 700 !important;
        display: inline-block;
        margin-bottom: 0;
    }
    
    /* 副标题英文 */
    .sub-title {
        text-align: center;
        color: #6B7A8A;
        font-size: 0.9rem;
        letter-spacing: 2px;
        margin-top: -0.2rem;
        margin-bottom: 1rem;
    }
    
    /* 标签栏 - 柔和颜色 */
    .badge-container {
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .badge {
        display: inline-block;
        padding: 5px 16px;
        background: rgba(42,92,138,0.1);
        color: #2A5C8A;
        border-radius: 30px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 0 6px;
    }
    .badge i {
        margin-right: 6px;
    }
    
    /* 详情卡片 - 简洁列表样式 */
    .detail-list {
        background: #FFFFFF;
        border-radius: 20px;
        padding: 0.5rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
    }
    .detail-item {
        display: flex;
        padding: 0.8rem 1.5rem;
        border-bottom: 1px solid #E2E8F0;
    }
    .detail-item:last-child {
        border-bottom: none;
    }
    .detail-icon {
        width: 32px;
        color: #2A5C8A;
        font-size: 1.1rem;
    }
    .detail-label {
        width: 100px;
        font-weight: 600;
        color: #1E2A3A;
    }
    .detail-value {
        flex: 1;
        color: #1E2A3A;
    }
    
    /* 指标卡片两列布局 */
    .metric-item {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
    }
    .metric-value {
        font-size: 1.3rem;
        font-weight: 700;
        color: #2A5C8A;
    }
    .metric-label {
        font-size: 0.75rem;
        color: #6B7A8A;
        margin-top: 0.3rem;
    }
    
    /* 进度条美化 */
    .stProgress > div > div {
        background-color: #2A5C8A !important;
        border-radius: 10px;
    }
    .stProgress > div {
        background-color: #E2E8F0 !important;
        border-radius: 10px;
    }
    
    /* 信息框美化 */
    .stAlert {
        border-radius: 16px !important;
        border-left: 4px solid #2A5C8A !important;
    }
    
    /* 分割线 */
    hr {
        margin: 1.5rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #2A5C8A, transparent);
    }
    
    /* 指标卡片 */
    [data-testid="stMetric"] {
        background: #FFFFFF;
        padding: 1rem;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
    }
    [data-testid="stMetricValue"] {
        color: #2A5C8A !important;
        font-weight: 700 !important;
    }
    
    /* 跳转提示框样式 */
    .jump-success {
        background: linear-gradient(135deg, #D4EDDA, #C3E6CB);
        border-left: 4px solid #28A745;
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 20px;
        color: #155724;
    }
</style>
""", unsafe_allow_html=True)


# 标题区域
st.markdown("""
<div class="main-title">
    <h1><i class="fas fa-graduation-cap"></i> 湖南大学金融科技专业导航系统</h1>
</div>
<div class="sub-title">
    Hunan University FinTech Navigation System
</div>
<div class="badge-container">
    <span class="badge"><i class="fas fa-robot"></i> AI智能导航</span>
    <span class="badge"><i class="fas fa-chart-line"></i> 实时数据</span>
    <span class="badge"><i class="fas fa-bullseye"></i> 职业匹配</span>
    <span class="badge"><i class="fas fa-chart-pie"></i> 技能分析</span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")


# 读取Excel
course_df = pd.read_excel(r"D:\Desktop\fintech-guide\data\课程表.xlsx")
job_df = pd.read_excel(r"D:\Desktop\fintech-guide\data\职业表.xlsx")
skill_df = pd.read_excel(r"D:\Desktop\fintech-guide\data\技能表.xlsx")
certificate_df = pd.read_excel(r"D:\Desktop\fintech-guide\data\证书表.xlsx")

# 建立证书到职业的映射字典
cert_to_jobs_map = {}
for _, row in certificate_df.iterrows():
    cert_name = row["证书名称"]
    jobs_text = row.get("对应岗位", "")
    jobs_list = [j.strip() for j in str(jobs_text).split("、") if j.strip() and j.strip() != "nan"]
    cert_to_jobs_map[cert_name] = jobs_list

# 建立职业到证书的映射字典
job_to_certs_map = {}
for _, row in job_df.iterrows():
    job_name = row["岗位"]
    job_to_certs_map[job_name] = []

for cert_name, jobs in cert_to_jobs_map.items():
    for job in jobs:
        # 精确匹配
        if job in job_to_certs_map:
            job_to_certs_map[job].append(cert_name)
        else:
            # 模糊匹配
            for job_key in job_to_certs_map.keys():
                if job in job_key or job_key in job:
                    if cert_name not in job_to_certs_map[job_key]:
                        job_to_certs_map[job_key].append(cert_name)
                    break

certificate_links = pd.DataFrame([
    ("CQF", "Python数据分析", 0.8),
    ("CQF", "FRM", 0.7),
    ("CQF", "机器学习", 0.8),
    ("CFA", "FRM", 0.6),
    ("CFA", "FMVA®", 0.7),
    ("FRM", "SHMFTPP", 0.5),
    ("SHMFTPP", "银行金融科技基础", 0.6),
    ("机器学习", "DeepLearning.AI", 0.9),
    ("机器学习", "Kaggle", 0.7),
    ("DeepLearning.AI", "AI工程师", 0.7),
    ("Python数据分析", "Kaggle", 0.6),
    ("Python数据分析", "Tableau/Power BI", 0.5),
    ("CPA", "ACCA", 0.5),
    ("SOA", "中国精算师", 0.6),
], columns=["源证书", "目标证书", "关联强度"])

# 定义路线图数据
roadmaps = {
    "金科量化路线": {
        "certificates": ["Python数据分析", "CQF", "机器学习", "Kaggle"],
        "description": "专注于量化交易、算法策略开发的路线",
        "careers": ["量化研究员", "算法交易工程师", "金融数据科学家"]
    },
    "风控专家路线": {
        "certificates": ["FRM", "Python数据分析", "SHMFTPP"],
        "description": "专注于金融风险管理、合规风控的路线",
        "careers": ["风控建模工程师", "反洗钱分析师", "金融风险管理师"]
    },
    "金融科技产品路线": {
        "certificates": ["SHMFTPP", "FMVA®", "银行金融科技基础"],
        "description": "专注于金融科技产品设计、业务分析的路线",
        "careers": ["金融产品经理", "商业分析师", "金融科技咨询顾问"]
    },
    "AI金融路线": {
        "certificates": ["机器学习", "DeepLearning.AI", "AI工程师", "Kaggle"],
        "description": "专注于AI在金融领域应用的路线",
        "careers": ["金融AI工程师", "金融数据科学家", "机器学习工程师"]
    },
    "数据分析路线": {
        "certificates": ["Python数据分析", "Tableau/Power BI", "Kaggle"],
        "description": "专注于金融数据分析、可视化的路线",
        "careers": ["数据分析师", "商业分析师", "数据科学家"]
    }
}


# 左侧导航 按钮菜单
# 初始化导航状态
if "nav_selected" not in st.session_state:
    st.session_state.nav_selected = "课程地图"

# 初始化联动状态
if "selected_job_from_cert" not in st.session_state:
    st.session_state.selected_job_from_cert = None
if "selected_cert_from_job" not in st.session_state:
    st.session_state.selected_cert_from_job = None
if "jump_from_cert_to_job" not in st.session_state:
    st.session_state.jump_from_cert_to_job = False
if "jump_from_job_to_cert" not in st.session_state:
    st.session_state.jump_from_job_to_cert = False

# 侧边栏
st.sidebar.markdown("""
<div class="sidebar-header">
    <div class="icon"><i class="fas fa-chalkboard-user"></i></div>
    <div class="title">FinTech 导航</div>
    <div class="subtitle">湖南大学金融科技专业</div>
</div>
""", unsafe_allow_html=True)

# 课程地图按钮
if st.sidebar.button(
    "📚 课程地图",
    key="nav_course",
    use_container_width=True,
    type="primary" if st.session_state.nav_selected == "课程地图" else "secondary"
):
    st.session_state.nav_selected = "课程地图"
    st.rerun()

# 职业生态按钮
if st.sidebar.button(
    "💼 职业生态",
    key="nav_job",
    use_container_width=True,
    type="primary" if st.session_state.nav_selected == "职业生态" else "secondary"
):
    st.session_state.nav_selected = "职业生态"
    st.rerun()

# 技能图谱按钮
if st.sidebar.button(
    "🧠 技能图谱",
    key="nav_skill",
    use_container_width=True,
    type="primary" if st.session_state.nav_selected == "技能图谱" else "secondary"
):
    st.session_state.nav_selected = "技能图谱"
    st.rerun()

# 证书导航按钮
if st.sidebar.button(
    "🎓 证书导航",
    key="nav_certificate",
    use_container_width=True,
    type="primary" if st.session_state.nav_selected == "证书导航" else "secondary"
):
    st.session_state.nav_selected = "证书导航"
    st.rerun()

# 底部
st.sidebar.markdown("""
<div class="sidebar-footer">
    <i class="fas fa-database"></i> 数据实时更新
</div>
""", unsafe_allow_html=True)

# 获取当前选中的页面
page = st.session_state.nav_selected


# 页面1：课程地图 
if page == "课程地图":
    st.markdown('<h2><i class="fas fa-map"></i> 金融科技课程地图</h2>', unsafe_allow_html=True)

    course_list = course_df["课程名称"].tolist()
    selected_course = st.selectbox("🔍 选择课程查看详情", course_list)
    course_info = course_df[course_df["课程名称"] == selected_course].iloc[0]

    # 顶部指标卡片
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📅 开课学期", course_info["开课学期"])
    with col2:
        st.metric("📖 学分", course_info["学分"])
    with col3:
        st.metric("⚡ 综合难度", f"{course_info['难度(1-10)']}/10")
    with col4:
        st.metric("🏷️ 课程类别", course_info["课程类别"])

    st.markdown("---")

    # 雷达图
    categories = ["数学强度", "编程强度", "课程难度", "实际用途", "学习压力"]
    pressure_map = {"低": 3, "中": 6, "高": 9}
    pressure = pressure_map.get(course_info["学习压力等级"], 5)

    values = [
        course_info["数学强度(1-10)"],
        course_info["编程强度(1-10)"],
        course_info["难度(1-10)"],
        8,
        pressure
    ]

    categories_display = categories + [categories[0]]
    values_display = values + [values[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_display,
        theta=categories_display,
        fill='toself',
        line=dict(color="#2A5C8A", width=3),
        fillcolor='rgba(42,92,138,0.2)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10], tickfont=dict(color="#1E2A3A", size=13), gridcolor='#CBD5E1', linecolor='#CBD5E1'),
            angularaxis=dict(tickfont=dict(color="#1E2A3A", size=13, family="Microsoft YaHei"), gridcolor='#CBD5E1', linecolor='#CBD5E1'),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=False,
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#1E2A3A", size=13)
    )

    st.subheader("🧠 课程能力画像")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

    # 课程强度分析
    st.subheader("🔥 课程强度分析")
    col_strength1, col_strength2 = st.columns(2)

    with col_strength1:
        math_val = course_info["数学强度(1-10)"]
        st.progress(math_val / 10)
        st.write(f"📐 **数学强度**：{math_val}/10")
        st.caption("数学建模与理论分析能力要求")

        coding_val = course_info["编程强度(1-10)"]
        st.progress(coding_val / 10)
        st.write(f"💻 **编程强度**：{coding_val}/10")
        st.caption("代码实现与算法能力要求")

    with col_strength2:
        diff_val = course_info["难度(1-10)"]
        st.progress(diff_val / 10)
        st.write(f"⚡ **课程难度**：{diff_val}/10")
        st.caption("整体学习难度评估")

        st.progress(pressure / 10)
        st.write(f"💪 **学习压力**：{course_info['学习压力等级']}")
        st.caption("时间投入与心理压力评估")

    st.markdown("---")

    # 课程详情
    st.subheader("📘 课程详情")
    st.markdown(f"""
    <div class="detail-list">
        <div class="detail-item">
            <div class="detail-icon"><i class="fas fa-book"></i></div>
            <div class="detail-label">课程名称</div>
            <div class="detail-value">{course_info['课程名称']}</div>
        </div>
        <div class="detail-item">
            <div class="detail-icon"><i class="fas fa-tag"></i></div>
            <div class="detail-label">课程类别</div>
            <div class="detail-value">{course_info['课程类别']}</div>
        </div>
        <div class="detail-item">
            <div class="detail-icon"><i class="fas fa-lightbulb"></i></div>
            <div class="detail-label">实际用途</div>
            <div class="detail-value">{course_info['实际用途']}</div>
        </div>
        <div class="detail-item">
            <div class="detail-icon"><i class="fas fa-briefcase"></i></div>
            <div class="detail-label">对应职业方向</div>
            <div class="detail-value">{course_info['对应职业方向']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# 页面2：职业生态（带联动）
elif page == "职业生态":
    st.markdown('<h2><i class="fas fa-chart-network"></i> 金融科技职业生态图谱</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: #6B7A8A; margin-bottom: 1rem;"><i class="fas fa-circle"></i> 节点大小 = 进入难度 | <i class="fas fa-palette"></i> 节点颜色 = 行业前景评分</p>', unsafe_allow_html=True)

    # 处理从证书页面跳转过来的职业高亮
    if st.session_state.jump_from_cert_to_job and st.session_state.selected_job_from_cert:
        jump_job = st.session_state.selected_job_from_cert
        # 显示跳转成功提示
        st.markdown(f"""
        <div class="jump-success">
            ✨ 已从「证书导航」跳转，正在查看：<strong>{jump_job}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        # 添加返回按钮
        col_back1, col_back2 = st.columns([1, 5])
        with col_back1:
            if st.button("← 返回证书导航", key="back_to_cert_from_job"):
                st.session_state.jump_from_cert_to_job = False
                st.session_state.selected_job_from_cert = None
                st.session_state.nav_selected = "证书导航"
                st.rerun()
        st.markdown("---")
        
        # 自动选中跳转的职业
        if jump_job in job_df["岗位"].tolist():
            selected_job = jump_job
        else:
            # 尝试模糊匹配
            matches = job_df[job_df["岗位"].str.contains(jump_job[:6], na=False)]
            if len(matches) > 0:
                selected_job = matches.iloc[0]["岗位"]
                st.info(f"💡 未找到完全匹配的「{jump_job}」，已为您推荐相关职业：{selected_job}")
            else:
                selected_job = job_df["岗位"].tolist()[0]
                st.warning(f"未找到「{jump_job}」，已展示默认职业")
        
        # 重置跳转标志
        st.session_state.jump_from_cert_to_job = False
    else:
        # 正常的选择框
        job_list = job_df["岗位"].tolist()
        selected_job = st.selectbox("🔍 选择职业查看详情", job_list)
    
    job_info = job_df[job_df["岗位"] == selected_job].iloc[0]

    # 职业生态图谱
    G = nx.Graph()
    center_node = "金融科技"
    G.add_node(center_node)

    for _, row in job_df.iterrows():
        job = row["岗位"]
        G.add_node(job)
        G.add_edge(center_node, job)

    pos = nx.spring_layout(G, seed=42, k=1)

    # 边
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        mode='lines',
        line=dict(width=1, color='rgba(42,92,138,0.3)'),
        hoverinfo='none'
    )

    # 节点
    node_x, node_y, node_text, node_size, node_color = [], [], [], [], []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

        if node == center_node:
            node_text.append("🎯 金融科技职业核心")
            node_size.append(60)
            node_color.append(10)
        else:
            row = job_df[job_df["岗位"] == node].iloc[0]
            future = row["行业前景评分（10分制）"]
            difficulty = row["进入难度（1-10）"]
            hover = f"""
            <b>{node}</b><br><br>
            🏷️ 方向：{row['岗位属性与方向']}<br>
            💰 薪资：{row['薪资与薪资结构']}<br>
            📍 城市：{row['主要就业城市']}<br>
            🛠️ 技能：{row['技能要求（具体）'][:100]}...<br>
            🚀 前景：{future}/10
            """
            node_text.append(hover)
            node_size.append(difficulty * 5)
            node_color.append(future)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=node_text,
        marker=dict(
            showscale=True,
            colorscale='Blues',
            color=node_color,
            size=node_size,
            colorbar=dict(title="行业前景", tickfont=dict(color="#1E2A3A")),
            line=dict(width=1.5, color='white')
        )
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title="",
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=20, r=20, t=40),
            height=750,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            font=dict(color="#1E2A3A")
        )
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

    # 职业深度画像
    st.subheader("💼 职业深度画像")
    
    # 指标卡片 - 两列布局
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="metric-item">
            <div class="metric-value">{job_info['行业前景评分（10分制）']}/10</div>
            <div class="metric-label">🚀 行业前景</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="metric-item">
            <div class="metric-value">{job_info['进入难度（1-10）']}/10</div>
            <div class="metric-label">🎯 进入难度</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-item">
            <div class="metric-value">{job_info['压力与工作时间']}</div>
            <div class="metric-label">🔥 工作压力</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="metric-item">
            <div class="metric-value">{job_info['学业倾向'][:20]}{"..." if len(job_info['学业倾向']) > 20 else ""}</div>
            <div class="metric-label">🎓 学历倾向</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # 职业详情
    st.markdown(f"""
    <div class="detail-list">
        <div class="detail-item">
            <div class="detail-icon"><i class="fas fa-directions"></i></div>
            <div class="detail-label">岗位方向</div>
            <div class="detail-value">{job_info['岗位属性与方向']}</div>
        </div>
        <div class="detail-item">
            <div class="detail-icon"><i class="fas fa-coins"></i></div>
            <div class="detail-label">薪资结构</div>
            <div class="detail-value">{job_info['薪资与薪资结构']}</div>
        </div>
        <div class="detail-item">
            <div class="detail-icon"><i class="fas fa-city"></i></div>
            <div class="detail-label">主要城市</div>
            <div class="detail-value">{job_info['主要就业城市']}</div>
        </div>
        <div class="detail-item">
            <div class="detail-icon"><i class="fas fa-building"></i></div>
            <div class="detail-label">典型企业</div>
            <div class="detail-value">{job_info['典型企业/机构']}</div>
        </div>
        <div class="detail-item">
            <div class="detail-icon"><i class="fas fa-users"></i></div>
            <div class="detail-label">适合人群</div>
            <div class="detail-value">{job_info['适合人群（含MBTI倾向）']}</div>
        </div>
        <div class="detail-item">
            <div class="detail-icon"><i class="fas fa-tools"></i></div>
            <div class="detail-label">技能要求</div>
            <div class="detail-value">{job_info['技能要求（具体）']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    
    # 关联证书推荐
    st.markdown("#### 🎓 关联证书推荐")
    st.markdown("点击下方证书可跳转到「证书导航」页面查看详情")
    
    # 根据当前职业查找关联证书
    related_certs = job_to_certs_map.get(selected_job, [])
    
    if related_certs:
        cert_cols = st.columns(min(len(related_certs), 4))
        for idx, cert in enumerate(related_certs[:4]):
            with cert_cols[idx % 4]:
                if st.button(f"🎓 {cert}", key=f"cert_from_job_{idx}"):
                    st.session_state.selected_cert_from_job = cert
                    st.session_state.jump_from_job_to_cert = True
                    st.session_state.nav_selected = "证书导航"
                    st.rerun()
        
        if len(related_certs) > 4:
            with st.expander(f"📋 查看更多关联证书（共{len(related_certs)}个）"):
                for idx, cert in enumerate(related_certs[4:]):
                    if st.button(f"🎓 {cert}", key=f"cert_from_job_more_{idx}"):
                        st.session_state.selected_cert_from_job = cert
                        st.session_state.jump_from_job_to_cert = True
                        st.session_state.nav_selected = "证书导航"
                        st.rerun()
    else:
        st.info("💡 暂无直接关联的证书，建议查看「证书导航」页面了解更多认证信息")


# 页面3：技能图谱
elif page == "技能图谱":

    st.markdown('<h2 style="text-align: center;"><i class="fas fa-project-diagram"></i> 技能关系图谱</h2>', unsafe_allow_html=True)

    skill_list = skill_df["技能"].unique().tolist()
    selected_skill = st.selectbox("🔍 选择核心技能查看关系图", skill_list)

    skill_data = skill_df[skill_df["技能"] == selected_skill]

    if len(skill_data) == 0:
        st.warning(f"未找到「{selected_skill}」的关联数据")
        st.stop()

    G = nx.Graph()
    G.add_node(selected_skill, type="skill")

    for _, row in skill_data.iterrows():
        course = row["来源课程"]
        job = row["对应岗位"]
        G.add_node(course, type="course")
        G.add_edge(course, selected_skill)
        G.add_node(job, type="job")
        G.add_edge(selected_skill, job)

    try:
# 使用更美观的布局
        if len(G.nodes()) <= 15:
            pos = nx.kamada_kawai_layout(G)
        else:
            pos = nx.spring_layout(G, seed=42, k=1.5, iterations=30)
    except:
        pos = nx.spring_layout(G, seed=42)

    node_x, node_y, node_text, node_color, node_sizes = [], [], [], [], []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
# 完全显示文字
        node_text.append(node)
        
        node_type = G.nodes[node]["type"]

        if node_type == "skill":
            node_color.append("#2A5C8A")  
            node_sizes.append(50)
        elif node_type == "course":
            node_color.append("#5BA0C8")  
            node_sizes.append(32)
        else:
            node_color.append("#E8A87C")  
            node_sizes.append(35)

    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        mode='lines',
        line=dict(width=1.5, color='#94A3B8'),
        hoverinfo='none'
    )

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="top center",
        textfont=dict(
            size=11,
            color="#1E2A3A",
            family="Microsoft YaHei, SimHei",
            weight="bold"
        ),
        hoverinfo='text',
        hovertext=node_text,
        marker=dict(
            size=node_sizes,
            color=node_color,
            line=dict(width=2, color='white'),
            opacity=0.9
        )
    )

# 动态计算坐标范围，确保文字完整显示
    if node_x:
        x_min, x_max = min(node_x), max(node_x)
        y_min, y_max = min(node_y), max(node_y)
# 根据节点数量动态调整边距
        node_count = len(node_x)
        if node_count <= 10:
            x_pad = max(0.8, (x_max - x_min) * 0.3)
            y_pad = max(0.8, (y_max - y_min) * 0.3)
        elif node_count <= 20:
            x_pad = max(0.5, (x_max - x_min) * 0.25)
            y_pad = max(0.5, (y_max - y_min) * 0.25)
        else:
            x_pad = max(0.3, (x_max - x_min) * 0.2)
            y_pad = max(0.3, (y_max - y_min) * 0.2)
        
        x_range = [x_min - x_pad, x_max + x_pad]
        y_range = [y_min - y_pad, y_max + y_pad]
    else:
        x_range = [-2, 2]
        y_range = [-2, 2]

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title=dict(
                text=f"✨ {selected_skill} 技能关系图谱",
                x=0.5,
                xanchor='center',
                font=dict(size=20, color="#2A5C8A", family="Microsoft YaHei", weight="bold")
            ),
            showlegend=False,
            hovermode='closest',
            margin=dict(b=80, l=80, r=80, t=100),  # 增大外边距
            height=750,  # 增加高度
            autosize=True,  # 自动调整大小
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                range=x_range,
                scaleanchor="y",  # 保持比例
                scaleratio=1
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                range=y_range
            ),
            annotations=[
                dict(
                    text="🔵 深蓝：核心技能 | 🔷 浅蓝：课程 | 🟠 橙色：岗位",
                    xref="paper", yref="paper", 
                    x=0.5, y=-0.12,
                    showarrow=False,
                    font=dict(size=12, color="#6B7A8A"),
                    align="center"
                )
            ]
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 查看技能关联详情"):
        st.dataframe(skill_data, use_container_width=True, hide_index=True)



        # 读取证书数据（使用你已有的Excel文件）
certificate_df = pd.read_excel(r"D:\Desktop\fintech-guide\data\证书表.xlsx")

# 补充证书间的关联关系数据
certificate_links = pd.DataFrame([
    # 格式: 源证书, 目标证书, 关联强度
    ("CQF", "Python数据分析", 0.8),
    ("CQF", "FRM", 0.7),
    ("CQF", "机器学习", 0.8),
    ("CFA", "FRM", 0.6),
    ("CFA", "FMVA®", 0.7),
    ("FRM", "SHMFTPP", 0.5),
    ("SHMFTPP", "银行金融科技基础", 0.6),
    ("机器学习", "DeepLearning.AI", 0.9),
    ("机器学习", "Kaggle", 0.7),
    ("DeepLearning.AI", "AI工程师", 0.7),
    ("Python数据分析", "Kaggle", 0.6),
    ("Python数据分析", "Tableau/Power BI", 0.5),
    ("CPA", "ACCA", 0.5),
    ("SOA", "中国精算师", 0.6),
])

# 定义路线图数据
roadmaps = {
    "金科量化路线": {
        "certificates": ["Python数据分析", "CQF", "机器学习", "Kaggle"],
        "description": "专注于量化交易、算法策略开发的路线",
        "careers": ["量化研究员", "算法交易工程师", "金融数据科学家"]
    },
    "风控专家路线": {
        "certificates": ["FRM", "Python数据分析", "SHMFTPP"],
        "description": "专注于金融风险管理、合规风控的路线",
        "careers": ["风控建模工程师", "反洗钱分析师", "金融风险管理师"]
    },
    "金融科技产品路线": {
        "certificates": ["SHMFTPP", "FMVA®", "银行金融科技基础"],
        "description": "专注于金融科技产品设计、业务分析的路线",
        "careers": ["金融产品经理", "商业分析师", "金融科技咨询顾问"]
    },
    "AI金融路线": {
        "certificates": ["机器学习", "DeepLearning.AI", "AI工程师", "Kaggle"],
        "description": "专注于AI在金融领域应用的路线",
        "careers": ["金融AI工程师", "金融数据科学家", "机器学习工程师"]
    },
    "数据分析路线": {
        "certificates": ["Python数据分析", "Tableau/Power BI", "Kaggle"],
        "description": "专注于金融数据分析、可视化的路线",
        "careers": ["数据分析师", "商业分析师", "数据科学家"]
    }
}


    # 页面4：证书导
if page == "证书导航":
    
    st.markdown('<h2><i class="fas fa-certificate"></i> 金融科技证书导航系统</h2>', unsafe_allow_html=True)
    
    # 创建标签页
    tab1, tab2, tab3, tab4 = st.tabs(["🌌 证书宇宙图", "🔍 证书深度画像", "🤖 AI证书推荐", "🗺️ 证书路线图"])
    
    # Tab 1: 证书宇宙图
    st.markdown("### 🌌 金融科技证书宇宙图")
    st.markdown('<p style="color: #6B7A8A; margin-bottom: 1rem;"><i class="fas fa-adjust"></i> 节点大小 = 含金量 | 🎨 节点颜色 = 难度 | 🔗 连线 = 证书关联性</p>', unsafe_allow_html=True)
    
    # 构建证书宇宙图
    G_cert = nx.Graph()
    center_node = "金融科技"
    G_cert.add_node(center_node)
    
    # 添加证书节点
    cert_node_data = {}
    for _, row in certificate_df.iterrows():
        cert_name = row["证书名称"]
        # 数值转换 - 增强健壮性
        try:
            difficulty = float(row["考试难度"]) if isinstance(row["考试难度"], (int, float)) else 5
        except:
            difficulty = 5
        
        try:
            value = float(row["含金量"]) if isinstance(row["含金量"], (int, float)) else 5
        except:
            value = 5
        
        G_cert.add_node(cert_name)
        G_cert.add_edge(center_node, cert_name)
        cert_node_data[cert_name] = {"difficulty": difficulty, "value": value}
    
    # 添加证书间的关联边 - 带错误处理
    try:
        if len(certificate_links) > 0 and "源证书" in certificate_links.columns:
            for _, link in certificate_links.iterrows():
                source = link["源证书"]
                target = link["目标证书"]
                weight = link["关联强度"] if "关联强度" in certificate_links.columns else 0.5
                
                if source in cert_node_data and target in cert_node_data:
                    G_cert.add_edge(source, target, weight=weight)
    except Exception as e:
        st.warning(f"添加证书关联时出现小问题（不影响查看）：{str(e)[:50]}")
    
    # 布局 - 添加异常处理
    try:
        pos = nx.spring_layout(G_cert, seed=42, k=1.2, iterations=50)
    except:
        pos = nx.circular_layout(G_cert)
    
    # 构建边轨迹
    edge_x, edge_y = [], []
    edge_weights = []
    for edge in G_cert.edges():
        try:
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        except:
            continue
    
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        mode='lines',
        line=dict(width=1, color='rgba(100,100,150,0.4)'),
        hoverinfo='none'
    )
    
    # 构建节点轨迹
    node_x, node_y, node_text, node_sizes, node_colors = [], [], [], [], []
    
    for node in G_cert.nodes():
        try:
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
        except:
            continue
        
        if node == center_node:
            node_text.append(f"<b>🎯 {node}</b><br>金融科技证书核心")
            node_sizes.append(50)
            node_colors.append(5)
        elif node in cert_node_data:
            data = cert_node_data[node]
            diff = data["difficulty"]
            val = data["value"]
            # 获取证书详情
            cert_row = certificate_df[certificate_df["证书名称"] == node]
            if len(cert_row) > 0:
                info = cert_row.iloc[0]
                hover_text = f"""
                <b>{node}</b><br>
                📚 核心名称：{info['核心名称']}<br>
                📂 分类：{info['分类']}<br>
                ⭐ 含金量：{val}/10<br>
                🎯 难度：{diff}/10<br>
                💰 费用：{info['考试费用']}<br>
                🚀 适合方向：{str(info['适合方向'])[:50]}...
                """
            else:
                hover_text = f"<b>{node}</b><br>⭐ 含金量: {val}/10<br>🎯 难度: {diff}/10"
            node_text.append(hover_text)
            node_sizes.append(max(15, min(50, val * 5)))  # 限制节点大小范围
            node_colors.append(diff)
        else:
            node_text.append(node)
            node_sizes.append(25)
            node_colors.append(5)
    
    # 确保有节点数据才绘图
    if len(node_x) > 0:
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            text=node_text,
            marker=dict(
                showscale=True,
                colorscale='RdYlBu_r',
                color=node_colors,
                size=node_sizes,
                colorbar=dict(title="考试难度", tickfont=dict(color="#1E2A3A")),
                line=dict(width=1.5, color='white'),
                sizemode='area',
                sizemin=12
            )
        )
        
        fig_cosmos = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                title=dict(text="✨ 金融科技证书生态系统", x=0.5, font=dict(size=18)),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=40, l=40, r=40, t=60),
                height=650,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                annotations=[
                    dict(
                        text="🔴 难度高 | 🔵 难度低 | 节点大小 = 含金量",
                        xref="paper", yref="paper",
                        x=0.5, y=-0.05,
                        showarrow=False,
                        font=dict(size=11, color="#6B7A8A")
                    )
                ]
            )
        )
        st.plotly_chart(fig_cosmos, use_container_width=True)
    else:
        st.warning("暂时无法生成证书宇宙图，请检查数据")
    
    # 图例说明
    col_legend1, col_legend2, col_legend3 = st.columns(3)
    with col_legend1:
        st.markdown("🔴 **高难度证书** (难度7-10)")
        st.markdown("🟡 **中等难度证书** (难度4-6)")
    with col_legend2:
        st.markdown("🔵 **低难度证书** (难度1-3)")
        st.markdown("📏 **节点越大 = 含金量越高**")
    with col_legend3:
        st.markdown("🔗 **连线 = 知识关联/推荐衔接**")
    
    #Tab 2: 证书深度画像
    with tab2:
        st.markdown("### 🔍 证书深度画像")
        
        cert_list = certificate_df["证书名称"].tolist()
        selected_cert = st.selectbox("🎯 选择证书查看深度画像", cert_list, key="cert_select")
        cert_info = certificate_df[certificate_df["证书名称"] == selected_cert].iloc[0]
        
        # 数值转换辅助函数
        def parse_rating(val):
            if isinstance(val, (int, float)):
                return val
            if isinstance(val, str):
                if "高" in val:
                    return 8
                if "中" in val:
                    return 5
                if "低" in val:
                    return 3
            return 5
        
        #基础信息卡（两列布局）
        st.markdown("#### 📋 基础信息卡")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            difficulty_raw = cert_info["考试难度"] if "考试难度" in cert_info else 5
            difficulty_val = difficulty_raw if isinstance(difficulty_raw, (int, float)) else parse_rating(difficulty_raw)
            st.markdown(f"""
            <div class="metric-item">
                <div class="metric-value">{difficulty_val}/10</div>
                <div class="metric-label">🎯 考试难度</div>
            </div>
            """, unsafe_allow_html=True)
            
            value_raw = cert_info["含金量"] if "含金量" in cert_info else 5
            value_val = value_raw if isinstance(value_raw, (int, float)) else parse_rating(value_raw)
            st.markdown(f"""
            <div class="metric-item">
                <div class="metric-value">{value_val}/10</div>
                <div class="metric-label">⭐ 含金量</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            cost_text = cert_info["考试费用"] if "考试费用" in cert_info else "待查"
            st.markdown(f"""
            <div class="metric-item">
                <div class="metric-value">{cost_text}</div>
                <div class="metric-label">💰 考试费用</div>
            </div>
            """, unsafe_allow_html=True)
            
            period_text = cert_info["备考周期"] if "备考周期" in cert_info else "待查"
            st.markdown(f"""
            <div class="metric-item">
                <div class="metric-value">{period_text}</div>
                <div class="metric-label">⏰ 备考周期</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            stage_text = cert_info["推荐年级"] if "推荐年级" in cert_info else "待查"
            st.markdown(f"""
            <div class="metric-item">
                <div class="metric-value">{stage_text}</div>
                <div class="metric-label">📚 推荐阶段</div>
            </div>
            """, unsafe_allow_html=True)
            
            cost_eff = cert_info["性价比评价"] if "性价比评价" in cert_info else "中"
            st.markdown(f"""
            <div class="metric-item">
                <div class="metric-value">{cost_eff}</div>
                <div class="metric-label">💎 性价比</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 雷达图
        st.markdown("#### 📊 能力维度雷达图")
        
        # 获取各维度数据
        math_req_raw = cert_info["数学要求"] if "数学要求" in cert_info else "中"
        math_val = parse_rating(math_req_raw)
        
        prog_req_raw = cert_info["编程要求"] if "编程要求" in cert_info else "中"
        prog_val = parse_rating(prog_req_raw)
        
        eng_req_raw = cert_info["英语要求"] if "英语要求" in cert_info else "中"
        eng_val = parse_rating(eng_req_raw)
        
        # 时间成本（根据备考周期估算）
        time_cost_map = {"1月": 2, "1-2月": 3, "2-3月": 4, "3-6月": 6, "6-9月": 7, "1年": 7, "1-1.5年": 7, "1-2年": 8, "2-3年": 8, "2.5-3年": 8, "3-5年": 9}
        period_str = cert_info["备考周期"] if "备考周期" in cert_info else "3-6月"
        time_cost = time_cost_map.get(period_str, 5)
        
        # 行业认可度
        industry_raw = cert_info["行业认可度"] if "行业认可度" in cert_info else "中"
        industry_val_map = {"入门": 3, "一般": 4, "中": 5, "中等": 5, "中高": 6, "高": 7, "极高": 8, "顶尖": 9}
        industry_val = industry_val_map.get(industry_raw, 5)
        
        radar_categories = ["数学要求", "编程要求", "英语要求", "时间成本", "行业认可"]
        radar_values = [math_val, prog_val, eng_val, time_cost, industry_val]
        
        radar_display = radar_categories + [radar_categories[0]]
        values_display = radar_values + [radar_values[0]]
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=values_display,
            theta=radar_display,
            fill='toself',
            line=dict(color="#2A5C8A", width=3),
            fillcolor='rgba(42,92,138,0.2)'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 10], gridcolor='#CBD5E1'),
                angularaxis=dict(tickfont=dict(size=12), gridcolor='#CBD5E1')
            ),
            showlegend=False,
            height=450,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
        
        st.markdown("---")
        
        #适合人群分析 
        st.markdown("#### 👥 适合人群分析")
        
        col_person1, col_person2 = st.columns(2)
        
        with col_person1:
            mbti_text = cert_info["适合人群"] if "适合人群" in cert_info else "各类型"
            st.markdown(f"""
            <div class="detail-list">
                <div class="detail-item">
                    <div class="detail-icon"><i class="fas fa-brain"></i></div>
                    <div class="detail-label">MBTI倾向</div>
                    <div class="detail-value">{mbti_text}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_person2:
            # 根据证书特点生成性格描述
            if value_val >= 8:
                personality_desc = "✅ 适合追求高回报、愿意付出长期努力的同学<br>✅ 抗压能力强，有明确职业规划"
            elif difficulty_val >= 7:
                personality_desc = "✅ 适合学习能力强、有毅力的同学<br>✅ 建议有扎实的专业基础"
            else:
                personality_desc = "✅ 适合希望快速获得认证、增强简历的同学<br>✅ 入门级证书，各年级均可考虑"
            st.markdown(f"""
            <div class="detail-list">
                <div class="detail-item">
                    <div class="detail-icon"><i class="fas fa-user-check"></i></div>
                    <div class="detail-label">性格特征</div>
                    <div class="detail-value">{personality_desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 对应职业联动
        st.markdown("#### 💼 对应职业联动")
        
        # 从证书的"对应岗位"字段解析职业
        jobs_text = cert_info["对应岗位"] if "对应岗位" in cert_info else ""
        related_jobs = [j.strip() for j in jobs_text.split("、") if j.strip()] if jobs_text else ["数据分析师", "风控建模工程师", "金融科技产品经理"]
        
        # 显示相关职业
        job_cols = st.columns(min(len(related_jobs), 4))
        for idx, job in enumerate(related_jobs[:4]):
            with job_cols[idx % 4]:
                st.markdown(f"""
                <div style="background: #F5F7FA; border-radius: 12px; padding: 12px; text-align: center; margin: 5px;">
                    <i class="fas fa-briefcase" style="font-size: 1.5rem; color: #2A5C8A;"></i>
                    <div style="font-weight: 500; margin-top: 5px;">{job}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # 从职业表查找更多关联
        st.markdown("##### 📌 典型岗位详解")
        for job in related_jobs[:2]:
            job_match = job_df[job_df["岗位"].str.contains(job[:4], na=False)]
            if len(job_match) > 0:
                job_info_match = job_match.iloc[0]
                with st.expander(f"🔍 {job} 岗位详情"):
                    st.markdown(f"""
                    - **岗位方向**：{job_info_match.get('岗位属性与方向', '待补充')}
                    - **薪资范围**：{job_info_match.get('薪资与薪资结构', '待补充')}
                    - **主要城市**：{job_info_match.get('主要就业城市', '待补充')}
                    - **技能要求**：{job_info_match.get('技能要求（具体）', '待补充')[:150]}...
                    """)
        
        st.markdown("---")
        
        # 企业认可
        st.markdown("#### 🏢 企业认可度")
        
        company_text = cert_info["典型企业认可"] if "典型企业认可" in cert_info else "各大金融机构"
        
        st.markdown(f"""
        <div class="detail-list">
            <div class="detail-item">
                <div class="detail-icon"><i class="fas fa-building"></i></div>
                <div class="detail-label">典型认可企业</div>
                <div class="detail-value">{company_text}</div>
            </div>
            <div class="detail-item">
                <div class="detail-icon"><i class="fas fa-chart-line"></i></div>
                <div class="detail-label">行业认可度</div>
                <div class="detail-value">{cert_info['行业认可度'] if '行业认可度' in cert_info else '中'}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 行业认可度进度条
        industry_score = industry_val_map.get(cert_info.get('行业认可度', '中'), 5)
        st.progress(industry_score / 10)
        st.caption(f"行业认可评分：{industry_score}/10")
    
    #Tab 3: AI证书推荐
    with tab3:
        st.markdown("### 🤖 AI智能证书推荐系统")
        st.markdown('<p style="color: #6B7A8A; margin-bottom: 1rem;">根据你的兴趣、性格和职业目标，AI为你智能匹配最优证书路线</p>', unsafe_allow_html=True)
        
        # 用户输入表单
        with st.form("ai_recommend_form"):
            st.markdown("#### 📝 请填写你的信息")
            
            col_interest1, col_interest2, col_interest3 = st.columns(3)
            with col_interest1:
                like_finance = st.selectbox("💹 喜欢金融", ["是", "一般", "否"])
            with col_interest2:
                like_math = st.selectbox("📐 喜欢数学", ["是", "一般", "否"])
            with col_interest3:
                like_programming = st.selectbox("💻 喜欢编程", ["是", "一般", "否"])
            
            col_mbti1, col_mbti2 = st.columns(2)
            with col_mbti1:
                mbti_type = st.selectbox("🧠 你的MBTI类型", 
                    ["INTJ", "INTP", "ENTJ", "ENTP", "ISTJ", "ESTJ", "INFJ", "ENFJ", "其他"])
            with col_mbti2:
                mbti_desc = st.text_input("补充说明（可选）", placeholder="例如：喜欢独立工作...")
            
            col_goal1, col_goal2, col_goal3 = st.columns(3)
            with col_goal1:
                goal_high_salary = st.checkbox("💰 高薪")
            with col_goal2:
                goal_stable = st.checkbox("🏛️ 稳定")
            with col_goal3:
                goal_ai = st.checkbox("🤖 AI方向")
            
            submitted = st.form_submit_button("🎯 开始AI推荐", use_container_width=True, type="primary")
        
        if submitted:
            st.markdown("---")
            st.markdown("#### 🎯 AI推荐结果")
            
            # 构建用户画像
            user_profile = {
                "fin_interest": like_finance,
                "math_interest": like_math,
                "prog_interest": like_programming,
                "mbti": mbti_type,
                "goals": []
            }
            if goal_high_salary:
                user_profile["goals"].append("high_salary")
            if goal_stable:
                user_profile["goals"].append("stable")
            if goal_ai:
                user_profile["goals"].append("ai")
            
            # 推荐逻辑
            recommendations = []
            
            # 量化路线推荐
            if like_math == "是" and like_programming == "是":
                recommendations.append({
                    "route": "金科量化路线",
                    "certificate": "CQF",
                    "reason": "你对数学和编程都有兴趣，非常适合量化金融方向。CQF是量化圈的硬通货，能系统性地提升你的量化建模能力。",
                    "score": 95
                })
                recommendations.append({
                    "route": "AI金融路线",
                    "certificate": "机器学习认证",
                    "reason": "结合你的编程兴趣，AI+金融是当前最热门的赛道，机器学习认证能帮你打下坚实的技术基础。",
                    "score": 88
                })
            
            # 金融+稳定方向
            if like_finance == "是" and goal_stable:
                recommendations.append({
                    "route": "风控专家路线",
                    "certificate": "FRM",
                    "reason": "你喜欢金融且有稳定目标，FRM在银行风控岗认可度极高，职业路径清晰稳定。",
                    "score": 90
                })
                if mbti_type in ["ISTJ", "ESTJ"]:
                    recommendations[-1]["reason"] += " 你的MBTI类型(ISTJ/ESTJ)非常适合风控这类需要细致严谨的岗位。"
            
            # 产品/业务方向
            if like_finance == "是" and like_programming != "是" and mbti_type in ["ENTJ", "ENFJ", "ENTP"]:
                recommendations.append({
                    "route": "金融科技产品路线",
                    "certificate": "SHMFTPP",
                    "reason": "你有金融兴趣和良好的沟通特质，SHMFTPP是金融科技产品岗的利器，性价比极高。",
                    "score": 85
                })
            
            # AI方向专门推荐
            if goal_ai:
                recommendations.append({
                    "route": "AI金融路线",
                    "certificate": "DeepLearning.AI",
                    "reason": "目标AI方向推荐深度学习专项，这是入门深度学习的黄金课程，由吴恩达主讲。",
                    "score": 92
                })
            
            # 默认推荐
            if len(recommendations) == 0:
                recommendations = [
                    {"route": "数据分析路线", "certificate": "Python数据分析", "reason": "入门友好，就业面广，适合作为基础技能补充。", "score": 80},
                    {"route": "金科量化路线", "certificate": "CQF", "reason": "挑战与回报并存，适合想走高端路线的同学。", "score": 75}
                ]
            
            # 按分数排序
            recommendations.sort(key=lambda x: x["score"], reverse=True)
            
            # 展示推荐结果
            for rec in recommendations[:3]:
                with st.container():
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #F0F4F8, #FFFFFF); border-radius: 16px; padding: 1.2rem; margin-bottom: 1rem; border-left: 4px solid #2A5C8A;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <span style="font-size: 1.2rem; font-weight: 700;">🏆 {rec['certificate']}</span>
                                <span style="margin-left: 10px; background: #2A5C8A; color: white; padding: 2px 10px; border-radius: 20px; font-size: 0.7rem;">{rec['route']}</span>
                            </div>
                            <span style="color: #2A5C8A; font-weight: 700;">匹配度 {rec['score']}%</span>
                        </div>
                        <div style="margin-top: 10px; color: #1E2A3A;">💡 {rec['reason']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # 详细路线解释
            st.markdown("---")
            st.markdown("#### 📖 为什么推荐这些路线？")
            
            rec_certs = [rec['certificate'] for rec in recommendations[:3]]
            for cert_name in rec_certs:
                cert_row = certificate_df[certificate_df["证书名称"] == cert_name]
                if len(cert_row) > 0:
                    cert = cert_row.iloc[0]
                    st.markdown(f"""
                    <div style="margin-bottom: 1rem;">
                        <strong>📌 {cert_name} — {cert['核心名称']}</strong><br>
                        • 适合方向：{cert['适合方向']}<br>
                        • 推荐年级：{cert['推荐年级']} | 难度：{cert['考试难度']}/10 | 含金量：{cert['含金量']}/10<br>
                        • 备考建议：{cert['备考周期']}，费用{cert['考试费用']}
                    </div>
                    """, unsafe_allow_html=True)
            
            # 个性化建议
            st.info(f"""
            💡 **个性化建议**：基于你的MBTI类型“{mbti_type}”：
            - {"INTJ/INTP类型适合量化、算法研究类证书" if mbti_type in ["INTJ", "INTP"] else ""}
            - {"ENTJ/ENTP类型适合金融产品、管理咨询类证书" if mbti_type in ["ENTJ", "ENTP"] else ""}
            - {"ISTJ/ESTJ类型适合风控、会计审计类证书" if mbti_type in ["ISTJ", "ESTJ"] else ""}
            - 建议结合大二大三的课程安排，合理规划备考时间，避免与期末考试冲突。
            """)
    
        #Tab 4: 证书路线图 
    with tab4:
        st.markdown("### 🗺️ 金融科技证书路线图")
        st.markdown('<p style="color: #6B7A8A; margin-bottom: 1rem;">选择你的职业发展路线，查看对应的证书规划和时间安排</p>', unsafe_allow_html=True)
        
        # 路线选择
        route_names = list(roadmaps.keys())
        selected_route = st.selectbox("🎯 选择发展路线", route_names)
        
        route_data = roadmaps[selected_route]
        
        st.markdown(f"#### {selected_route}")
        st.markdown(f"📝 **路线说明**：{route_data['description']}")
        
        # 创建两列布局
        col_route1, col_route2 = st.columns([2, 1])
        
        with col_route1:
            st.markdown("##### 📅 证书学习时间线")
            
            # 使用 st.markdown 逐条显示，避免复杂的 HTML 拼接
            for cert in route_data["certificates"]:
                # 获取证书详细信息
                cert_row = certificate_df[certificate_df["证书名称"] == cert]
                
                if len(cert_row) > 0:
                    difficulty = cert_row.iloc[0]["考试难度"]
                    value = cert_row.iloc[0]["含金量"]
                    core_name = cert_row.iloc[0]["核心名称"]
                    
                    # 转换为数值（处理可能的字符串）
                    try:
                        diff_num = float(difficulty) if isinstance(difficulty, (int, float)) else 5
                    except:
                        diff_num = 5
                    
                    try:
                        val_num = float(value) if isinstance(value, (int, float)) else 5
                    except:
                        val_num = 5
                    
                    # 确定推荐年级
                    grade = cert_row.iloc[0]["推荐年级"] if "推荐年级" in cert_row.columns else "大二/大三"
                    # 提取年级（如"大一（一级）" -> "大一"）
                    if "大一" in str(grade):
                        show_grade = "大一"
                    elif "大二" in str(grade):
                        show_grade = "大二"
                    elif "大三" in str(grade):
                        show_grade = "大三"
                    else:
                        show_grade = str(grade)[:4] if len(str(grade)) > 4 else str(grade)
                    
                    # 使用 st.container 和 st.columns 替代 HTML
                    with st.container():
                        cols = st.columns([1, 3, 1])
                        with cols[0]:
                            st.markdown(f"**{show_grade}**")
                        with cols[1]:
                            st.markdown(f"🏅 **{cert}**")
                            st.caption(f"{core_name} | 难度 {diff_num}/10 | 含金量 {val_num}/10")
                        with cols[2]:
                            st.markdown("➡️")
                        st.markdown("---")
                else:
                    # 如果证书不在数据中，简单显示
                    with st.container():
                        cols = st.columns([1, 3, 1])
                        with cols[0]:
                            st.markdown("**待定**")
                        with cols[1]:
                            st.markdown(f"🏅 **{cert}**")
                        with cols[2]:
                            st.markdown("➡️")
                        st.markdown("---")
        
        with col_route2:
            st.markdown("##### 🎯 对应职业")
            for career in route_data["careers"]:
                st.markdown(f"""
                <div style="background: white; border-radius: 12px; padding: 10px; margin-bottom: 8px; border-left: 3px solid #2A5C8A;">
                    💼 {career}
                </div>
                """, unsafe_allow_html=True)
            
            # 添加路线特点
            st.markdown("---")
            st.markdown("##### ✨ 路线特点")
            if "量化" in selected_route:
                st.markdown("- 薪资天花板高")
                st.markdown("- 需要强数理编程背景")
                st.markdown("- 适合喜欢挑战的同学")
            elif "风控" in selected_route:
                st.markdown("- 职业稳定性强")
                st.markdown("- 银行/金融机构需求大")
                st.markdown("- 适合细致严谨的同学")
            elif "产品" in selected_route:
                st.markdown("- 沟通协调能力重要")
                st.markdown("- 成长路径清晰")
                st.markdown("- 适合综合能力强同学")
            elif "AI" in selected_route:
                st.markdown("- 技术前沿方向")
                st.markdown("- 需要持续学习")
                st.markdown("- 薪资增长空间大")
            else:
                st.markdown("- 入门友好")
                st.markdown("- 就业面广")
                st.markdown("- 适合技能补充")
        
        st.markdown("---")
        
        # 其他路线快速预览
        st.markdown("##### 🔄 其他推荐路线")
        other_routes = [r for r in route_names if r != selected_route]
        
        # 使用 columns 创建按钮式选择
        route_cols = st.columns(min(len(other_routes), 4))
        for idx, route in enumerate(other_routes[:4]):
            with route_cols[idx % 4]:
                if st.button(route, key=f"route_btn_{idx}"):
                    st.session_state.selected_route = route
                    st.rerun()
        
        # 路线组合建议
        st.markdown("---")
        st.markdown("##### 💡 路线组合建议")
        
        advice_map = {
            "金科量化路线": "💡 量化路线建议：大二掌握Python和数学基础 → 大三报考CQF → 同步参与Kaggle竞赛积累实战经验 → 大四准备量化私募/券商实习面试",
            "风控专家路线": "💡 风控路线建议：大二学习概率统计和FRM一级 → 大三报考FRM二级 → 同时学习Python数据分析 → 大四申请银行/互金风控岗位",
            "金融科技产品路线": "💡 产品路线建议：大二了解金融科技基础 → 大三考取SHMFTPP一级 → 参与金融科技比赛/项目 → 大四申请产品经理实习",
            "AI金融路线": "💡 AI金融路线建议：大二打好Python和数学基础 → 大三系统学习机器学习 → 参与Kaggle竞赛 → 大四准备AI金融岗位",
            "数据分析路线": "💡 数据分析路线建议：大二考取Python数据分析认证 → 学习Tableau/Power BI → 大三参与数据分析项目 → 大四申请数据分析实习"
        }
        
        st.info(advice_map.get(selected_route, "💡 建议根据个人兴趣和职业目标，选择合适的证书组合，循序渐进地备考。"))
        
        # 添加温馨提示
        st.markdown("---")
        st.caption("📌 温馨提示：以上路线仅供参考，请结合个人实际情况和学校课程安排合理规划。证书备考需要长期坚持，建议循序渐进。")# ==================== 页面3：技能图谱 ====================
