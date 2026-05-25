"""
课程地图页面
"""
import streamlit as st
import plotly.graph_objects as go
from src.utils.data_loader import load_course_data, safe_get

def render():
    st.markdown('<div class="page-shell">', unsafe_allow_html=True)

    df = load_course_data()
    if df.empty:
        st.markdown('</div>', unsafe_allow_html=True)
        return

    courses = df["课程名称"].tolist()
    selected = st.selectbox("选择课程查看详情", courses)
    info = df[df["课程名称"] == selected].iloc[0]

    st.markdown(f"""
    <div class="page-hero">
        <div class="hero-grid">
            <div>
                <div class="section-kicker">Course dossier</div>
                <h2>{selected}</h2>
                <p class="section-caption">把课程从单纯的图表页升级为课程画像：先看关键信号，再看能力雷达、强度分析与课程详情。</p>
                <div class="tag-row" style="margin-top:0.9rem;">
                    <span class="tag tag-primary">{safe_get(info, '开课学期')}</span>
                    <span class="tag tag-accent">{safe_get(info, '课程类别')}</span>
                </div>
            </div>
            <div class="panel-card">
                <div class="eyebrow-text">Course focus</div>
                <div class="card-title">判断这门课值得投入多少精力</div>
                <div class="card-caption">通过学分、难度、数学与编程强度，快速判断它在你的成长路径中属于基础课、支撑课还是关键课。</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-strip">
        <div class="metric-item"><div class="metric-label">Semester</div><div class="metric-value">{safe_get(info, '开课学期')}</div><div class="metric-note">开课学期</div></div>
        <div class="metric-item"><div class="metric-label">Credits</div><div class="metric-value">{safe_get(info, '学分')}</div><div class="metric-note">课程学分</div></div>
        <div class="metric-item"><div class="metric-label">Difficulty</div><div class="metric-value">{safe_get(info, '难度(1-10)', 5)}/10</div><div class="metric-note">综合难度</div></div>
        <div class="metric-item"><div class="metric-label">Category</div><div class="metric-value">{safe_get(info, '课程类别')}</div><div class="metric-note">课程类别</div></div>
    </div>
    """, unsafe_allow_html=True)

    categories = ["数学强度", "编程强度", "课程难度", "实际用途", "学习压力"]
    pressure_map = {"低": 3, "中": 6, "高": 9}
    pressure = pressure_map.get(safe_get(info, "学习压力等级"), 5)

    values = [
        safe_get(info, "数学强度(1-10)", 5),
        safe_get(info, "编程强度(1-10)", 5),
        safe_get(info, "难度(1-10)", 5),
        8,
        pressure
    ]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        line=dict(color="#4A95FF", width=3),
        fillcolor='rgba(62,139,255,0.18)'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(range=[0, 10], gridcolor='rgba(148,175,206,0.18)', linecolor='rgba(148,175,206,0.18)', tickfont=dict(color="#95A8BE"))),
        showlegend=False,
        height=450,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#EAF2FB")
    )
    st.markdown("""
    <div class="chart-frame">
        <div class="chart-header">
            <div>
                <div class="chart-title">课程能力画像</div>
                <div class="chart-caption">从数学、编程、难度、用途与学习压力五个维度观察课程特征，越接近外圈代表强度越高。</div>
            </div>
            <span class="tag tag-primary">Radar profile</span>
        </div>
    """, unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="section-header">
        <div class="section-kicker">Intensity analysis</div>
        <div class="section-title">课程强度分析</div>
        <p class="section-caption">把关键强度拆开看，帮助你安排学习节奏与预期投入。</p>
    </div>
    """, unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.progress(safe_get(info, "数学强度(1-10)", 5) / 10)
        st.write(f"**数学强度**：{safe_get(info, '数学强度(1-10)', 5)}/10")
        st.progress(safe_get(info, "编程强度(1-10)", 5) / 10)
        st.write(f"**编程强度**：{safe_get(info, '编程强度(1-10)', 5)}/10")
    with c2:
        st.progress(safe_get(info, "难度(1-10)", 5) / 10)
        st.write(f"**课程难度**：{safe_get(info, '难度(1-10)', 5)}/10")
        st.progress(pressure / 10)
        st.write(f"**学习压力**：{safe_get(info, '学习压力等级')}")

    st.markdown("""
    <div class="section-header">
        <div class="section-kicker">Detail dossier</div>
        <div class="section-title">课程详情</div>
        <p class="section-caption">查看课程定位、实际用途与潜在对应职业方向。</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div class="detail-list">
        <div class="detail-item"><div class="detail-label">课程名称</div><div class="detail-value">{safe_get(info, '课程名称')}</div></div>
        <div class="detail-item"><div class="detail-label">课程类别</div><div class="detail-value">{safe_get(info, '课程类别')}</div></div>
        <div class="detail-item"><div class="detail-label">实际用途</div><div class="detail-value">{safe_get(info, '实际用途')}</div></div>
        <div class="detail-item"><div class="detail-label">职业方向</div><div class="detail-value">{safe_get(info, '对应职业方向')}</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
