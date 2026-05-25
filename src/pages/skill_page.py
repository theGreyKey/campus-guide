"""
技能图谱页面
"""


import streamlit as st
import plotly.graph_objects as go
import networkx as nx
from src.utils.data_loader import load_skill_data

def render():
    st.markdown('<h2 style="text-align: center;"><i class="fas fa-project-diagram"></i> 技能关系图谱</h2>', unsafe_allow_html=True)
    
    df = load_skill_data()
    if df.empty:
        return
    
    skills = df["技能"].unique().tolist()
    selected = st.selectbox("🔍 选择核心技能查看关系图", skills)
    
    skill_data = df[df["技能"] == selected]
    if skill_data.empty:
        st.warning(f"未找到「{selected}」的关联数据")
        return
    
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
    
    # 节点
    nx_, ny_, ntext, ncolor, nsize = [], [], [], [], []
    for node in G.nodes():
        x, y = pos[node]
        nx_.append(x)
        ny_.append(y)
        ntext.append(node)
        
        t = G.nodes[node]["type"]
        if t == "skill":
            ncolor.append("#2A5C8A")
            nsize.append(50)
        elif t == "course":
            ncolor.append("#5BA0C8")
            nsize.append(32)
        else:
            ncolor.append("#E8A87C")
            nsize.append(35)
    
    # 边
    ex, ey = [], []
    for e in G.edges():
        x0, y0 = pos[e[0]]
        x1, y1 = pos[e[1]]
        ex.extend([x0, x1, None])
        ey.extend([y0, y1, None])
    
    edge_trace = go.Scatter(x=ex, y=ey, mode='lines', line=dict(width=1.5, color='#94A3B8'), hoverinfo='none')
    node_trace = go.Scatter(
        x=nx_, y=ny_, mode='markers+text', text=ntext, textposition="top center",
        textfont=dict(size=11, color="#1E2A3A"),
        marker=dict(size=nsize, color=ncolor, line=dict(width=2, color='white'), opacity=0.9)
    )
    
    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title=dict(text=f"{selected} 技能关系图谱", x=0.5, font=dict(size=20, color="#2A5C8A")),
        showlegend=False, height=700,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        annotations=[dict(text="🔵 深蓝：核心技能 | 🔷 浅蓝：课程 | 🟠 橙色：岗位",
                          xref="paper", yref="paper", x=0.5, y=-0.1, showarrow=False,
                          font=dict(size=12, color="#A8D8EA"))]
    )
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("📋 查看技能关联详情"):
        st.dataframe(skill_data, use_container_width=True, hide_index=True)