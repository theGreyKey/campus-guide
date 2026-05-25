"""
成长路线定制页面
"""


import streamlit as st
import pandas as pd
from src.utils.data_loader import load_job_data, load_cert_data, safe_get

def render():
    st.markdown('<h2 style="text-align: center;"><i class="fas fa-road"></i> 专业成长路线定制</h2>', unsafe_allow_html=True)
    
    job_df = load_job_data()
    cert_df = load_cert_data()
    
    st.markdown("""
    <div class="white-card">
        <p style="font-size: 1.1rem; color: #1E2A3A;">🎯 根据你的目标和偏好，定制专属成长路线</p>
        <p style="color: #5BA0C8;">填写以下信息，AI 将为你生成个性化的学习路径和证书规划</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        career_goal = st.selectbox("🎯 职业目标", 
            ["量化交易", "风险管理", "金融产品", "AI开发", "数据分析", "不确定"])
        
        math_level = st.select_slider("📐 数学能力", ["较弱", "一般", "较强", "很强"])
        prog_level = st.select_slider("💻 编程能力", ["无基础", "基础", "熟练", "精通"])
        
    with col2:
        available_time = st.select_slider("⏰ 每周可投入时间", ["<5小时", "5-10小时", "10-20小时", ">20小时"])
        target_time = st.selectbox("🎯 目标考证时间", ["3个月内", "6个月内", "1年内", "2年内"])
        preferred_industry = st.multiselect("🏢 偏好行业", ["银行", "证券/基金", "保险", "互联网金融", "金融科技公司", "咨询"])
    
    # 性格标签
    st.markdown("##### 🧠 性格/偏好（可多选）")
    personality_cols = st.columns(4)
    personality_options = ["喜欢钻研", "喜欢与人沟通", "追求稳定", "喜欢挑战", "注重细节", "有创造力", "逻辑性强", "抗压能力强"]
    selected_personality = []
    
    for idx, opt in enumerate(personality_options):
        with personality_cols[idx % 4]:
            if st.checkbox(opt, key=f"person_{idx}"):
                selected_personality.append(opt)
    
    generate_btn = st.button("✨ 生成我的成长路线", use_container_width=True, type="primary")
    
    if generate_btn:
        st.markdown("---")
        st.markdown("## 📋 你的专属成长路线")
        
        # 根据输入推荐方向
        if career_goal == "量化交易" or (math_level in ["较强", "很强"] and prog_level in ["熟练", "精通"]):
            direction = "quant"
            direction_name = "金科量化路线"
            certs = ["Python数据分析", "CQF", "机器学习", "Kaggle"]
            skills = ["Python编程", "概率统计", "随机过程", "金融工程", "机器学习"]
            courses = ["程序设计", "概率论与数理统计", "随机过程", "金融工程学A", "金融机器学习R"]
            
        elif career_goal == "风险管理" or "稳定" in selected_personality:
            direction = "risk"
            direction_name = "风控专家路线"
            certs = ["FRM", "Python数据分析", "SHMFTPP"]
            skills = ["Python编程", "SQL", "统计学", "信用风险建模", "反欺诈"]
            courses = ["概率论与数理统计", "金融风险管理E", "机器学习", "大数据分析"]
            
        elif career_goal == "金融产品" or "喜欢与人沟通" in selected_personality:
            direction = "product"
            direction_name = "金融科技产品路线"
            certs = ["SHMFTPP", "FMVA®", "银行金融科技基础"]
            skills = ["金融科技通识", "产品设计", "需求分析", "商业分析", "项目管理"]
            courses = ["金融科技概论", "银行数字化转型", "金融科技创新与监管"]
            
        elif career_goal == "AI开发" or ("喜欢挑战" in selected_personality and prog_level in ["熟练", "精通"]):
            direction = "ai"
            direction_name = "AI金融路线"
            certs = ["机器学习", "DeepLearning.AI", "AI工程师", "Kaggle"]
            skills = ["Python编程", "机器学习", "深度学习", "LLM应用", "PyTorch/TensorFlow"]
            courses = ["机器学习", "大语言模型的金融应用", "深度学习", "数据结构"]
            
        else:
            direction = "data"
            direction_name = "数据分析路线"
            certs = ["Python数据分析", "Tableau/Power BI", "Kaggle"]
            skills = ["Python编程", "SQL", "数据可视化", "统计学", "业务分析"]
            courses = ["程序设计", "概率论与数理统计", "大数据分析与挖掘"]
        
        # 时间规划
        if target_time == "3个月内":
            certs = certs[:1]
        elif target_time == "6个月内":
            certs = certs[:2]
        
        # 显示路线 - 改为白色背景，带浅蓝色边框
        st.markdown(f"""
        <div style="background: #FFFFFF; border-radius: 16px; padding: 1.2rem; margin-bottom: 1rem; border: 1px solid #C0D9E8; border-left: 4px solid #2A5C8A; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <div style="font-size: 1.3rem; font-weight: 700; color: #2A5C8A;">✨ {direction_name}</div>
            <div style="margin-top: 8px; color: #1E2A3A;">基于你的输入，推荐最适合的发展方向</div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="white-card">
                <h4>📅 学习时间线</h4>
            </div>
            """, unsafe_allow_html=True)
            
            stages = ["第一阶段：基础准备", "第二阶段：技能提升", "第三阶段：考证冲刺", "第四阶段：实习/就业"]
            for i, stage in enumerate(stages):
                with st.expander(stage):
                    if i == 0:
                        st.write("📚 学习课程：" + ", ".join(courses[:2]))
                        st.write("🎯 目标：掌握基础编程和数学")
                    elif i == 1:
                        st.write("📚 学习课程：" + ", ".join(courses[2:4] if len(courses) > 2 else courses))
                        st.write("🎯 目标：完成项目实战")
                    elif i == 2:
                        st.write("🎓 推荐证书：" + ", ".join(certs))
                        st.write("🎯 目标：考取核心证书")
                    else:
                        st.write("💼 目标岗位：" + direction_name)
                        st.write("🎯 目标：积累实习经验，准备面试")
        
        with col2:
            st.markdown("""
            <div class="white-card">
                <h4>📚 核心技能清单</h4>
            </div>
            """, unsafe_allow_html=True)
            for skill in skills:
                st.markdown(f"- ✅ {skill}")
            
            st.markdown("""
            <div class="white-card" style="margin-top: 20px;">
                <h4>🎓 推荐证书</h4>
            </div>
            """, unsafe_allow_html=True)
            for cert in certs:
                st.markdown(f"- 🏅 {cert}")
        
        # 个性化建议
        st.markdown("---")
        st.markdown("#### 💡 个性化发展建议")
        
        suggestions = []
        if math_level == "较弱":
            suggestions.append("📐 建议先加强数学基础，可以学习《高等数学》和《概率论》网课")
        if prog_level == "无基础":
            suggestions.append("💻 建议从Python入门，完成《Python编程从入门到实践》")
        if available_time == "<5小时":
            suggestions.append("⏰ 时间有限，建议制定每周固定学习计划，保持持续性")
        if "银行" in preferred_industry:
            suggestions.append("🏦 银行方向建议考取FRM、银行从业资格证")
        if "量化交易" in career_goal:
            suggestions.append("📈 量化方向建议多参与Kaggle竞赛积累实战经验")
        
        if not suggestions:
            suggestions.append("🎉 你的基础条件很好，建议尽早开始准备相关证书和实习")
        
        for s in suggestions:
            st.info(s)
        
        # 推荐资源
        st.markdown("---")
        st.markdown("#### 📖 推荐学习资源")
        resource_cols = st.columns(3)
        resources = [
            ("📚 Coursera", "机器学习/深度学习课程"),
            ("📊 Kaggle", "数据科学竞赛平台"),
            ("🎓 中国大学MOOC", "国内名校课程")
        ]
        for idx, (name, desc) in enumerate(resources):
            with resource_cols[idx]:
                st.markdown(f"**{name}**\n{desc}")
    
    elif generate_btn:
        st.warning("请填写完整信息")