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
    st.markdown('<h2><i class="fas fa-certificate"></i> 金融科技证书导航系统</h2>', unsafe_allow_html=True)
    
    cert_df = load_cert_data()
    job_df = load_job_data()
    if cert_df.empty:
        return
    
    cert_job_map = build_cert_job_map(cert_df, job_df)
    
    # 处理跳转
    if st.session_state.jump_from_job and st.session_state.selected_cert:
        st.markdown(f'<div class="jump-notice">✨ 已从「职业生态」跳转，正在查看：<strong>{st.session_state.selected_cert}</strong></div>', unsafe_allow_html=True)
        if st.button("← 返回职业生态"):
            st.session_state.jump_from_job = False
            st.session_state.selected_cert = None
            st.session_state.nav_selected = "职业生态"
            st.rerun()
        st.markdown("---")
        st.session_state.jump_from_job = False
    
    # 获取 URL 参数中的证书
    try:
        query_params = st.query_params
        cert_param = query_params.get("cert", "")
        if cert_param and cert_param in cert_df["证书名称"].tolist():
            st.session_state.selected_cert_detail = cert_param
    except:
        pass
    
    tab1, tab2, tab3, tab4 = st.tabs(["🌌 证书宇宙图", "🔍 证书深度画像", "🤖 AI证书推荐", "🗺️ 证书路线图"])
    
    # Tab 1: 证书宇宙图
    with tab1:
        st.markdown('<div class="chart-title">🌌 金融科技证书生态系统</div>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center;color:#6B7A8A;">节点大小 = 含金量 | 颜色 = 难度 | 连线 = 关联性 | 点击节点查看详情</p>', unsafe_allow_html=True)
        
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
        
        # 边
        ex, ey = [], []
        for e in G.edges():
            try:
                ex.extend([pos[e[0]][0], pos[e[1]][0], None])
                ey.extend([pos[e[0]][1], pos[e[1]][1], None])
            except:
                pass
        
        edge_trace = go.Scatter(x=ex, y=ey, mode='lines', line=dict(width=1, color='rgba(100,100,150,0.4)'), hoverinfo='none')
        
        # 节点
        nx_, ny_, ntext, nsize, ncolor = [], [], [], [], []
        for node in G.nodes():
            try:
                nx_.append(pos[node][0])
                ny_.append(pos[node][1])
            except:
                continue
            
            if node == "金融科技":
                ntext.append("<b>🎯 金融科技证书核心</b>")
                nsize.append(50)
                ncolor.append(5)
            else:
                d = cert_data[node]["difficulty"]
                v = cert_data[node]["value"]
                info = cert_data[node]["row"]
                hover = f"<b>{node}</b><br>⭐ 含金量：{v}/10<br>🎯 难度：{d}/10<br>💰 费用：{safe_get(info, '考试费用')}<br>📅 备考：{safe_get(info, '备考周期')}"
                ntext.append(hover)
                nsize.append(max(15, min(50, v * 5)))
                ncolor.append(d)
        
        node_trace = go.Scatter(
            x=nx_, y=ny_,
            mode='markers',
            hoverinfo='text',
            text=ntext,
            marker=dict(showscale=True, colorscale='RdYlBu_r', color=ncolor, size=nsize,
                       colorbar=dict(title="考试难度"), line=dict(width=1.5, color='white'))
        )
        
        fig = go.Figure(data=[edge_trace, node_trace])
        fig.update_layout(
            showlegend=False, height=650,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 2: 证书深度画像
    with tab2:
        cert_list = cert_df["证书名称"].tolist()
        selected = st.selectbox("🎯 选择证书查看深度画像", cert_list, key="cert_select")
        info = cert_df[cert_df["证书名称"] == selected].iloc[0]
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="metric-item"><div class="metric-value">{parse_rating(safe_get(info, "考试难度", 5))}/10</div><div class="metric-label">🎯 考试难度</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-item"><div class="metric-value">{parse_rating(safe_get(info, "含金量", 5))}/10</div><div class="metric-label">⭐ 含金量</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-item"><div class="metric-value">{safe_get(info, "考试费用")}</div><div class="metric-label">💰 考试费用</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-item"><div class="metric-value">{safe_get(info, "备考周期")}</div><div class="metric-label">⏰ 备考周期</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="metric-item"><div class="metric-value">{safe_get(info, "推荐年级")}</div><div class="metric-label">📚 推荐阶段</div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-item"><div class="metric-value">{safe_get(info, "性价比评价", "中")}</div><div class="metric-label">💎 性价比</div></div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("#### 👥 适合人群分析")
        st.markdown(f"""
        <div class="detail-list">
            <div class="detail-item"><div class="detail-icon"><i class="fas fa-brain"></i></div>
                <div class="detail-label">适合人群</div><div class="detail-value">{safe_get(info, "适合人群")}</div></div>
            <div class="detail-item"><div class="detail-icon"><i class="fas fa-building"></i></div>
                <div class="detail-label">典型企业</div><div class="detail-value">{safe_get(info, "典型企业认可")}</div></div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        #关联职业
        st.markdown("#### 💼 关联职业（点击可查看详情）")
        related_jobs = cert_job_map.get(selected, [])
        
        if related_jobs:
            st.caption("点击下方职业卡片，跳转到职业生态页面查看详情")
            
            # 使用 grid 布局显示职业卡片
            cols = st.columns(min(4, len(related_jobs)))
            for idx, job in enumerate(related_jobs[:4]):
                with cols[idx % 4]:
                    st.markdown(f"""
                    <div class="job-card" style="cursor: pointer; text-align: center; padding: 15px; background: #F5F7FA; border-radius: 12px; border: 1px solid #E2E8F0; transition: all 0.2s;">
                        <i class="fas fa-briefcase" style="font-size: 2rem; color: #2A5C8A;"></i>
                        <div style="font-weight: 600; margin-top: 8px; color: #2A5C8A;">{job}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"查看 {job}", key=f"cert_job_{selected}_{idx}"):
                        st.session_state.selected_job = job
                        st.session_state.jump_from_cert = True
                        st.session_state.nav_selected = "职业生态"
                        st.rerun()
            
            if len(related_jobs) > 4:
                with st.expander(f"📋 查看更多关联职业（共{len(related_jobs)}个）"):
                    for idx, job in enumerate(related_jobs[4:]):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"💼 {job}")
                        with col2:
                            if st.button(f"查看详情", key=f"cert_job_more_{selected}_{idx}"):
                                st.session_state.selected_job = job
                                st.session_state.jump_from_cert = True
                                st.session_state.nav_selected = "职业生态"
                                st.rerun()
        else:
            st.info("💡 暂无直接关联的职业信息")
    
    # Tab 3: AI证书推荐 
    with tab3:
        st.markdown('<div class="chart-title">🤖 AI智能证书推荐系统</div>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center;color:#6B7A8A;">根据你的兴趣和职业目标，AI为你智能匹配最优证书</p>', unsafe_allow_html=True)
        
        with st.form("ai_form"):
            col1, col2 = st.columns(2)
            with col1:
                like_math = st.selectbox("📐 数学兴趣", ["是", "一般", "否"])
                like_finance = st.selectbox("💹 金融兴趣", ["是", "一般", "否"])
                mbti = st.selectbox("🧠 MBTI类型", ["INTJ", "INTP", "ENTJ", "ENTP", "ISTJ", "ESTJ", "其他"])
            with col2:
                like_prog = st.selectbox("💻 编程兴趣", ["是", "一般", "否"])
                career_goal = st.selectbox("🎯 职业目标", ["量化交易", "风险管理", "金融产品", "AI开发", "数据分析"])
                exam_time = st.selectbox("⏰ 备考时间", ["充裕(>6个月)", "适中(3-6个月)", "紧张(<3个月)"])
            
            submitted = st.form_submit_button("🎯 开始AI推荐", use_container_width=True, type="primary")
        
        if submitted:
            st.markdown("---")
            st.markdown("#### 🎯 AI推荐结果")
            
            recommendations = []
            
            if like_math == "是" and like_prog == "是" and career_goal == "量化交易":
                recommendations.append(("🏆 CQF", "金科量化路线", 95, "你对数学和编程都感兴趣，非常适合量化金融。CQF是量化圈的硬通货。"))
                recommendations.append(("🏅 Python数据分析", "金科量化路线", 85, "Python是量化的基础工具。"))
            
            if career_goal == "AI开发":
                recommendations.append(("🏆 机器学习", "AI金融路线", 92, "AI+金融是当前最热门的赛道。"))
                recommendations.append(("🏅 DeepLearning.AI", "AI金融路线", 88, "吴恩达的深度学习专项。"))
            
            if career_goal == "风险管理" or mbti in ["ISTJ", "INTJ"]:
                recommendations.append(("🏆 FRM", "风控专家路线", 90, "FRM在银行风控岗认可度极高。"))
            
            if career_goal == "金融产品" or mbti in ["ENTJ", "ENFJ"]:
                recommendations.append(("🏆 SHMFTPP", "金融科技产品路线", 88, "深港澳金融科技师，性价比极高。"))
            
            if not recommendations:
                recommendations = [
                    ("🏆 Python数据分析", "数据分析路线", 85, "入门友好，就业面广。"),
                    ("🏅 Tableau/Power BI", "数据分析路线", 80, "数据可视化技能。")
                ]
            
            if exam_time == "紧张(<3个月)":
                recommendations = [r for r in recommendations if "CQF" not in r[0] and "FRM" not in r[0]][:2]
            
            for cert, route, rec_score, reason in recommendations[:3]:
                st.markdown(f"""
                <div class="recommend-card">
                    <div><span class="recommend-title">{cert}</span><span class="recommend-score">匹配度 {rec_score}%</span></div>
                    <div style="margin-top:8px;">📌 推荐路线：{route}</div>
                    <div style="margin-top:8px;color:#4A5568;">💡 {reason}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.info(f"💡 **个性化建议**：基于你的MBTI类型「{mbti}」和职业目标「{career_goal}」，建议大二开始准备基础证书。")
    
    #Tab 4: 证书路线图
    with tab4:
        st.markdown('<div class="chart-title">🗺️ 金融科技证书路线图</div>', unsafe_allow_html=True)
        
        route_names = list(ROADMAPS.keys())
        selected_route = st.selectbox("🎯 选择发展路线", route_names)
        route = ROADMAPS[selected_route]
        
        st.markdown(f"#### {selected_route}")
        st.markdown(f"📝 **路线说明**：{route['description']}")
        
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown("##### 📅 证书学习时间线")
            for i, cert in enumerate(route["certificates"]):
                stage = ["大一/大二", "大二/大三", "大三", "大三/大四"][i] if i < 4 else "大三/大四"
                st.markdown(f"**{stage}** → 🏅 {cert}")
        with c2:
            st.markdown("##### 🎯 对应职业")
            for career in route["careers"]:
                st.markdown(f"💼 {career}")
        
        st.info(f"💡 **建议**：{selected_route} 建议大二开始准备基础证书，循序渐进备考。")