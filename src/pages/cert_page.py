"""
证书导航页面
"""


import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import networkx as nx
from config.settings import CERTIFICATE_LINKS, ROADMAPS, RECOMMENDATION_RULES
from src.utils.data_loader import load_cert_data, load_job_data, safe_get, parse_rating

def build_cert_job_map(cert_df, job_df):
    """构建证书->职业映射"""
    mapping = {}
    if cert_df.empty:
        return mapping

    for _, row in cert_df.iterrows():
        cert = safe_get(row, "证书名称", "")
        jobs_text = safe_get(row, "对应岗位", "")
        if not cert or not jobs_text:
            continue
        mapping[cert] = [j.strip() for j in str(jobs_text).split("、") if j.strip()]
    return mapping

def render():
    st.markdown('<div class="page-shell">', unsafe_allow_html=True)

    cert_df = load_cert_data()
    job_df = load_job_data()
    if cert_df.empty:
        st.markdown('</div>', unsafe_allow_html=True)
        return

    cert_job_map = build_cert_job_map(cert_df, job_df)

    if st.session_state.jump_from_job and st.session_state.selected_cert:
        st.markdown(f'<div class="jump-notice">已从「职业生态」跳转，当前正在查看证书画像：<strong>{st.session_state.selected_cert}</strong></div>', unsafe_allow_html=True)
        if st.button("返回职业生态", use_container_width=True):
            st.session_state.jump_from_job = False
            st.session_state.selected_cert = None
            st.session_state.nav_selected = "职业生态"
            st.rerun()
        st.session_state.jump_from_job = False

    try:
        query_params = st.query_params
        cert_param = query_params.get("cert", "")
        if cert_param and cert_param in cert_df["证书名称"].tolist():
            st.session_state.selected_cert_detail = cert_param
    except:
        pass

    hero_cert = st.session_state.get("selected_cert_detail") or cert_df["证书名称"].tolist()[0]
    st.markdown(f"""
    <div class="page-hero">
        <div class="hero-grid">
            <div>
                <div class="section-kicker">Certification dossier</div>
                <h2>金融科技证书导航</h2>
                <p class="section-caption">围绕证书生态、深度画像、智能推荐与路线图，构建与职业页一致的情报画像语言。</p>
                <div class="tag-row" style="margin-top:0.9rem;">
                    <span class="tag tag-primary">生态关系</span>
                    <span class="tag tag-accent">投入产出</span>
                    <span class="tag tag-success">路线规划</span>
                </div>
            </div>
            <div class="panel-card">
                <div class="eyebrow-text">Current focus</div>
                <div class="card-title">默认深度查看：{hero_cert}</div>
                <div class="card-caption">你可以在 tabs 中切换生态、画像、推荐与路线，保持浏览逻辑不变但获得更统一的产品层次。</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["证书生态图", "证书深度画像", "智能证书推荐", "证书路线图"])

    with tab1:
        st.markdown("""
        <div class="chart-frame">
            <div class="chart-header">
                <div>
                    <div class="chart-title">金融科技证书生态系统</div>
                    <div class="chart-caption">节点大小表示含金量，颜色表示考试难度，连线表示证书之间的关联强度。</div>
                </div>
                <span class="tag tag-primary">Graph module</span>
            </div>
        """, unsafe_allow_html=True)

        G = nx.Graph()
        G.add_node("金融科技")
        cert_data = {}

        for _, row in cert_df.iterrows():
            name = safe_get(row, "证书名称", "")
            if not name:
                continue
            diff = parse_rating(safe_get(row, "考试难度", 5))
            val = parse_rating(safe_get(row, "含金量", 5))
            G.add_node(name)
            G.add_edge("金融科技", name)
            cert_data[name] = {"difficulty": diff, "value": val, "row": row}

        for src, tgt, w in CERTIFICATE_LINKS:
            if src in cert_data and tgt in cert_data:
                G.add_edge(src, tgt, weight=w)

        try:
            pos = nx.spring_layout(G, seed=42, k=1.2)
        except:
            pos = nx.circular_layout(G)

        ex, ey = [], []
        for e in G.edges():
            try:
                ex.extend([pos[e[0]][0], pos[e[1]][0], None])
                ey.extend([pos[e[0]][1], pos[e[1]][1], None])
            except:
                pass

        edge_trace = go.Scatter(x=ex, y=ey, mode='lines', line=dict(width=1, color='rgba(130,168,217,0.24)'), hoverinfo='none')

        nx_, ny_, ntext, nsize, ncolor = [], [], [], [], []
        for node in G.nodes():
            try:
                nx_.append(pos[node][0])
                ny_.append(pos[node][1])
            except:
                continue

            if node == "金融科技":
                ntext.append("<b>金融科技证书核心</b>")
                nsize.append(50)
                ncolor.append(5)
            else:
                d = cert_data[node]["difficulty"]
                v = cert_data[node]["value"]
                info = cert_data[node]["row"]
                hover = f"<b>{node}</b><br>含金量：{v}/10<br>难度：{d}/10<br>费用：{safe_get(info, '考试费用')}<br>备考：{safe_get(info, '备考周期')}"
                ntext.append(hover)
                nsize.append(max(15, min(50, v * 5)))
                ncolor.append(d)

        node_trace = go.Scatter(
            x=nx_, y=ny_,
            mode='markers',
            hoverinfo='text',
            text=ntext,
            marker=dict(showscale=True, colorscale='Blues', color=ncolor, size=nsize,
                       colorbar=dict(title="考试难度"), line=dict(width=1.5, color='rgba(255,255,255,0.85)'))
        )

        fig = go.Figure(data=[edge_trace, node_trace])
        fig.update_layout(
            showlegend=False, height=650,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#EAF2FB")
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        cert_list = cert_df["证书名称"].tolist()
        default_index = 0
        selected_cert_detail = st.session_state.get("selected_cert_detail")
        if selected_cert_detail in cert_list:
            default_index = cert_list.index(selected_cert_detail)
        selected = st.selectbox("选择证书查看深度画像", cert_list, index=default_index, key="cert_select")
        info = cert_df[cert_df["证书名称"] == selected].iloc[0]
        st.session_state.selected_cert_detail = selected

        st.markdown(f"""
        <div class="metric-strip">
            <div class="metric-item">
                <div class="metric-label">Difficulty</div>
                <div class="metric-value">{parse_rating(safe_get(info, '考试难度', 5))}/10</div>
                <div class="metric-note">考试难度</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Value</div>
                <div class="metric-value">{parse_rating(safe_get(info, '含金量', 5))}/10</div>
                <div class="metric-note">证书含金量</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Cost</div>
                <div class="metric-value">{safe_get(info, '考试费用')}</div>
                <div class="metric-note">考试费用</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Prep cycle</div>
                <div class="metric-value">{safe_get(info, '备考周期')}</div>
                <div class="metric-note">备考周期</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="section-header">
            <div class="section-kicker">Certificate profile</div>
            <div class="section-title">证书画像详情</div>
            <p class="section-caption">从适合人群、企业认可、推荐阶段与性价比判断证书是否值得投入。</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="detail-list">
            <div class="detail-item"><div class="detail-label">适合人群</div><div class="detail-value">{safe_get(info, '适合人群')}</div></div>
            <div class="detail-item"><div class="detail-label">典型企业</div><div class="detail-value">{safe_get(info, '典型企业认可')}</div></div>
            <div class="detail-item"><div class="detail-label">推荐阶段</div><div class="detail-value">{safe_get(info, '推荐年级')}</div></div>
            <div class="detail-item"><div class="detail-label">性价比</div><div class="detail-value">{safe_get(info, '性价比评价', '中')}</div></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="section-header">
            <div class="section-kicker">Related roles</div>
            <div class="section-title">关联职业推荐</div>
            <p class="section-caption">保留现有 session_state 跳转逻辑，但让卡片与 CTA 成为同一操作单元。</p>
        </div>
        """, unsafe_allow_html=True)
        related_jobs = cert_job_map.get(selected, [])

        if related_jobs:
            for i in range(0, min(len(related_jobs), 4), 2):
                cols = st.columns(2)
                for j in range(2):
                    idx = i + j
                    if idx < min(len(related_jobs), 4):
                        job = related_jobs[idx]
                        with cols[j]:
                            st.markdown(f"""
                            <div class="recommendation-card">
                                <div class="card-title-row">
                                    <div class="result-card-title">{job}</div>
                                    <span class="tag tag-primary">关联职业</span>
                                </div>
                                <div class="result-card-meta">跳转后可继续查看职业画像、生态图谱与相关证书推荐。</div>
                                <div class="card-body-muted">用于判断该证书对应的职业出口与能力转换方向。</div>
                            </div>
                            """, unsafe_allow_html=True)
                            if st.button(f"查看 {job}", key=f"cert_job_{selected}_{idx}", use_container_width=True):
                                st.session_state.selected_job = job
                                st.session_state.jump_from_cert = True
                                st.session_state.nav_selected = "职业生态"
                                st.rerun()

            if len(related_jobs) > 4:
                with st.expander(f"查看更多关联职业（共{len(related_jobs)}个）"):
                    for idx, job in enumerate(related_jobs[4:]):
                        st.markdown(f"""
                        <div class="compact-card">
                            <div class="card-title-row">
                                <div class="result-card-title">{job}</div>
                                <span class="tag">更多方向</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button("查看详情", key=f"cert_job_more_{selected}_{idx}", use_container_width=True):
                            st.session_state.selected_job = job
                            st.session_state.jump_from_cert = True
                            st.session_state.nav_selected = "职业生态"
                            st.rerun()
        else:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-title">暂无直接关联职业信息</div>
                <div class="empty-caption">可以先浏览职业生态页，反向查看该证书可能补足的方向。</div>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="section-shell"><div class="section-header"><div class="section-kicker">Recommendation</div><div class="section-title">智能证书推荐系统</div><p class="section-caption">根据兴趣与目标组合，为你匹配更合适的证书路径。</p></div>', unsafe_allow_html=True)

        with st.form("ai_form"):
            col1, col2 = st.columns(2)
            with col1:
                like_math = st.selectbox("数学兴趣", ["是", "一般", "否"])
                like_finance = st.selectbox("金融兴趣", ["是", "一般", "否"])
                mbti = st.selectbox("MBTI类型", ["INTJ", "INTP", "ENTJ", "ENTP", "ISTJ", "ESTJ", "其他"])
            with col2:
                like_prog = st.selectbox("编程兴趣", ["是", "一般", "否"])
                career_goal = st.selectbox("职业目标", ["量化交易", "风险管理", "金融产品", "AI开发", "数据分析"])
                exam_time = st.selectbox("备考时间", ["充裕(>6个月)", "适中(3-6个月)", "紧张(<3个月)"])

            submitted = st.form_submit_button("开始推荐", use_container_width=True, type="primary")

        if submitted:
            recommendations = []

            if like_math == "是" and like_prog == "是" and career_goal == "量化交易":
                recommendations.append(("CQF", "金科量化路线", 95, "你对数学和编程都感兴趣，非常适合量化金融。CQF是量化圈的硬通货。"))
                recommendations.append(("Python数据分析", "金科量化路线", 85, "Python是量化的基础工具。"))

            if career_goal == "AI开发":
                recommendations.append(("机器学习", "AI金融路线", 92, "AI+金融是当前最热门的赛道。"))
                recommendations.append(("DeepLearning.AI", "AI金融路线", 88, "吴恩达的深度学习专项。"))

            if career_goal == "风险管理" or mbti in ["ISTJ", "INTJ"]:
                recommendations.append(("FRM", "风控专家路线", 90, "FRM在银行风控岗认可度极高。"))

            if career_goal == "金融产品" or mbti in ["ENTJ", "ENFJ"]:
                recommendations.append(("SHMFTPP", "金融科技产品路线", 88, "深港澳金融科技师，性价比极高。"))

            if not recommendations:
                recommendations = [
                    ("Python数据分析", "数据分析路线", 85, "入门友好，就业面广。"),
                    ("Tableau/Power BI", "数据分析路线", 80, "数据可视化技能。")
                ]

            if exam_time == "紧张(<3个月)":
                recommendations = [r for r in recommendations if "CQF" not in r[0] and "FRM" not in r[0]][:2]

            for cert, route, rec_score, reason in recommendations[:3]:
                st.markdown(f"""
                <div class="recommendation-card">
                    <div class="card-title-row">
                        <span class="recommend-title">{cert}</span>
                        <span class="recommend-score">匹配度 {rec_score}%</span>
                    </div>
                    <div class="card-body-muted">推荐路线：{route}</div>
                    <div class="card-body-muted">{reason}</div>
                </div>
                """, unsafe_allow_html=True)

            st.info(f"**个性化建议**：基于你的MBTI类型「{mbti}」和职业目标「{career_goal}」，建议大二开始准备基础证书。")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="section-shell"><div class="section-header"><div class="section-kicker">Roadmap</div><div class="section-title">金融科技证书路线图</div><p class="section-caption">结合发展方向查看推荐证书时间线与对应职业出口。</p></div>', unsafe_allow_html=True)

        route_names = list(ROADMAPS.keys())
        selected_route = st.selectbox("选择发展路线", route_names)
        route = ROADMAPS[selected_route]

        st.markdown(f"""
        <div class="guide-card">
            <div class="card-title-row">
                <div class="card-title">{selected_route}</div>
                <span class="tag tag-primary">路线说明</span>
            </div>
            <div class="card-caption">{route['description']}</div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns([1.2, 0.8])
        with c1:
            st.markdown('<div class="section-shell"><div class="card-title">证书学习时间线</div>', unsafe_allow_html=True)
            for i, cert in enumerate(route["certificates"]):
                stage = ["大一/大二", "大二/大三", "大三", "大三/大四"][i] if i < 4 else "大三/大四"
                st.markdown(f"""
                <div class="timeline-stage">
                    <div class="timeline-card">
                        <div class="timeline-stage-title">{stage}</div>
                        <div class="timeline-stage-caption">重点证书：{cert}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="section-shell"><div class="card-title">对应职业出口</div>', unsafe_allow_html=True)
            for career in route["careers"]:
                st.markdown(f'<div class="compact-card"><div class="result-card-title">{career}</div></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.info(f"**建议**：{selected_route} 建议大二开始准备基础证书，循序渐进备考。")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
