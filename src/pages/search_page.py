"""
智能搜索页面
"""
import streamlit as st
import pandas as pd
from src.utils.data_loader import load_job_data, load_cert_data, safe_get


def render():
    st.markdown('<div class="page-shell">', unsafe_allow_html=True)

    job_df = load_job_data()
    cert_df = load_cert_data()

    if job_df.empty:
        st.markdown('</div>', unsafe_allow_html=True)
        return

    st.markdown("""
    <div class="page-hero">
        <div class="hero-grid">
            <div>
                <div class="section-kicker">Search workspace</div>
                <h2>智能职业搜索系统</h2>
                <p class="section-caption">把偏好、能力、行业倾向和不想做的工作方式写进同一个查询框，快速得到职业与证书的组合建议。</p>
                <div class="tag-row" style="margin-top:0.9rem;">
                    <span class="tag tag-primary">职业推荐</span>
                    <span class="tag tag-accent">证书建议</span>
                    <span class="tag tag-success">综合策略</span>
                </div>
            </div>
            <div class="panel-card">
                <div class="eyebrow-text">How to search</div>
                <div class="card-title">像描述理想工作一样输入</div>
                <div class="card-caption">例如：希望高薪、数学能力强、喜欢数据和编程、不想做销售、对银行或量化感兴趣。</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    user_input = st.text_area(
        "描述你的偏好",
        value=st.session_state.get("search_input", ""),
        placeholder="例如：我想要高薪工作，数学能力强，不喜欢做销售，喜欢和数据打交道...",
        height=120,
    )

    st.markdown("""
    <div class="section-shell">
        <div class="section-header">
            <div class="section-kicker">Quick prompts</div>
            <div class="section-title">快捷标签补充区</div>
            <p class="section-caption">标签样式只在该区域内生效，用来快速拼接搜索语义，不污染其他按钮。</p>
        </div>
    """, unsafe_allow_html=True)

    quick_tags = ["高薪", "数学强", "喜欢编程", "稳定", "喜欢沟通", "喜欢数据", "高压", "有挑战", "银行", "量化", "不喜欢销售"]

    st.markdown('<div class="search-tag-scope">', unsafe_allow_html=True)
    cols_per_row = 4
    for i in range(0, len(quick_tags), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, tag in enumerate(quick_tags[i:i + cols_per_row]):
            with cols[j]:
                if st.button(tag, key=f"tag_{i+j}", use_container_width=True):
                    current = st.session_state.get("search_input", user_input or "").strip()
                    st.session_state.search_input = f"{current} {tag}".strip()
                    st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)

    if user_input != st.session_state.get("search_input", ""):
        st.session_state.search_input = user_input

    search_btn = st.button("开始智能搜索", use_container_width=True, type="primary")

    if search_btn and user_input:
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

        if not matched_jobs and not matched_certs:
            matched_jobs = {"数据分析师", "风控建模工程师", "金融产品经理"}
            matched_certs = {"Python数据分析", "FRM"}

        job_count = len(matched_jobs)
        cert_count = len(matched_certs)
        emphasis = "偏技术/分析" if any(k in input_lower for k in ["数学", "编程", "数据", "量化", "ai"]) else "偏综合探索"

        st.markdown(f"""
        <div class="metric-strip">
            <div class="metric-item">
                <div class="metric-label">Query signal</div>
                <div class="metric-value">{len(user_input.strip())}</div>
                <div class="metric-note">当前输入字符数</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Matched roles</div>
                <div class="metric-value">{job_count}</div>
                <div class="metric-note">职业方向命中数</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Matched certs</div>
                <div class="metric-value">{cert_count}</div>
                <div class="metric-note">证书建议命中数</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Search posture</div>
                <div class="metric-value">{emphasis}</div>
                <div class="metric-note">本次搜索的能力倾向</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="section-shell">
            <div class="section-header">
                <div class="section-kicker">Results digest</div>
                <div class="section-title">结果摘要</div>
                <p class="section-caption">先看系统对你输入的总体判断，再进入职业与证书双结果区。</p>
            </div>
            <div class="insight-list" style="margin-top:0.85rem;">
        """, unsafe_allow_html=True)

        digest_items = [
            f"系统从输入中提取出 {job_count} 个职业候选与 {cert_count} 个证书建议。",
            "如果你强调数学、编程、数据或量化，结果会更偏向研究、开发和分析岗。",
            "如果你强调稳定、银行或沟通，结果会更偏向银行科技、产品或咨询类方向。"
        ]
        for item in digest_items:
            st.markdown(f'<div class="insight-card"><div class="card-caption">{item}</div></div>', unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="section-header">
            <div class="section-kicker">Role recommendations</div>
            <div class="section-title">职业推荐结果</div>
            <p class="section-caption">每张卡片展示方向摘要，按钮负责进入详情页，避免卡片与 CTA 割裂。</p>
        </div>
        """, unsafe_allow_html=True)

        if matched_jobs:
            job_list = list(matched_jobs)[:6]
            for i in range(0, len(job_list), 2):
                cols = st.columns(2)
                for j in range(2):
                    idx = i + j
                    if idx < len(job_list):
                        job = job_list[idx]
                        job_info = job_df[job_df["岗位"] == job]
                        if len(job_info) > 0:
                            info = job_info.iloc[0]
                            with cols[j]:
                                st.markdown(f"""
                                <div class="recommendation-card">
                                    <div class="card-title-row">
                                        <div class="result-card-title">{job}</div>
                                        <span class="tag tag-primary">职业推荐</span>
                                    </div>
                                    <div class="result-card-meta">前景 {safe_get(info, '行业前景评分（10分制）', 5)}/10 · 难度 {safe_get(info, '进入难度（1-10）', 5)}/10</div>
                                    <div class="card-body-muted">{str(safe_get(info, '岗位属性与方向', ''))[:70]}...</div>
                                    <div class="card-body-muted" style="margin-top:0.45rem;">典型城市：{safe_get(info, '主要就业城市', '待补充')}</div>
                                </div>
                                """, unsafe_allow_html=True)
                                if st.button("查看职业详情", key=f"search_job_{idx}", use_container_width=True):
                                    st.session_state.selected_job = job
                                    st.session_state.jump_from_cert = False
                                    st.session_state.nav_selected = "职业生态"
                                    st.rerun()
        else:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-title">暂未匹配到职业方向</div>
                <div class="empty-caption">可以补充更多偏好关键词，例如行业、能力优势或希望避免的工作内容。</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="section-header">
            <div class="section-kicker">Certification suggestions</div>
            <div class="section-title">证书建议结果</div>
            <p class="section-caption">证书区与职业区平行呈现，帮助你同时判断方向与验证路径。</p>
        </div>
        """, unsafe_allow_html=True)

        if matched_certs:
            cert_list = list(matched_certs)[:4]
            for i in range(0, len(cert_list), 2):
                cols = st.columns(2)
                for j in range(2):
                    idx = i + j
                    if idx < len(cert_list):
                        cert = cert_list[idx]
                        with cols[j]:
                            cert_info = cert_df[cert_df["证书名称"] == cert] if not cert_df.empty and "证书名称" in cert_df.columns else pd.DataFrame()
                            meta = "适合作为当前方向的补充能力证明或学习起点。"
                            if len(cert_info) > 0:
                                cert_row = cert_info.iloc[0]
                                meta = f"含金量 {safe_get(cert_row, '含金量', '待补充')} · 难度 {safe_get(cert_row, '考试难度', '待补充')} · 备考周期 {safe_get(cert_row, '备考周期', '待补充')}"
                            st.markdown(f"""
                            <div class="recommendation-card">
                                <div class="card-title-row">
                                    <div class="result-card-title">{cert}</div>
                                    <span class="tag tag-accent">证书建议</span>
                                </div>
                                <div class="result-card-meta">{meta}</div>
                                <div class="card-body-muted">适合作为当前搜索偏好的能力背书或路线起点。</div>
                            </div>
                            """, unsafe_allow_html=True)
                            if st.button("查看证书详情", key=f"search_cert_{idx}", use_container_width=True):
                                st.session_state.selected_cert = cert
                                st.session_state.jump_from_job = False
                                st.session_state.nav_selected = "证书导航"
                                st.rerun()
        else:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-title">暂未匹配到证书建议</div>
                <div class="empty-caption">可以增加更明确的职业目标，比如量化、银行、风控或 AI。</div>
            </div>
            """, unsafe_allow_html=True)

        advice = ""
        if "高薪" in input_lower:
            advice += "- 量化研究员、金融AI工程师薪资天花板高，但竞争激烈，建议提前准备相关技能。\n"
        if "数学" in input_lower:
            advice += "- 你的数学优势非常适合量化金融、精算、风控建模方向。\n"
        if "编程" in input_lower:
            advice += "- 编程能力强建议走技术路线：量化开发、金融科技开发、AI工程。\n"
        if "稳定" in input_lower:
            advice += "- 追求稳定可以考虑银行科技岗、监管科技岗、风控岗位。\n"
        if "销售" in input_lower and "不" in input_lower:
            advice += "- 避开销售岗，建议选择后台技术岗：数据分析、风控、开发。\n"

        if not advice:
            advice = "- 建议从Python数据分析入门，逐步明确职业方向。\n- 多参加实习和项目，积累实战经验。"

        st.markdown("""
        <div class="section-shell">
            <div class="section-header">
                <div class="section-kicker">Recommendation memo</div>
                <div class="section-title">综合建议</div>
                <p class="section-caption">把职业方向、能力短板和下一步动作收敛成可执行判断。</p>
            </div>
        """, unsafe_allow_html=True)
        st.info(advice)
        st.markdown('</div>', unsafe_allow_html=True)

    elif search_btn:
        st.warning("请输入你的偏好描述")

    st.markdown("""
    <div class="section-shell">
        <div class="section-header">
            <div class="section-kicker">Popular picks</div>
            <div class="section-title">热门职业入口</div>
            <p class="section-caption">如果你还没有明确目标，可以先从热门方向进入详情页继续探索。</p>
        </div>
    """, unsafe_allow_html=True)

    hot_jobs = ["量化研究员", "金融AI工程师", "数据分析师", "风控建模工程师", "金融产品经理", "银行科技岗"]

    for i in range(0, len(hot_jobs), 3):
        cols = st.columns(3)
        for j in range(3):
            idx = i + j
            if idx < len(hot_jobs):
                job = hot_jobs[idx]
                with cols[j]:
                    st.markdown(f"""
                    <div class="interactive-card compact-card">
                        <div class="card-title-row">
                            <div class="job-card-title">{job}</div>
                            <span class="tag">热门方向</span>
                        </div>
                        <div class="job-card-meta">进入详情页可继续查看职业画像、关联证书与发展提示。</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("查看详情", key=f"hot_{idx}", use_container_width=True):
                        st.session_state.selected_job = job
                        st.session_state.nav_selected = "职业生态"
                        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
