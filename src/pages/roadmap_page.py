"""
成长路线定制页面
"""


import streamlit as st
import pandas as pd
from src.utils.data_loader import load_job_data, load_cert_data, safe_get

def render():
    st.markdown('<div class="page-shell">', unsafe_allow_html=True)

    job_df = load_job_data()
    cert_df = load_cert_data()

    st.markdown("""
    <div class="page-hero">
        <div class="hero-grid">
            <div>
                <div class="section-kicker">Roadmap workspace</div>
                <h2>专业成长路线定制</h2>
                <p class="section-caption">结合目标岗位、能力基础、时间预算与行业偏好，生成更像成长规划台的阶段化路线展示。</p>
                <div class="tag-row" style="margin-top:0.9rem;">
                    <span class="tag tag-primary">阶段路线</span>
                    <span class="tag tag-success">技能面板</span>
                    <span class="tag tag-accent">证书规划</span>
                </div>
            </div>
            <div class="panel-card">
                <div class="eyebrow-text">Planning logic</div>
                <div class="card-title">保留原有推荐逻辑，仅重构展示叙事</div>
                <div class="card-caption">先完成输入，再把结果拆成阶段、技能、证书、建议与资源五个面板，减少一次性文本堆叠。</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="form-shell form-panel content-fade">', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        <div class="section-kicker">Planner input</div>
        <div class="section-title">路线规划输入区</div>
        <p class="section-caption">按目标、能力与资源三组信息填写，帮助系统生成更贴近实际的学习与考证安排。</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="interactive-surface" style="padding:1rem;">', unsafe_allow_html=True)
        st.markdown('<div class="eyebrow-text" style="margin-bottom:0.5rem;">目标与能力</div>', unsafe_allow_html=True)
        career_goal = st.selectbox("职业目标", ["量化交易", "风险管理", "金融产品", "AI开发", "数据分析", "不确定"])
        math_level = st.select_slider("数学能力", ["较弱", "一般", "较强", "很强"])
        prog_level = st.select_slider("编程能力", ["无基础", "基础", "熟练", "精通"])
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="interactive-surface" style="padding:1rem;">', unsafe_allow_html=True)
        st.markdown('<div class="eyebrow-text" style="margin-bottom:0.5rem;">时间与偏好</div>', unsafe_allow_html=True)
        available_time = st.select_slider("每周可投入时间", ["<5小时", "5-10小时", "10-20小时", ">20小时"])
        target_time = st.selectbox("目标考证时间", ["3个月内", "6个月内", "1年内", "2年内"])
        preferred_industry = st.multiselect("偏好行业", ["银行", "证券/基金", "保险", "互联网金融", "金融科技公司", "咨询"])
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="section-header" style="margin-top:0.4rem;">
        <div class="section-title">性格 / 偏好标签</div>
        <p class="section-caption">可多选，用于微调方向与建议内容。</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="choice-matrix preference-grid">', unsafe_allow_html=True)
    personality_cols = st.columns(4)
    personality_options = ["喜欢钻研", "喜欢与人沟通", "追求稳定", "喜欢挑战", "注重细节", "有创造力", "逻辑性强", "抗压能力强"]
    selected_personality = []

    for idx, opt in enumerate(personality_options):
        with personality_cols[idx % 4]:
            if st.checkbox(opt, key=f"person_{idx}"):
                selected_personality.append(opt)
    st.markdown('</div>', unsafe_allow_html=True)

    generate_btn = st.button("生成我的成长路线", use_container_width=True, type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

    if generate_btn:
        if career_goal == "量化交易" or (math_level in ["较强", "很强"] and prog_level in ["熟练", "精通"]):
            direction = "quant"
            direction_name = "金科量化路线"
            certs = ["Python数据分析", "CQF", "机器学习", "Kaggle"]
            skills = ["Python编程", "概率统计", "随机过程", "金融工程", "机器学习"]
            courses = ["程序设计", "概率论与数理统计", "随机过程", "金融工程学A", "金融机器学习R"]

        elif career_goal == "风险管理" or "稳定" in selected_personality:
            direction = "risk"
            direction_name = "风控专家路线"
            certs = ["FRM", "Python数据分析", "SHMFTPP"]
            skills = ["Python编程", "SQL", "统计学", "信用风险建模", "反欺诈"]
            courses = ["概率论与数理统计", "金融风险管理E", "机器学习", "大数据分析"]

        elif career_goal == "金融产品" or "喜欢与人沟通" in selected_personality:
            direction = "product"
            direction_name = "金融科技产品路线"
            certs = ["SHMFTPP", "FMVA®", "银行金融科技基础"]
            skills = ["金融科技通识", "产品设计", "需求分析", "商业分析", "项目管理"]
            courses = ["金融科技概论", "银行数字化转型", "金融科技创新与监管"]

        elif career_goal == "AI开发" or ("喜欢挑战" in selected_personality and prog_level in ["熟练", "精通"]):
            direction = "ai"
            direction_name = "AI金融路线"
            certs = ["机器学习", "DeepLearning.AI", "AI工程师", "Kaggle"]
            skills = ["Python编程", "机器学习", "深度学习", "LLM应用", "PyTorch/TensorFlow"]
            courses = ["机器学习", "大语言模型的金融应用", "深度学习", "数据结构"]

        else:
            direction = "data"
            direction_name = "数据分析路线"
            certs = ["Python数据分析", "Tableau/Power BI", "Kaggle"]
            skills = ["Python编程", "SQL", "数据可视化", "统计学", "业务分析"]
            courses = ["程序设计", "概率论与数理统计", "大数据分析与挖掘"]

        if target_time == "3个月内":
            certs = certs[:1]
        elif target_time == "6个月内":
            certs = certs[:2]

        st.markdown('<div class="roadmap-board content-fade">', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="roadmap-summary">
            <div class="card-title-row">
                <div>
                    <div class="section-kicker">Roadmap generated</div>
                    <div class="section-title">{direction_name}</div>
                </div>
                <span class="tag tag-success">{target_time}</span>
            </div>
            <div class="card-caption">系统已基于职业目标、能力基础、时间窗口和偏好标签生成阶段化路线。</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-strip">
            <div class="metric-item">
                <div class="metric-label">Primary direction</div>
                <div class="metric-value">{direction_name}</div>
                <div class="metric-note">当前最匹配的发展主线</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Time window</div>
                <div class="metric-value">{target_time}</div>
                <div class="metric-note">目标考证节奏</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Skill posture</div>
                <div class="metric-value">{math_level} / {prog_level}</div>
                <div class="metric-note">数学与编程基础组合</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Industry preference</div>
                <div class="metric-value">{len(preferred_industry) if preferred_industry else 0}</div>
                <div class="metric-note">已选择的行业偏好数量</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="section-shell">
            <div class="card-title-row">
                <div>
                    <div class="section-kicker">Direction thesis</div>
                    <div class="section-title">{direction_name}</div>
                </div>
                <span class="tag tag-primary">推荐方向</span>
            </div>
            <div class="card-caption">基于你的输入，当前更适合先沿这条路径构建课程、技能与证书组合。</div>
        </div>
        """, unsafe_allow_html=True)

        stages = [
            ("第一阶段：基础准备", f"学习课程：{', '.join(courses[:2])}", "目标：掌握基础编程和数学"),
            ("第二阶段：技能提升", f"学习课程：{', '.join(courses[2:4] if len(courses) > 2 else courses)}", "目标：完成项目实战"),
            ("第三阶段：考证冲刺", f"推荐证书：{', '.join(certs)}", "目标：考取核心证书"),
            ("第四阶段：实习/就业", f"目标岗位：{direction_name}", "目标：积累实习经验，准备面试")
        ]

        left, right = st.columns([1.3, 1])

        with left:
            st.markdown("""
            <div class="section-shell">
                <div class="section-header">
                    <div class="section-kicker">Phased roadmap</div>
                    <div class="section-title">阶段化成长路线</div>
                    <p class="section-caption">把结果拆成四个阶段，按基础、提升、考证、实习逐步推进。</p>
                </div>
            """, unsafe_allow_html=True)
            for title, line1, line2 in stages:
                st.markdown(f"""
                <div class="timeline-stage">
                    <div class="timeline-card">
                        <div class="timeline-stage-title">{title}</div>
                        <div class="timeline-stage-caption">{line1}</div>
                        <div class="timeline-stage-caption">{line2}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with right:
            st.markdown("""
            <div class="section-shell">
                <div class="section-header">
                    <div class="section-kicker">Capability stack</div>
                    <div class="section-title">技能与证书面板</div>
                    <p class="section-caption">把需要补齐的能力与优先证书拆开看，减少信息混杂。</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('<div class="eyebrow-text" style="margin:0.9rem 0 0.55rem;">核心技能</div>', unsafe_allow_html=True)
            for skill in skills:
                st.markdown(f'<div class="compact-card"><div class="result-card-title">{skill}</div></div>', unsafe_allow_html=True)

            st.markdown('<div class="eyebrow-text" style="margin:0.9rem 0 0.55rem;">优先证书</div>', unsafe_allow_html=True)
            for cert in certs:
                st.markdown(f'<div class="compact-card"><div class="result-card-title">{cert}</div></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="section-header">
            <div class="section-kicker">Action guidance</div>
            <div class="section-title">个性化建议与学习资源</div>
            <p class="section-caption">先识别当前短板，再给出资源入口，帮助你把路线真正落地。</p>
        </div>
        """, unsafe_allow_html=True)

        suggestions = []
        if math_level == "较弱":
            suggestions.append("建议先加强数学基础，可以学习《高等数学》和《概率论》网课")
        if prog_level == "无基础":
            suggestions.append("建议从Python入门，完成《Python编程从入门到实践》")
        if available_time == "<5小时":
            suggestions.append("时间有限，建议制定每周固定学习计划，保持持续性")
        if "银行" in preferred_industry:
            suggestions.append("银行方向建议考取FRM、银行从业资格证")
        if "量化交易" in career_goal:
            suggestions.append("量化方向建议多参与Kaggle竞赛积累实战经验")

        if not suggestions:
            suggestions.append("你的基础条件很好，建议尽早开始准备相关证书和实习")

        sug_col, res_col = st.columns([1.15, 0.85])
        with sug_col:
            st.markdown('<div class="section-shell">', unsafe_allow_html=True)
            for s in suggestions:
                st.markdown(f'<div class="insight-card"><div class="card-caption">{s}</div></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with res_col:
            st.markdown('<div class="section-shell">', unsafe_allow_html=True)
            resources = [
                ("Coursera", "机器学习 / 深度学习课程"),
                ("Kaggle", "数据科学竞赛平台"),
                ("中国大学MOOC", "国内名校课程")
            ]
            for name, desc in resources:
                st.markdown(f"""
                <div class="resource-card compact-card">
                    <div class="result-card-title">{name}</div>
                    <div class="result-card-meta">{desc}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    elif generate_btn:
        st.warning("请填写完整信息")

    st.markdown('</div>', unsafe_allow_html=True)
