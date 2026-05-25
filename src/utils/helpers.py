"""
工具函数
"""


import streamlit as st

def load_css():
    """加载CSS样式"""
    st.markdown("""
    <style>
    /* 引入 Font Awesome 图标库 */
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');
    
    /* 主题色定义 */
    /* 主色调: #2A5C8A */
    /* 辅色调: #5BA0C8 */
    /* 浅色调: #C0D9E8 */
    
    /* 全局背景 */
    .stApp {
        background: linear-gradient(135deg, #F5F7FA 0%, #E8EEF5 100%);
    }
    
    /* ========== 全局文字颜色设置 ========== */
    .stApp, .main, .block-container {
        color: #1E2A3A !important;
    }
    
    /* 所有标题颜色 */
    h1, h2, h3, h4, h5, h6 {
        color: #2A5C8A !important;
    }
    
    /* 所有标签文字 */
    label, .stSelectbox label, .stTextInput label, .stTextArea label {
        color: #1E2A3A !important;
        font-weight: 500 !important;
    }
    
    /* 隐藏默认的侧边栏折叠按钮 */
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
    
    /* ========== Selectbox 下拉框 - 白色背景，深色文字 ========== */
    .stSelectbox label {
        color: #1E2A3A !important;
        font-weight: 500 !important;
    }
    .stSelectbox div[data-baseweb="select"] {
        background-color: white !important;
        border-radius: 8px !important;
        border: 1px solid #D1D5DB !important;
    }
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: white !important;
        color: #1E2A3A !important;
        font-weight: 500 !important;
    }
    /* 选中的值文字颜色 */
    .stSelectbox div[data-baseweb="select"] div[role="button"] span {
        color: #1E2A3A !important;
        font-weight: 500 !important;
    }
    .stSelectbox svg {
        fill: #2A5C8A !important;
    }
    
    /* 下拉菜单选项 - 白色背景，深色文字 */
    div[data-baseweb="popover"] ul {
        background-color: white !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="popover"] li {
        color: #1E2A3A !important;
        background-color: white !important;
        font-weight: 500 !important;
    }
    div[data-baseweb="popover"] li:hover {
        background-color: #C0D9E8 !important;
    }
    div[data-baseweb="popover"] li[aria-selected="true"] {
        background-color: #2A5C8A !important;
        color: white !important;
    }
    
        /* ========== SelectSlider 滑块样式 ========== */
    .stSlider label {
        color: #1E2A3A !important;
        font-weight: 500 !important;
    }
    /* 滑块选中的值文字 */
    .stSlider div[data-testid="stMarkdownContainer"] p {
        color: #1E2A3A !important;
        font-weight: 500 !important;
    }
    
    /* 滑块已选中的部分 - 主题色 */
    .stSlider div[data-baseweb="slider"] div[data-testid="stSliderThumb"] {
        background-color: #2A5C8A !important;
        border: 2px solid white !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2) !important;
    }
    /* 滑块轨道已填充部分 */
    .stSlider div[data-baseweb="slider"] div[role="slider"] + div {
        background-color: #2A5C8A !important;
    }
    /* 滑块数值显示框 - 白色背景 */
    .stSlider [data-testid="stSliderTickBar"] {
        background-color: transparent !important;
    }
    /* 滑块数值标记 */
    .stSlider .stMarkdown {
        color: #1E2A3A !important;
    }
    
    /* ========== TextArea 文本框 - 白色背景 ========== */
    .stTextArea textarea {
        background-color: white !important;
        color: #1E2A3A !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 8px !important;
        font-size: 14px !important;
    }
    .stTextArea textarea:focus {
        border-color: #2A5C8A !important;
        box-shadow: 0 0 0 2px rgba(42,92,138,0.2) !important;
    }
    .stTextArea textarea::placeholder {
        color: #9CA3AF !important;
    }
    
    /* ========== TextInput 输入框 - 白色背景 ========== */
    .stTextInput input {
        background-color: white !important;
        color: #1E2A3A !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 8px !important;
        font-size: 14px !important;
    }
    .stTextInput input:focus {
        border-color: #2A5C8A !important;
        box-shadow: 0 0 0 2px rgba(42,92,138,0.2) !important;
    }
    .stTextInput input::placeholder {
        color: #9CA3AF !important;
    }
    
    /* ========== NumberInput 输入框 - 白色背景 ========== */
    .stNumberInput input {
        background-color: white !important;
        color: #1E2A3A !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 8px !important;
    }
    
    /* ========== MultiSelect 多选框 - 白色背景 ========== */
    .stMultiSelect div[data-baseweb="select"] {
        background-color: white !important;
        border-radius: 8px !important;
        border: 1px solid #D1D5DB !important;
    }
    .stMultiSelect div[data-baseweb="select"] div {
        background-color: white !important;
        color: #1E2A3A !important;
    }
    
    /* ========== DateInput 日期输入框 - 白色背景 ========== */
    .stDateInput input {
        background-color: white !important;
        color: #1E2A3A !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 8px !important;
    }
    
    /* ========== TimeInput 时间输入框 - 白色背景 ========== */
    .stTimeInput input {
        background-color: white !important;
        color: #1E2A3A !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 8px !important;
    }
    
    /* ========== 复选框样式 ========== */
    .stCheckbox label span {
        color: #1E2A3A !important;
    }
    .stCheckbox label span[data-baseweb="checkbox"] {
        border-color: #2A5C8A !important;
    }
    
    /* ========== 单选框样式 ========== */
    .stRadio label span {
        color: #1E2A3A !important;
    }
    
    /* ========== 主标题样式 ========== */
    .main-title {
        text-align: center;
        margin-top: 20px;
        margin-bottom: 0.5rem;
    }
    .main-title h1 {
        background: linear-gradient(135deg, #2A5C8A, #5BA0C8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        display: inline-block;
        margin-bottom: 0;
    }
    
    /* 副标题英文 */
    .sub-title {
        text-align: center;
        color: #5BA0C8 !important;
        font-size: 0.9rem;
        letter-spacing: 2px;
        margin-top: -0.2rem;
        margin-bottom: 1rem;
    }
    
    /* 标签栏 */
    .badge-container {
        text-align: center;
        margin-bottom: 1rem;
    }
    .badge {
        display: inline-block;
        padding: 5px 16px;
        background: rgba(42,92,138,0.1);
        color: #2A5C8A !important;
        border-radius: 30px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 0 6px;
    }
    .badge i {
        margin-right: 6px;
    }
    
    /* ========== 详情卡片样式 ========== */
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
        color: #1E2A3A !important;
    }
    .detail-value {
        flex: 1;
        color: #1E2A3A !important;
    }
    
    /* ========== 指标卡片样式 ========== */
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
        color: #2A5C8A !important;
    }
    .metric-label {
        font-size: 0.75rem;
        color: #5BA0C8 !important;
        margin-top: 0.3rem;
    }
    
    /* ========== 进度条美化 ========== */
    .stProgress > div > div {
        background-color: #2A5C8A !important;
        border-radius: 10px;
    }
    .stProgress > div {
        background-color: #E2E8F0 !important;
        border-radius: 10px;
    }
    
    /* ========== 信息框美化 ========== */
    .stAlert {
        border-radius: 16px !important;
        border-left: 4px solid #2A5C8A !important;
        background-color: #FFFFFF !important;
    }
    .stAlert p {
        color: #1E2A3A !important;
    }
    
    /* ========== 分割线 ========== */
    hr {
        margin: 1.5rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #2A5C8A, transparent);
    }
    
    /* ========== 指标卡片 ========== */
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
    [data-testid="stMetricLabel"] {
        color: #5BA0C8 !important;
    }
    
    /* ========== 白色卡片 ========== */
    .white-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
    }
    .white-card p, .white-card div {
        color: #1E2A3A !important;
    }
    
    /* ========== 按钮样式 ========== */
    .stButton button {
        font-weight: 500 !important;
        border-radius: 8px !important;
        border: none !important;
    }
    .stButton button[kind="primary"] {
        background-color: #2A5C8A !important;
        color: white !important;
    }
    .stButton button[kind="primary"]:hover {
        background-color: #1A4C7A !important;
    }
    .stButton button[kind="secondary"] {
        background-color: #C0D9E8 !important;
        color: #1E2A3A !important;
    }
    .stButton button[kind="secondary"]:hover {
        background-color: #A8C8D8 !important;
        color: #1E2A3A !important;
    }
    
    /* ========== 数据表格样式 ========== */
    .stDataFrame, .dataframe {
        color: #1E2A3A !important;
        background-color: white !important;
    }
    .stDataFrame td, .dataframe td {
        color: #1E2A3A !important;
        background-color: white !important;
    }
    .stDataFrame th, .dataframe th {
        color: #2A5C8A !important;
        font-weight: 600 !important;
        background-color: #F5F7FA !important;
    }
    
    /* ========== Expander 样式 ========== */
    .streamlit-expanderHeader {
        color: #2A5C8A !important;
        font-weight: 500 !important;
        background-color: #F5F7FA !important;
        border-radius: 8px !important;
    }
    .streamlit-expanderContent {
        color: #1E2A3A !important;
        background-color: white !important;
    }
    
    /* ========== 移动端适配 ========== */
    @media (max-width: 768px) {
        .main-title h1 {
            font-size: 1.8rem !important;
        }
        .badge {
            font-size: 0.7rem;
            padding: 3px 10px;
        }
    }
    
    /* ========== Tab 标签页样式 ========== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F5F7FA;
        border-radius: 12px;
        padding: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 16px;
        color: #2A5C8A !important;
        background-color: transparent !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2A5C8A !important;
        color: white !important;
    }
    
    /* ========== 快捷标签按钮样式 ========== */
    .quick-tag-btn {
        background-color: #C0D9E8 !important;
        color: #2A5C8A !important;
        border: 1px solid #2A5C8A !important;
        border-radius: 20px !important;
        padding: 5px 12px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
    }
    .quick-tag-btn:hover {
        background-color: #2A5C8A !important;
        color: white !important;
    }
    
    /* ========== 滑块数值显示样式 ========== */
    .stSlider [data-testid="stMarkdownContainer"] p {
        color: #1E2A3A !important;
        font-weight: 500 !important;
        font-size: 14px !important;
    }
    
    /* ========== 数字输入框数值样式 ========== */
    .stNumberInput [data-testid="stMarkdownContainer"] p {
        color: #1E2A3A !important;
    }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """渲染页面头部"""
    st.markdown("""
    <div class="main-title">
        <h1><i class="fas fa-graduation-cap"></i> 湖南大学金融科技专业导航系统</h1>
    </div>
    <div class="sub-title">Hunan University FinTech Navigation System</div>
    <div class="badge-container">
        <span class="badge"><i class="fas fa-robot"></i> AI智能导航</span>
        <span class="badge"><i class="fas fa-chart-line"></i> 实时数据</span>
        <span class="badge"><i class="fas fa-bullseye"></i> 职业匹配</span>
        <span class="badge"><i class="fas fa-chart-pie"></i> 技能分析</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

def init_session():
    """初始化 session state"""
    if "nav_selected" not in st.session_state:
        st.session_state.nav_selected = "课程地图"
    if "selected_job" not in st.session_state:
        st.session_state.selected_job = None
    if "selected_cert" not in st.session_state:
        st.session_state.selected_cert = None
    if "jump_from_cert" not in st.session_state:
        st.session_state.jump_from_cert = False
    if "jump_from_job" not in st.session_state:
        st.session_state.jump_from_job = False
    if "show_sidebar" not in st.session_state:
        st.session_state.show_sidebar = True
    if "search_input" not in st.session_state:
        st.session_state.search_input = ""