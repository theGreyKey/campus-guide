"""
职业生态页面
"""


import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import networkx as nx
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils.data_loader import load_job_data, load_cert_data, safe_get


def build_job_cert_map(cert_df):
    """构建职业->证书映射"""
    mapping = {}
    if cert_df.empty:
        return mapping
    
    for _, row in cert_df.iterrows():
        cert = safe_get(row, "证书名称", "")
        jobs_text = safe_get(row, "对应岗位", "")
        if not cert or not jobs_text:
            continue
        for job in str(jobs_text).split("、"):  # 使用中文顿号分隔
            job = job.strip()
            if job:
                if job not in mapping:
                    mapping[job] = []
                if cert not in mapping[job]:
                    mapping[job].append(cert)
    return mapping


def render():
    st.markdown('<h2><i class="fas fa-chart-network"></i> 金融科技职业生态图谱</h2>', unsafe_allow_html=True)
    
    job_df = load_job_data()
    cert_df = load_cert_data()
    if job_df.empty:
        return
    
    job_cert_map = build_job_cert_map(cert_df)
    
    #处理从证书页面跳转过来的逻辑
    if st.session_state.get("jump_from_cert", False) and st.session_state.get("selected_job"):
        st.markdown(f'<div class="jump-notice">✨ 已从「证书导航」跳转，正在查看：<strong>{st.session_state.selected_job}</strong></div>', unsafe_allow_html=True)
        
        col_back1, _ = st.columns([1, 5])
        with col_back1:
            if st.button("← 返回证书导航"):
                st.session_state.jump_from_cert = False
                st.session_state.selected_job = None
                st.session_state.nav_selected = "证书导航"
                st.rerun()
        st.markdown("---")
        
        # 获取选中的职业
        if st.session_state.selected_job in job_df["岗位"].tolist():
            selected = st.session_state.selected_job
        else:
            # 模糊匹配
            matched = job_df[job_df["岗位"].str.contains(st.session_state.selected_job[:4], na=False)]
            if len(matched) > 0:
                selected = matched.iloc[0]["岗位"]
            else:
                selected = job_df["岗位"].tolist()[0]
        
        # 重置跳转标志
        st.session_state.jump_from_cert = False
        
    else:
        # 正常选择职业
        job_list = job_df["岗位"].dropna().tolist()
        selected = st.selectbox("🔍 选择职业查看详情", job_list)
    
    info = job_df[job_df["岗位"] == selected].iloc[0]
    
    #职业生态图谱
    st.markdown("### 🌐 职业生态图谱")
    
    G = nx.Graph()
    G.add_node("金融科技")
    for _, row in job_df.iterrows():
        job = safe_get(row, "岗位", "")
        if job:
            G.add_node(job)
            G.add_edge("金融科技", job)
    
    try:
        pos = nx.spring_layout(G, seed=42, k=1)
    except:
        pos = nx.circular_layout(G)
    
    # 边
    ex, ey = [], []
    for e in G.edges():
        try:
            x0, y0 = pos[e[0]]
            x1, y1 = pos[e[1]]
            ex.extend([x0, x1, None])
            ey.extend([y0, y1, None])
        except:
            pass
    
    edge_trace = go.Scatter(
        x=ex, y=ey, 
        mode='lines', 
        line=dict(width=1, color='rgba(42,92,138,0.3)'), 
        hoverinfo='none'
    )
    
    # 节点
    nx_, ny_, ntxt, nsize, ncolor = [], [], [], [], []
    for node in G.nodes():
        try:
            nx_.append(pos[node][0])
            ny_.append(pos[node][1])
        except:
            continue
        
        if node == "金融科技":
            ntxt.append("🎯 金融科技职业核心")
            nsize.append(60)
            ncolor.append(10)
        else:
            row = job_df[job_df["岗位"] == node].iloc[0]
            fut = safe_get(row, "行业前景评分（10分制）", 5)
            diff = safe_get(row, "进入难度（1-10）", 5)
            try:
                fut = float(fut)
                diff = float(diff)
            except:
                fut, diff = 5, 5
            ntxt.append(f"<b>{node}</b><br>前景：{fut}/10<br>难度：{diff}/10")
            nsize.append(max(20, diff * 5))
            ncolor.append(fut)
    
    node_trace = go.Scatter(
        x=nx_, y=ny_,
        mode='markers',
        hoverinfo='text',
        text=ntxt,
        marker=dict(
            showscale=True, 
            colorscale='Blues', 
            color=ncolor, 
            size=nsize,
            colorbar=dict(title="行业前景"), 
            line=dict(width=1.5, color='white')
        )
    )
    
    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title=dict(text="✨ 职业生态图谱", x=0.5, font=dict(size=18)),
        showlegend=False, 
        height=550,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
    
    #职业深度画像
    st.markdown("### 💼 职业深度画像")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="white-card">
            <div class="metric-value">{safe_get(info, "行业前景评分（10分制）", 5)}/10</div>
            <div class="metric-label">🚀 行业前景</div>
        </div>
        <div class="white-card">
            <div class="metric-value">{safe_get(info, "进入难度（1-10）", 5)}/10</div>
            <div class="metric-label">🎯 进入难度</div>
        </div>
        """, unsafe_allow_html=True)
    
    with c2:
        st.markdown(f"""
        <div class="white-card">
            <div class="metric-value">{safe_get(info, "压力与工作时间")}</div>
            <div class="metric-label">🔥 工作压力</div>
        </div>
        <div class="white-card">
            <div class="metric-value">{safe_get(info, "学业倾向")[:20]}...</div>
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
            <div class="detail-value">{safe_get(info, '岗位属性与方向')}</div>
        </div>
        <div class="detail-item">
            <div class="detail-icon"><i class="fas fa-coins"></i></div>
            <div class="detail-label">薪资结构</div>
            <div class="detail-value">{safe_get(info, '薪资与薪资结构')}</div>
        </div>
        <div class="detail-item">
            <div class="detail-icon"><i class="fas fa-city"></i></div>
            <div class="detail-label">主要城市</div>
            <div class="detail-value">{safe_get(info, '主要就业城市')}</div>
        </div>
        <div class="detail-item">
            <div class="detail-icon"><i class="fas fa-building"></i></div>
            <div class="detail-label">典型企业</div>
            <div class="detail-value">{safe_get(info, '典型企业/机构')}</div>
        </div>
        <div class="detail-item">
            <div class="detail-icon"><i class="fas fa-users"></i></div>
            <div class="detail-label">适合人群</div>
            <div class="detail-value">{safe_get(info, '适合人群（含MBTI倾向）')}</div>
        </div>
        <div class="detail-item">
            <div class="detail-icon"><i class="fas fa-tools"></i></div>
            <div class="detail-label">技能要求</div>
            <div class="detail-value">{safe_get(info, '技能要求（具体）')}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 关联证书推荐
    st.markdown("### 🎓 关联证书推荐")
    st.caption("点击证书可跳转到「证书导航」页面的深度画像")
    
    related = job_cert_map.get(selected, [])
    
    if related:
        cols = st.columns(min(4, len(related)))
        for idx, cert in enumerate(related[:4]):
            with cols[idx % 4]:
                st.markdown(f"""
                <div class="clickable-card" style="cursor: pointer;">
                    <i class="fas fa-certificate" style="font-size: 1.8rem; color: #2A5C8A;"></i>
                    <div style="font-weight: 600; margin-top: 8px;">{cert}</div>
                    <div style="font-size: 0.75rem; color: #6B7A8A;">点击查看详情</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"查看 {cert}", key=f"job_cert_{idx}"):
                    st.session_state.selected_cert = cert
                    st.session_state.jump_from_job = True
                    st.session_state.nav_selected = "证书导航"
                    st.rerun()
        
        if len(related) > 4:
            with st.expander(f"📋 查看更多关联证书（共{len(related)}个）"):
                for idx, cert in enumerate(related[4:]):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"🎓 {cert}")
                    with col2:
                        if st.button(f"查看", key=f"job_cert_more_{idx}"):
                            st.session_state.selected_cert = cert
                            st.session_state.jump_from_job = True
                            st.session_state.nav_selected = "证书导航"
                            st.rerun()
    else:
        st.info("💡 暂无直接关联的证书，建议查看「证书导航」页面了解更多认证信息")


# 确保 render 函数可以被导入
if __name__ != "__main__":
    pass