"""
技能图谱页面
"""


import streamlit as st
import plotly.graph_objects as go
import networkx as nx
from src.utils.data_loader import load_skill_data

def render():
    st.markdown('<div class="page-shell">', unsafe_allow_html=True)

    df = load_skill_data()
    if df.empty:
        st.markdown('</div>', unsafe_allow_html=True)
        return

    skills = df["技能"].unique().tolist()
    selected = st.selectbox("选择核心技能查看关系图", skills)

    skill_data = df[df["技能"] == selected]
    if skill_data.empty:
        st.warning(f"未找到「{selected}」的关联数据")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    st.markdown(f"""
    <div class="page-hero">
        <div class="hero-grid">
            <div>
                <div class="section-kicker">Skill graph dossier</div>
                <h2>{selected}</h2>
                <p class="section-caption">围绕一个核心技能，同时查看其对应课程与岗位，帮助你判断知识如何转化为职业能力。</p>
                <div class="tag-row" style="margin-top:0.9rem;">
                    <span class="tag tag-primary">核心技能</span>
                    <span class="tag">课程连接</span>
                    <span class="tag tag-accent">岗位出口</span>
                </div>
            </div>
            <div class="panel-card">
                <div class="eyebrow-text">Graph reading</div>
                <div class="card-title">把技能放进课程与岗位的中间层看</div>
                <div class="card-caption">这页更像能力关系图谱，而不是单纯网络图：它帮助你看清一项技能连接哪些课程、又能流向哪些职业方向。</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    G = nx.Graph()
    G.add_node(selected, type="skill")

    for _, row in skill_data.iterrows():
        course = row["来源课程"]
        job = row["对应岗位"]
        G.add_node(course, type="course")
        G.add_edge(course, selected)
        G.add_node(job, type="job")
        G.add_edge(selected, job)

    try:
        pos = nx.spring_layout(G, seed=42, k=1.5)
    except:
        pos = nx.circular_layout(G)

    nx_, ny_, ntext, ncolor, nsize = [], [], [], [], []
    for node in G.nodes():
        x, y = pos[node]
        nx_.append(x)
        ny_.append(y)
        ntext.append(node)

        t = G.nodes[node]["type"]
        if t == "skill":
            ncolor.append("#4A95FF")
            nsize.append(50)
        elif t == "course":
            ncolor.append("#7DE2D1")
            nsize.append(32)
        else:
            ncolor.append("#E0B56A")
            nsize.append(35)

    ex, ey = [], []
    for e in G.edges():
        x0, y0 = pos[e[0]]
        x1, y1 = pos[e[1]]
        ex.extend([x0, x1, None])
        ey.extend([y0, y1, None])

    edge_trace = go.Scatter(x=ex, y=ey, mode='lines', line=dict(width=1.5, color='rgba(148,175,206,0.26)'), hoverinfo='none')
    node_trace = go.Scatter(
        x=nx_, y=ny_, mode='markers+text', text=ntext, textposition="top center",
        textfont=dict(size=11, color="#EAF2FB"),
        marker=dict(size=nsize, color=ncolor, line=dict(width=2, color='rgba(255,255,255,0.85)'), opacity=0.95)
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title=dict(text=f"{selected} 技能关系图谱", x=0.5, font=dict(size=20, color="#EAF2FB")),
        showlegend=False, height=700,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        annotations=[dict(text="蓝色：核心技能 | 青色：课程 | 金色：岗位",
                          xref="paper", yref="paper", x=0.5, y=-0.1, showarrow=False,
                          font=dict(size=12, color="#95A8BE"))],
        font=dict(color="#EAF2FB")
    )
    st.markdown("""
    <div class="chart-frame">
        <div class="chart-header">
            <div>
                <div class="chart-title">技能关系图谱</div>
                <div class="chart-caption">从课程到技能，再到岗位，帮助你理解知识如何转化为职业能力。</div>
            </div>
            <span class="tag tag-primary">Graph module</span>
        </div>
    """, unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-strip">
        <div class="metric-item">
            <div class="metric-label">Linked courses</div>
            <div class="metric-value">{skill_data['来源课程'].nunique()}</div>
            <div class="metric-note">关联课程数量</div>
        </div>
        <div class="metric-item">
            <div class="metric-label">Linked roles</div>
            <div class="metric-value">{skill_data['对应岗位'].nunique()}</div>
            <div class="metric-note">关联岗位数量</div>
        </div>
        <div class="metric-item">
            <div class="metric-label">Records</div>
            <div class="metric-value">{len(skill_data)}</div>
            <div class="metric-note">当前技能关系记录数</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-header">
        <div class="section-kicker">Detail table</div>
        <div class="section-title">技能关联详情</div>
        <p class="section-caption">展开后可查看该技能与课程、岗位之间的完整对应表。</p>
    </div>
    """, unsafe_allow_html=True)
    with st.expander("查看技能关联详情"):
        st.dataframe(skill_data, use_container_width=True, hide_index=True)

    st.markdown('</div>', unsafe_allow_html=True)
