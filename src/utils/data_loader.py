"""
数据加载模块 - 无提示版本
"""
import streamlit as st
import pandas as pd
from config.settings import COURSE_PATH, JOB_PATH, SKILL_PATH, CERT_PATH

@st.cache_data
def load_course_data():
    try:
        df = pd.read_excel(COURSE_PATH)
        return df
    except Exception as e:
        st.error(f"课程表加载失败：{e}")
        return pd.DataFrame()

@st.cache_data
def load_job_data():
    try:
        df = pd.read_excel(JOB_PATH)
        return df
    except Exception as e:
        st.error(f"职业表加载失败：{e}")
        return pd.DataFrame()

@st.cache_data
def load_skill_data():
    try:
        df = pd.read_excel(SKILL_PATH)
        return df
    except Exception as e:
        st.error(f"技能表加载失败：{e}")
        return pd.DataFrame()

@st.cache_data
def load_cert_data():
    try:
        df = pd.read_excel(CERT_PATH)
        return df
    except Exception as e:
        st.error(f"证书表加载失败：{e}")
        return pd.DataFrame()

def safe_get(row, col, default="暂无"):
    try:
        if col not in row.index:
            return default
        val = row[col]
        if pd.isna(val):
            return default
        return val
    except:
        return default

def parse_rating(val):
    if isinstance(val, (int, float)):
        return val
    if isinstance(val, str):
        if "高" in val:
            return 8
        if "中" in val:
            return 5
        if "低" in val:
            return 3
    return 5