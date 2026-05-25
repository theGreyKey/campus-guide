"""
课程地图页面
"""
import streamlit as st
import plotly.graph_objects as go
from src.utils.data_loader import load_course_data, safe_get

def render():
    st.markdown('<h2><i class="fas fa-map"></i> 金融科技课程地图</h2>', unsafe_allow_html=True)
    
    df = load_course_data()
    if df.empty:
        return
    
    courses = df["课程名称"].tolist()
    selected = st.selectbox("🔍 选择课程查看详情", courses)
    info = df[df["课程名称"] == selected].iloc[0]
    
    # 指标卡片
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("📅 开课学期", safe_get(info, "开课学期"))
    with c2:
        st.metric("📖 学分", safe_get(info, "学分"))
    with c3:
        st.metric("⚡ 综合难度", f"{safe_get(info, '难度(1-10)', 5)}/10")
    with c4:
        st.metric("🏷️ 课程类别", safe_get(info, "课程类别"))
    
    st.markdown("---")
    
    # 雷达图
    st.markdown('<div class="chart-title">🧠 课程能力画像</div>', unsafe_allow_html=True)
    
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
        line=dict(color="#2A5C8A", width=3),
        fillcolor='rgba(42,92,138,0.2)'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(range=[0, 10])),
        showlegend=False,
        height=450,
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
    
    # 强度分析
    st.subheader("🔥 课程强度分析")
    c1, c2 = st.columns(2)
    with c1:
        st.progress(safe_get(info, "数学强度(1-10)", 5) / 10)
        st.write(f"📐 **数学强度**：{safe_get(info, '数学强度(1-10)', 5)}/10")
        st.progress(safe_get(info, "编程强度(1-10)", 5) / 10)
        st.write(f"💻 **编程强度**：{safe_get(info, '编程强度(1-10)', 5)}/10")
    with c2:
        st.progress(safe_get(info, "难度(1-10)", 5) / 10)
        st.write(f"⚡ **课程难度**：{safe_get(info, '难度(1-10)', 5)}/10")
        st.progress(pressure / 10)
        st.write(f"💪 **学习压力**：{safe_get(info, '学习压力等级')}")
    
    st.markdown("---")
    
    # 课程详情
    st.subheader("📘 课程详情")
    st.markdown(f"""
    <div class="detail-list">
        <div class="detail-item"><div class="detail-icon"><i class="fas fa-book"></i></div>
            <div class="detail-label">课程名称</div><div class="detail-value">{safe_get(info, '课程名称')}</div></div>
        <div class="detail-item"><div class="detail-icon"><i class="fas fa-tag"></i></div>
            <div class="detail-label">课程类别</div><div class="detail-value">{safe_get(info, '课程类别')}</div></div>
        <div class="detail-item"><div class="detail-icon"><i class="fas fa-lightbulb"></i></div>
            <div class="detail-label">实际用途</div><div class="detail-value">{safe_get(info, '实际用途')}</div></div>
        <div class="detail-item"><div class="detail-icon"><i class="fas fa-briefcase"></i></div>
            <div class="detail-label">对应职业方向</div><div class="detail-value">{safe_get(info, '对应职业方向')}</div></div>
    </div>
    """, unsafe_allow_html=True)