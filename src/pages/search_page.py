"""
智能搜索页面
"""
import streamlit as st
import pandas as pd
from src.utils.data_loader import load_job_data, load_cert_data, safe_get

def render():
    st.markdown('<h2><i class="fas fa-search"></i> 智能职业搜索系统</h2>', unsafe_allow_html=True)
    
    job_df = load_job_data()
    cert_df = load_cert_data()
    
    if job_df.empty:
        return
    
    st.markdown("""
    <div class="white-card" style="background: linear-gradient(135deg, #E8F0FE, white);">
        <p style="font-size: 1.1rem; margin-bottom: 10px;">🔍 输入你的偏好，AI 帮你推荐最适合的职业方向</p>
        <p style="color: #6B7A8A; font-size: 0.9rem;">例如：高薪、数学强、不喜欢销售、喜欢编程、稳定、喜欢沟通...</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 搜索输入
    user_input = st.text_area("✏️ 描述你的偏好", placeholder="例如：我想要高薪工作，数学能力强，不喜欢做销售，喜欢和数据打交道...", height=100)
    
    # 快捷标签 - 修复字体颜色不清晰的问题
    st.markdown("##### 🏷️ 快捷标签（点击添加）")
    
    # 添加快捷标签的CSS样式，确保文字颜色清晰可见
    st.markdown("""
    <style>
    /* 快捷标签按钮样式 - 确保文字清晰可见 */
    div[data-testid="column"] button {
        background-color: #e8f0fe !important;
        color: #2A5C8A !important;
        border: 1px solid #2A5C8A !important;
        border-radius: 20px !important;
        padding: 5px 12px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        white-space: nowrap !important;
    }
    div[data-testid="column"] button:hover {
        background-color: #2A5C8A !important;
        color: white !important;
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 快捷标签列表
    quick_tags = ["💰 高薪", "📐 数学强", "💻 喜欢编程", "🏛️ 稳定", "💬 喜欢沟通", "📊 喜欢数据", "⚡ 高压", "🎯 有挑战", "🏦 银行", "📈 量化", "🚫 不喜欢销售"]
    
    # 使用多行布局显示标签
    cols_per_row = 4
    for i in range(0, len(quick_tags), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, tag in enumerate(quick_tags[i:i+cols_per_row]):
            with cols[j]:
                if st.button(tag, key=f"tag_{i+j}"):
                    # 提取标签核心文字（去掉emoji）
                    core_tag = tag.split(" ")[-1] if " " in tag else tag
                    current = user_input if user_input else ""
                    st.session_state.search_input = current + " " + core_tag
                    st.rerun()
    
    if "search_input" in st.session_state and st.session_state.search_input:
        user_input = st.session_state.search_input
    
    search_btn = st.button("🔍 开始智能搜索", use_container_width=True, type="primary")
    
    if search_btn and user_input:
        st.markdown("---")
        st.markdown("## 📊 搜索结果")
        
        # 关键词匹配
        keywords = {
            "高薪": ["量化研究员", "金融AI工程师", "算法交易工程师", "CQF"],
            "数学强": ["量化研究员", "精算师", "风控建模工程师", "金融数据科学家"],
            "编程": ["量化研究员", "金融科技开发工程师", "算法交易工程师", "Python数据分析"],
            "稳定": ["银行科技岗", "反洗钱分析师", "监管科技岗", "FRM"],
            "沟通": ["金融产品经理", "商业分析师", "金融科技咨询顾问", "SHMFTPP"],
            "数据": ["数据分析师", "金融数据科学家", "数据仓库工程师", "Python数据分析"],
            "量化": ["量化研究员", "算法交易工程师", "CQF", "机器学习"],
            "风控": ["风控建模工程师", "反洗钱分析师", "FRM"],
            "AI": ["金融AI工程师", "机器学习工程师", "DeepLearning.AI"],
            "银行": ["银行科技岗", "反洗钱分析师", "商业银行管培生"],
            "高压": ["量化研究员", "券商投行岗", "算法交易工程师"],
            "挑战": ["量化研究员", "金融AI工程师", "CQF"]
        }
        
        # 匹配职业
        matched_jobs = set()
        matched_certs = set()
        
        input_lower = user_input.lower()
        for kw, items in keywords.items():
            if kw in input_lower or kw.lower() in input_lower:
                for item in items:
                    if item in job_df["岗位"].tolist():
                        matched_jobs.add(item)
                    else:
                        matched_certs.add(item)
        
        # 如果没有匹配，显示默认推荐
        if not matched_jobs and not matched_certs:
            matched_jobs = {"数据分析师", "风控建模工程师", "金融产品经理"}
            matched_certs = {"Python数据分析", "FRM"}
        
        # 显示匹配的职业
        st.markdown("#### 💼 推荐职业方向")
        if matched_jobs:
            # 每行显示3个
            job_list = list(matched_jobs)[:6]
            for i in range(0, len(job_list), 3):
                cols = st.columns(3)
                for j in range(3):
                    idx = i + j
                    if idx < len(job_list):
                        job = job_list[idx]
                        job_info = job_df[job_df["岗位"] == job]
                        if len(job_info) > 0:
                            info = job_info.iloc[0]
                            with cols[j]:
                                st.markdown(f"""
                                <div class="search-result-card" style="background: white; border-radius: 12px; padding: 12px; margin-bottom: 10px; border: 1px solid #E2E8F0;">
                                    <div style="font-size: 1rem; font-weight: 600; color: #2A5C8A;">{job}</div>
                                    <div style="font-size: 0.75rem; color: #6B7A8A; margin-top: 5px;">
                                        前景: {safe_get(info, '行业前景评分（10分制）', 5)}/10 | 
                                        难度: {safe_get(info, '进入难度（1-10）', 5)}/10
                                    </div>
                                    <div style="font-size: 0.8rem; margin-top: 8px; color: #1E2A3A;">{str(safe_get(info, '岗位属性与方向', ''))[:40]}...</div>
                                </div>
                                """, unsafe_allow_html=True)
                                if st.button(f"查看详情", key=f"search_job_{idx}"):
                                    st.session_state.selected_job = job
                                    st.session_state.jump_from_cert = False
                                    st.session_state.nav_selected = "职业生态"
                                    st.rerun()
        
        # 显示匹配的证书
        st.markdown("#### 🎓 推荐证书")
        if matched_certs:
            cert_list = list(matched_certs)[:4]
            for i in range(0, len(cert_list), 3):
                cols = st.columns(3)
                for j in range(3):
                    idx = i + j
                    if idx < len(cert_list):
                        cert = cert_list[idx]
                        with cols[j]:
                            st.markdown(f"""
                            <div class="search-result-card" style="background: white; border-radius: 12px; padding: 12px; margin-bottom: 10px; border: 1px solid #E2E8F0; text-align: center;">
                                <div style="font-size: 1rem; font-weight: 600; color: #2A5C8A;">{cert}</div>
                                <div style="font-size: 0.75rem; color: #6B7A8A;">推荐考取</div>
                            </div>
                            """, unsafe_allow_html=True)
                            if st.button(f"查看证书", key=f"search_cert_{idx}"):
                                st.session_state.selected_cert = cert
                                st.session_state.jump_from_job = False
                                st.session_state.nav_selected = "证书导航"
                                st.rerun()
        
        # AI 综合建议
        st.markdown("---")
        st.markdown("#### 💡 AI 综合建议")
        
        advice = ""
        if "高薪" in input_lower:
            advice += "• 量化研究员、金融AI工程师薪资天花板高，但竞争激烈，建议提前准备相关技能。\n"
        if "数学" in input_lower:
            advice += "• 你的数学优势非常适合量化金融、精算、风控建模方向。\n"
        if "编程" in input_lower:
            advice += "• 编程能力强建议走技术路线：量化开发、金融科技开发、AI工程。\n"
        if "稳定" in input_lower:
            advice += "• 追求稳定可以考虑银行科技岗、监管科技岗、风控岗位。\n"
        if "销售" in input_lower and "不" in input_lower:
            advice += "• 避开销售岗，建议选择后台技术岗：数据分析、风控、开发。\n"
        
        if not advice:
            advice = "• 建议从Python数据分析入门，逐步明确职业方向。\n• 多参加实习和项目，积累实战经验。"
        
        st.info(advice)
        
    elif search_btn:
        st.warning("请输入你的偏好描述")
    
    # 热门职业推荐
    st.markdown("---")
    st.markdown("#### 🔥 热门职业推荐")
    
    hot_jobs = ["量化研究员", "金融AI工程师", "数据分析师", "风控建模工程师", "金融产品经理", "银行科技岗"]
    
    # 每行显示3个
    for i in range(0, len(hot_jobs), 3):
        cols = st.columns(3)
        for j in range(3):
            idx = i + j
            if idx < len(hot_jobs):
                job = hot_jobs[idx]
                with cols[j]:
                    st.markdown(f"""
                    <div class="clickable-card" style="background: #F5F7FA; border-radius: 12px; padding: 12px; text-align: center; cursor: pointer; border: 1px solid #E2E8F0;">
                        <div style="font-weight: 600; color: #2A5C8A;">{job}</div>
                        <div style="font-size: 0.7rem; color: #6B7A8A; margin-top: 4px;">点击查看详情</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"查看{job}", key=f"hot_{idx}"):
                        st.session_state.selected_job = job
                        st.session_state.nav_selected = "职业生态"
                        st.rerun()