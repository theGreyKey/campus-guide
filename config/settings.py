"""
项目配置文件 - 存放所有路径和常量
"""


from pathlib import Path

# 项目根目录
ROOT_DIR = Path(__file__).parent.parent

# 数据目录
DATA_DIR = ROOT_DIR / "data"

# Excel 文件路径（使用相对路径）
COURSE_PATH = DATA_DIR / "课程表.xlsx"
JOB_PATH = DATA_DIR / "职业表.xlsx"
SKILL_PATH = DATA_DIR / "技能表.xlsx"
CERT_PATH = DATA_DIR / "证书表.xlsx"

# 主题颜色
THEME = {
    "primary": "#2A5C8A",
    "primary_light": "#4A7CAA",
    "primary_dark": "#1A4C7A",
    "secondary": "#5BA0C8",
    "accent": "#E8A87C",
    "bg": "#F5F7FA",
    "card_bg": "#FFFFFF",
    "text": "#1E2A3A",
    "text_light": "#6B7A8A",
    "border": "#E2E8F0"
}

# 证书间关联关系
CERTIFICATE_LINKS = [
    ("CQF", "Python数据分析", 0.8),
    ("CQF", "FRM", 0.7),
    ("CQF", "机器学习", 0.8),
    ("CFA", "FRM", 0.6),
    ("CFA", "FMVA®", 0.7),
    ("FRM", "SHMFTPP", 0.5),
    ("SHMFTPP", "银行金融科技基础", 0.6),
    ("机器学习", "DeepLearning.AI", 0.9),
    ("机器学习", "Kaggle", 0.7),
    ("DeepLearning.AI", "AI工程师", 0.7),
    ("Python数据分析", "Kaggle", 0.6),
    ("Python数据分析", "Tableau/Power BI", 0.5),
    ("CPA", "ACCA", 0.5),
    ("SOA", "中国精算师", 0.6),
]

# 路线图数据
ROADMAPS = {
    "金科量化路线": {
        "certificates": ["Python数据分析", "CQF", "机器学习", "Kaggle"],
        "description": "专注于量化交易、算法策略开发的路线",
        "careers": ["量化研究员", "算法交易工程师", "金融数据 Scientist"]
    },
    "风控专家路线": {
        "certificates": ["FRM", "Python数据分析", "SHMFTPP"],
        "description": "专注于金融风险管理、合规风控的路线",
        "careers": ["风控建模工程师", "反洗钱分析师", "金融风险管理师"]
    },
    "金融科技产品路线": {
        "certificates": ["SHMFTPP", "FMVA®", "银行金融科技基础"],
        "description": "专注于金融科技产品设计、业务分析的路线",
        "careers": ["金融产品经理", "商业分析师", "金融科技咨询顾问"]
    },
    "AI金融路线": {
        "certificates": ["机器学习", "DeepLearning.AI", "AI工程师", "Kaggle"],
        "description": "专注于AI在金融领域应用的路线",
        "careers": ["金融AI工程师", "金融数据科学家", "机器学习工程师"]
    },
    "数据分析路线": {
        "certificates": ["Python数据分析", "Tableau/Power BI", "Kaggle"],
        "description": "专注于金融数据分析、可视化的路线",
        "careers": ["数据分析师", "商业分析师", "数据科学家"]
    }
}

# 证书推荐规则库
RECOMMENDATION_RULES = {
    "量化方向": {
        "keywords": ["数学", "编程", "量化", "算法"],
        "mbti": ["INTJ", "INTP"],
        "certificates": ["CQF", "Python数据分析", "机器学习", "Kaggle"],
        "route": "金科量化路线"
    },
    "风控方向": {
        "keywords": ["稳定", "风险", "合规", "银行"],
        "mbti": ["ISTJ", "ISTP", "INTJ"],
        "certificates": ["FRM", "Python数据分析", "SHMFTPP"],
        "route": "风控专家路线"
    },
    "产品方向": {
        "keywords": ["沟通", "产品", "业务", "设计"],
        "mbti": ["ENTJ", "ENFJ", "ENTP", "ENFP"],
        "certificates": ["SHMFTPP", "FMVA®", "银行金融科技基础"],
        "route": "金融科技产品路线"
    },
    "AI方向": {
        "keywords": ["AI", "人工智能", "深度学习", "算法"],
        "mbti": ["INTP", "INTJ"],
        "certificates": ["机器学习", "DeepLearning.AI", "AI工程师", "Kaggle"],
        "route": "AI金融路线"
    },
    "数据分析方向": {
        "keywords": ["数据", "分析", "统计", "可视化"],
        "mbti": ["ISTJ", "INTJ", "INFJ"],
        "certificates": ["Python数据分析", "Tableau/Power BI", "Kaggle"],
        "route": "数据分析路线"
    }
}