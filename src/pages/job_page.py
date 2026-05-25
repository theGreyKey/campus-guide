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
        for job in str(jobs_text).split("、"):
            job = job.strip()
            if job:
                if job not in mapping:
                    mapping[job] = []
                if cert not in mapping[job]:
                    mapping[job].append(cert)
    return mapping


def render():
    st.markdown('<div class="page-shell">', unsafe_allow_html=True)

    job_df = load_job_data()
    cert_df = load_cert_data()
    if job_df.empty:
        st.markdown('</div>', unsafe_allow_html=True)
        return

    job_cert_map = build_job_cert_map(cert_df)

    if st.session_state.get("jump_from_cert", False) and st.session_state.get("selected_job"):
        st.markdown(f'<div class="jump-notice">已从「证书导航」跳转，当前正在查看职业画像：<strong>{st.session_state.selected_job}</strong></div>', unsafe_allow_html=True)

        col_back1, _ = st.columns([1, 5])
        with col_back1:
            if st.button("返回证书导航", use_container_width=True):
                st.session_state.jump_from_cert = False
                st.session_state.selected_job = None
                st.session_state.nav_selected = "证书导航"
                st.rerun()

        if st.session_state.selected_job in job_df["岗位"].tolist():
            selected = st.session_state.selected_job
        else:
            matched = job_df[job_df["岗位"].str.contains(st.session_state.selected_job[:4], na=False)]
            if len(matched) > 0:
                selected = matched.iloc[0]["岗位"]
            else:
                selected = job_df["岗位"].tolist()[0]

        st.session_state.jump_from_cert = False
    else:
        selected = st.selectbox("选择职业查看详情", job_df["岗位"].dropna().tolist())

    info = job_df[job_df["岗位"] == selected].iloc[0]

    st.markdown(f"""
    <div class="page-hero">
        <div class="hero-grid">
            <div>
                <div class="section-kicker">Career dossier</div>
                <h2>{selected}</h2>
                <p class="section-caption">先把职业放回整体生态，再看前景、门槛、压力、城市与关联证书，形成完整的职业情报画像。</p>
                <div class="tag-row" style="margin-top:0.9rem;">
                    <span class="tag tag-primary">行业前景 {safe_get(info, '行业前景评分（10分制）', 5)}/10</span>
                    <span class="tag tag-accent">进入难度 {safe_get(info, '进入难度（1-10）', 5)}/10</span>
                </div>
            </div>
            <div class="panel-card">
                <div class="eyebrow-text">Profile focus</div>
                <div class="card-title">从生态位置到岗位画像的统一视角</div>
                <div class="card-caption">图谱用于判断位置，画像用于判断匹配度，关联证书用于判断下一步补强路径。</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
        line=dict(width=1, color='rgba(130,168,217,0.24)'),
        hoverinfo='none'
    )

    nx_, ny_, ntxt, nsize, ncolor = [], [], [], [], []
    for node in G.nodes():
        try:
            nx_.append(pos[node][0])
            ny_.append(pos[node][1])
        except:
            continue

        if node == "金融科技":
            ntxt.append("金融科技职业核心")
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
            line=dict(width=1.5, color='rgba(255,255,255,0.85)')
        )
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title=dict(text="职业生态图谱", x=0.5, font=dict(size=18, color="#EAF2FB")),
        showlegend=False,
        height=550,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#EAF2FB")
    )
    st.markdown("""
    <div class="chart-frame">
        <div class="chart-header">
            <div>
                <div class="chart-title">职业生态图谱</div>
                <div class="chart-caption">节点大小体现进入门槛，颜色体现行业前景，用于快速判断该岗位在整体生态中的位置。</div>
            </div>
            <span class="tag tag-primary">Graph module</span>
        </div>
    """, unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-strip">
        <div class="metric-item">
            <div class="metric-label">Outlook</div>
            <div class="metric-value">{safe_get(info, '行业前景评分（10分制）', 5)}/10</div>
            <div class="metric-note">行业前景评分</div>
        </div>
        <div class="metric-item">
            <div class="metric-label">Entry barrier</div>
            <div class="metric-value">{safe_get(info, '进入难度（1-10）', 5)}/10</div>
            <div class="metric-note">进入门槛水平</div>
        </div>
        <div class="metric-item">
            <div class="metric-label">Workload</div>
            <div class="metric-value">{safe_get(info, '压力与工作时间')}</div>
            <div class="metric-note">工作压力与时间节奏</div>
        </div>
        <div class="metric-item">
            <div class="metric-label">Academic tilt</div>
            <div class="metric-value">{safe_get(info, '学业倾向')[:18]}...</div>
            <div class="metric-note">学历或背景倾向</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-header">
        <div class="section-kicker">Role profile</div>
        <div class="section-title">职业画像详情</div>
        <p class="section-caption">从方向、薪资、城市、企业、人群与技能要求六个维度查看岗位情报。</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="detail-list">
        <div class="detail-item">
            <div class="detail-label">岗位方向</div>
            <div class="detail-value">{safe_get(info, '岗位属性与方向')}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">薪资结构</div>
            <div class="detail-value">{safe_get(info, '薪资与薪资结构')}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">主要城市</div>
            <div class="detail-value">{safe_get(info, '主要就业城市')}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">典型企业</div>
            <div class="detail-value">{safe_get(info, '典型企业/机构')}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">适合人群</div>
            <div class="detail-value">{safe_get(info, '适合人群（含MBTI倾向）')}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">技能要求</div>
            <div class="detail-value">{safe_get(info, '技能要求（具体）')}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-header">
        <div class="section-kicker">Related certifications</div>
        <div class="section-title">关联证书推荐</div>
        <p class="section-caption">每张推荐卡都是单一操作单元，浏览后可直接跳转到证书导航页继续查看。</p>
    </div>
    """, unsafe_allow_html=True)

    related = job_cert_map.get(selected, [])

    if related:
        for i in range(0, min(len(related), 4), 2):
            cols = st.columns(2)
            for j in range(2):
                idx = i + j
                if idx < min(len(related), 4):
                    cert = related[idx]
                    with cols[j]:
                        st.markdown(f"""
                        <div class="recommendation-card">
                            <div class="card-title-row">
                                <div class="result-card-title">{cert}</div>
                                <span class="tag tag-accent">关联证书</span>
                            </div>
                            <div class="result-card-meta">进入证书导航页后，可继续查看证书画像、路线图与相关推荐。</div>
                            <div class="card-body-muted">适合作为 {selected} 方向的能力证明或学习补强点。</div>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button("查看证书详情", key=f"job_cert_{idx}", use_container_width=True):
                            st.session_state.selected_cert = cert
                            st.session_state.jump_from_job = True
                            st.session_state.nav_selected = "证书导航"
                            st.rerun()

        if len(related) > 4:
            with st.expander(f"查看更多关联证书（共{len(related)}个）"):
                for idx, cert in enumerate(related[4:]):
                    st.markdown(f"""
                    <div class="compact-card">
                        <div class="card-title-row">
                            <div class="result-card-title">{cert}</div>
                            <span class="tag">更多推荐</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("查看", key=f"job_cert_more_{idx}", use_container_width=True):
                        st.session_state.selected_cert = cert
                        st.session_state.jump_from_job = True
                        st.session_state.nav_selected = "证书导航"
                        st.rerun()
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-title">暂无直接关联证书</div>
            <div class="empty-caption">建议前往「证书导航」页查看更完整的认证地图与推荐路径。</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


if __name__ != "__main__":
    pass
