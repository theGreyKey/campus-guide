# setup.py
from setuptools import setup, find_packages

setup(
    name="fintech-navigation",
    version="1.0.0",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "streamlit>=1.28.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "plotly>=5.17.0",
        "networkx>=3.0",
        "openpyxl>=3.1.0",
    ],
)
