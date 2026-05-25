# Fintech Guide

Python Streamlit 金融科技导航系统。

## 本地 Python 环境

本项目不依赖 conda，使用项目目录内的 `.venv` 虚拟环境即可。

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

运行应用：

```powershell
streamlit run app.py
```

如需开发本地包导入：

```powershell
pip install -e .
```

## 项目结构

- `app.py`：Streamlit 应用入口。
- `src/pages/`：页面模块。
- `src/utils/`：共享工具和数据加载逻辑。
- `config/settings.py`：路径、主题、路线图和推荐规则配置。
- `data/`：Excel 数据源。
