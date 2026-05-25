"""
工具函数
"""


import streamlit as st


def load_css():
    """加载CSS样式"""
    st.markdown("""
    <style>
    :root {
        --bg: #07111F;
        --bg-muted: #0C1727;
        --surface: rgba(10, 20, 34, 0.92);
        --surface-strong: rgba(13, 25, 42, 0.97);
        --surface-muted: rgba(18, 32, 49, 0.88);
        --surface-soft: rgba(17, 31, 48, 0.72);
        --surface-tint: rgba(24, 42, 66, 0.82);
        --surface-glass: rgba(8, 18, 31, 0.72);
        --ink: #F4F8FC;
        --ink-soft: #D7E2EE;
        --muted: #95A8BE;
        --line: rgba(138, 164, 193, 0.18);
        --line-strong: rgba(148, 175, 206, 0.32);
        --primary: #3E8BFF;
        --primary-dark: #2B6FD4;
        --primary-soft: rgba(62, 139, 255, 0.16);
        --accent: #7DE2D1;
        --accent-soft: rgba(125, 226, 209, 0.14);
        --gold: #E0B56A;
        --gold-soft: rgba(224, 181, 106, 0.16);
        --danger: #E37C86;
        --shadow: 0 24px 60px rgba(0, 0, 0, 0.36);
        --shadow-soft: 0 14px 34px rgba(0, 0, 0, 0.24);
        --radius-xl: 28px;
        --radius-lg: 22px;
        --radius-md: 18px;
        --radius-sm: 12px;
        --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(62, 139, 255, 0.16), transparent 34%),
            radial-gradient(circle at top right, rgba(125, 226, 209, 0.12), transparent 28%),
            linear-gradient(180deg, #091423 0%, #07111F 42%, #050D17 100%);
    }

    .stApp, .main, .block-container {
        color: var(--ink) !important;
        font-family: "Inter", "Segoe UI", "Microsoft YaHei", sans-serif;
    }

    .main .block-container {
        max-width: 1240px;
        padding-top: 1.2rem;
        padding-bottom: 3.5rem;
    }

    h1, h2, h3, h4, h5, h6,
    p, li, span, div,
    label, .stSelectbox label, .stTextInput label, .stTextArea label {
        color: inherit !important;
        letter-spacing: 0 !important;
    }

    h2 {
        font-size: 1.9rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
    }

    h3 {
        font-size: 1.24rem !important;
        font-weight: 650 !important;
    }

    [data-testid="stSidebarCollapsedControl"] {
        display: none !important;
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }

    .stSelectbox div[data-baseweb="select"],
    .stMultiSelect div[data-baseweb="select"],
    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input,
    .stDateInput input,
    .stTimeInput input {
        background: rgba(7, 17, 31, 0.72) !important;
        color: var(--ink) !important;
        border: 1px solid var(--line) !important;
        border-radius: 14px !important;
        box-shadow: none !important;
        transition: border-color 160ms var(--ease-out), box-shadow 160ms var(--ease-out), background 160ms var(--ease-out);
    }

    .stSelectbox div[data-baseweb="select"] > div,
    .stMultiSelect div[data-baseweb="select"] div,
    .stSelectbox div[data-baseweb="select"] div[role="button"] span {
        background: transparent !important;
        color: var(--ink) !important;
        font-weight: 500 !important;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus,
    .stNumberInput input:focus,
    .stSelectbox div[data-baseweb="select"]:focus-within,
    .stMultiSelect div[data-baseweb="select"]:focus-within {
        border-color: rgba(62, 139, 255, 0.7) !important;
        box-shadow: 0 0 0 3px rgba(62, 139, 255, 0.16) !important;
        background: rgba(10, 20, 34, 0.94) !important;
    }

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #6F8399 !important;
    }

    .stSelectbox svg {
        fill: var(--primary) !important;
    }

    div[data-baseweb="popover"] ul {
        background: rgba(9, 18, 31, 0.98) !important;
        border: 1px solid var(--line) !important;
        border-radius: 14px !important;
        box-shadow: var(--shadow) !important;
    }

    div[data-baseweb="popover"] li {
        background: transparent !important;
        color: var(--ink) !important;
        font-weight: 500 !important;
    }

    div[data-baseweb="popover"] li:hover {
        background: rgba(62, 139, 255, 0.12) !important;
    }

    div[data-baseweb="popover"] li[aria-selected="true"] {
        background: var(--primary) !important;
        color: #FFFFFF !important;
    }

    .stSlider label,
    .stCheckbox label span,
    .stRadio label span {
        color: var(--ink) !important;
    }

    .stSlider div[data-baseweb="slider"] div[data-testid="stSliderThumb"] {
        background-color: var(--primary) !important;
        border: 2px solid #FFFFFF !important;
        box-shadow: 0 4px 14px rgba(62, 139, 255, 0.28) !important;
    }

    .stSlider div[data-baseweb="slider"] div[role="slider"] + div {
        background-color: var(--primary) !important;
    }

    .stCheckbox label span[data-baseweb="checkbox"] {
        border-color: rgba(62, 139, 255, 0.8) !important;
        background: rgba(7, 17, 31, 0.72) !important;
    }

    .app-hero {
        position: relative;
        overflow: hidden;
        display: grid;
        grid-template-columns: minmax(0, 1.4fr) minmax(280px, 0.9fr);
        gap: 1.35rem;
        align-items: stretch;
        padding: 1.65rem 1.7rem;
        margin-bottom: 1rem;
        border: 1px solid var(--line-strong);
        border-radius: var(--radius-xl);
        background:
            linear-gradient(135deg, rgba(16, 30, 50, 0.98) 0%, rgba(10, 20, 34, 0.95) 62%, rgba(8, 16, 28, 0.98) 100%);
        box-shadow: var(--shadow);
    }

    .app-hero::before {
        content: "";
        position: absolute;
        inset: 0;
        background:
            radial-gradient(circle at 14% 18%, rgba(62, 139, 255, 0.2), transparent 28%),
            radial-gradient(circle at 85% 16%, rgba(125, 226, 209, 0.12), transparent 22%);
        pointer-events: none;
    }

    .main-title,
    .hero-panel {
        position: relative;
        z-index: 1;
    }

    .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.35rem 0.72rem;
        border-radius: 999px;
        background: rgba(62, 139, 255, 0.12);
        border: 1px solid rgba(62, 139, 255, 0.2);
        color: #A9CAFF !important;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.08em !important;
        text-transform: uppercase;
    }

    .main-title h1 {
        color: var(--ink) !important;
        font-size: clamp(2.2rem, 3.8vw, 3.15rem) !important;
        font-weight: 760 !important;
        line-height: 1.03 !important;
        margin: 0.88rem 0 0 !important;
    }

    .sub-title {
        max-width: 720px;
        color: var(--ink-soft) !important;
        font-size: 1rem;
        line-height: 1.72;
        margin-top: 0.85rem;
    }

    .hero-meta {
        display: flex;
        gap: 0.7rem;
        flex-wrap: wrap;
        margin-top: 1rem;
    }

    .hero-meta .badge {
        background: rgba(255,255,255,0.04);
        color: var(--ink-soft) !important;
        border: 1px solid rgba(148, 175, 206, 0.14);
    }

    .hero-panel {
        display: grid;
        gap: 0.85rem;
        align-content: stretch;
    }

    .hero-panel-card {
        padding: 1rem 1.05rem;
        border-radius: var(--radius-lg);
        border: 1px solid rgba(148, 175, 206, 0.14);
        background: linear-gradient(180deg, rgba(15, 28, 45, 0.84) 0%, rgba(9, 18, 31, 0.9) 100%);
        backdrop-filter: blur(14px);
    }

    .hero-panel-label {
        color: var(--muted) !important;
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.08em !important;
        font-weight: 700;
    }

    .hero-panel-value {
        color: var(--ink) !important;
        font-size: 1.18rem;
        font-weight: 680;
        margin-top: 0.38rem;
    }

    .hero-panel-caption {
        color: var(--muted) !important;
        font-size: 0.85rem;
        line-height: 1.55;
        margin-top: 0.34rem;
    }

    .badge-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.55rem;
    }

    .badge {
        display: inline-flex;
        align-items: center;
        padding: 0.46rem 0.76rem;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid var(--line);
    }

    .page-shell {
        display: flex;
        flex-direction: column;
        gap: 1.1rem;
        margin-bottom: 1rem;
    }

    .page-hero,
    .section-shell,
    .panel-card,
    .insight-card,
    .timeline-card,
    .recommendation-card,
    .metric-strip,
    .chart-frame,
    .empty-state,
    .form-shell,
    .jump-notice,
    .guide-card,
    .white-card,
    .card,
    .clickable-card,
    .search-result-card,
    .recommend-card,
    .job-card,
    .compact-card,
    .interactive-card,
    .result-card,
    .resource-card,
    .detail-list {
        background: linear-gradient(180deg, rgba(13, 25, 42, 0.96) 0%, rgba(9, 18, 31, 0.96) 100%) !important;
        border: 1px solid var(--line) !important;
        border-radius: var(--radius-lg) !important;
        box-shadow: var(--shadow-soft) !important;
    }

    .page-hero {
        position: relative;
        overflow: hidden;
        padding: 1.5rem 1.55rem;
    }

    .page-hero::after {
        content: "";
        position: absolute;
        right: -4%;
        top: -30%;
        width: 240px;
        height: 240px;
        background: radial-gradient(circle, rgba(62, 139, 255, 0.14), transparent 68%);
        pointer-events: none;
    }

    .hero-grid {
        display: grid;
        grid-template-columns: minmax(0, 1.4fr) minmax(260px, 0.8fr);
        gap: 1rem;
        align-items: start;
    }

    .section-shell,
    .panel-card,
    .insight-card,
    .timeline-card,
    .recommendation-card,
    .form-shell,
    .guide-card,
    .white-card,
    .card,
    .clickable-card,
    .search-result-card,
    .recommend-card,
    .job-card,
    .compact-card,
    .interactive-card,
    .result-card,
    .resource-card {
        padding: 1.15rem 1.2rem;
    }

    .compact-card {
        padding: 0.92rem 1rem;
    }

    .section-header {
        display: flex;
        flex-direction: column;
        gap: 0.34rem;
        margin: 0;
    }

    .section-kicker {
        color: #9EC2FF !important;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.08em !important;
        text-transform: uppercase;
    }

    .section-title {
        color: var(--ink) !important;
        font-size: 1.28rem;
        font-weight: 700;
        line-height: 1.24;
    }

    .section-caption,
    .card-caption,
    .card-body-muted,
    .chart-caption,
    .empty-caption,
    .meta-text {
        color: var(--muted) !important;
        font-size: 0.92rem;
        line-height: 1.68;
        margin: 0;
    }

    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, rgba(62, 139, 255, 0.42), rgba(62, 139, 255, 0));
        margin: 0.2rem 0 0.1rem;
    }

    .content-stack,
    .compact-stack {
        display: flex;
        flex-direction: column;
    }

    .content-stack { gap: 1rem; }
    .compact-stack { gap: 0.72rem; }

    .eyebrow-text {
        color: var(--muted) !important;
        font-size: 0.74rem;
        text-transform: uppercase;
        letter-spacing: 0.08em !important;
        font-weight: 700;
    }

    .card-title,
    .card-title-row,
    .result-card-title,
    .search-result-title,
    .job-card-title,
    .recommend-title,
    .chart-title,
    .empty-title {
        color: var(--ink) !important;
        font-weight: 700;
    }

    .card-title,
    .chart-title {
        font-size: 1.02rem;
        margin-bottom: 0.4rem;
    }

    .card-title-row {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 0.8rem;
        margin-bottom: 0.45rem;
    }

    .metric-strip {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 0.95rem;
        padding: 0;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    .metric-item,
    [data-testid="stMetric"] {
        position: relative;
        overflow: hidden;
        background: linear-gradient(180deg, rgba(16, 29, 47, 0.98) 0%, rgba(10, 19, 33, 0.98) 100%) !important;
        border: 1px solid var(--line) !important;
        border-radius: var(--radius-md) !important;
        padding: 1rem 1.05rem;
        text-align: left;
        box-shadow: var(--shadow-soft) !important;
        transition: transform 160ms var(--ease-out), border-color 160ms var(--ease-out), box-shadow 160ms var(--ease-out);
    }

    .metric-item::before,
    [data-testid="stMetric"]::before {
        content: "";
        position: absolute;
        inset: 0 auto auto 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, var(--primary), rgba(125, 226, 209, 0));
    }

    .metric-item:hover,
    [data-testid="stMetric"]:hover,
    .panel-card:hover,
    .insight-card:hover,
    .timeline-card:hover,
    .recommendation-card:hover,
    .guide-card:hover,
    .white-card:hover,
    .card:hover,
    .clickable-card:hover,
    .search-result-card:hover,
    .recommend-card:hover,
    .job-card:hover,
    .compact-card:hover,
    .interactive-card:hover,
    .result-card:hover,
    .resource-card:hover {
        transform: translateY(-2px);
        border-color: rgba(62, 139, 255, 0.34) !important;
        box-shadow: var(--shadow) !important;
    }

    .metric-item { margin-bottom: 0; }

    .metric-value,
    [data-testid="stMetricValue"] {
        color: var(--ink) !important;
        font-weight: 760 !important;
    }

    .metric-value { font-size: 1.45rem; }

    .metric-label,
    [data-testid="stMetricLabel"] {
        color: var(--muted) !important;
        font-size: 0.8rem;
        margin-top: 0.3rem;
    }

    .metric-note {
        color: var(--muted) !important;
        font-size: 0.82rem;
        margin-top: 0.4rem;
        line-height: 1.55;
    }

    .detail-list {
        padding: 0.3rem 0;
    }

    .detail-item {
        display: flex;
        padding: 0.98rem 1.18rem;
        border-bottom: 1px solid rgba(148, 175, 206, 0.1);
        gap: 0.85rem;
        align-items: flex-start;
    }

    .detail-item:last-child { border-bottom: none; }
    .detail-icon { display: none; }

    .detail-label {
        width: 118px;
        font-weight: 600;
        color: var(--muted) !important;
        flex-shrink: 0;
    }

    .detail-value {
        flex: 1;
        color: var(--ink) !important;
        line-height: 1.72;
    }

    .tag-row,
    .action-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.55rem;
    }

    .tag,
    .chip {
        display: inline-flex;
        align-items: center;
        gap: 0.34rem;
        padding: 0.4rem 0.76rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.04);
        border: 1px solid var(--line);
        color: var(--ink-soft) !important;
        font-size: 0.78rem;
        font-weight: 650;
    }

    .tag-accent {
        background: var(--gold-soft);
        color: var(--gold) !important;
        border-color: rgba(224, 181, 106, 0.22);
    }

    .tag-primary {
        background: var(--primary-soft);
        color: #A9CAFF !important;
        border-color: rgba(62, 139, 255, 0.24);
    }

    .tag-success {
        background: var(--accent-soft);
        color: var(--accent) !important;
        border-color: rgba(125, 226, 209, 0.2);
    }

    .jump-notice {
        padding: 1rem 1.05rem;
        border-left: 3px solid var(--accent) !important;
        color: var(--ink) !important;
    }

    .chart-frame {
        padding: 1rem 1rem 0.65rem;
        position: relative;
        overflow: hidden;
    }

    .chart-frame::before {
        content: "";
        position: absolute;
        inset: 0 0 auto 0;
        height: 1px;
        background: linear-gradient(90deg, rgba(62, 139, 255, 0.8), rgba(62, 139, 255, 0));
    }

    .chart-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 1rem;
        margin-bottom: 0.65rem;
    }

    .chart-caption { margin-bottom: 0.15rem; }

    .result-card,
    .search-result-card,
    .recommend-card,
    .clickable-card,
    .job-card,
    .interactive-card,
    .recommendation-card {
        position: relative;
        overflow: hidden;
    }

    .result-card::before,
    .search-result-card::before,
    .recommend-card::before,
    .clickable-card::before,
    .job-card::before,
    .interactive-card::before,
    .recommendation-card::before {
        content: "";
        position: absolute;
        inset: 0 auto auto 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, rgba(62, 139, 255, 0.75), rgba(125, 226, 209, 0));
    }

    .result-card-meta,
    .search-result-meta,
    .job-card-meta {
        color: var(--muted) !important;
        font-size: 0.8rem;
        margin-top: 0.35rem;
        line-height: 1.58;
    }

    .recommend-score {
        color: #A9CAFF !important;
        font-size: 0.86rem;
        font-weight: 700;
        white-space: nowrap;
    }

    .empty-state {
        padding: 1rem 1.05rem;
        margin: 0.35rem 0 0.85rem;
    }

    .stProgress > div > div {
        background: linear-gradient(90deg, var(--primary), var(--accent)) !important;
        border-radius: 999px;
    }

    .stProgress > div {
        background: rgba(148, 175, 206, 0.14) !important;
        border-radius: 999px;
    }

    .stAlert {
        border-radius: 16px !important;
        border: 1px solid var(--line) !important;
        border-left: 3px solid var(--primary) !important;
        background: linear-gradient(180deg, rgba(13, 25, 42, 0.96) 0%, rgba(9, 18, 31, 0.96) 100%) !important;
        box-shadow: var(--shadow-soft) !important;
    }

    .stAlert p { color: var(--ink) !important; }

    hr {
        margin: 1.35rem 0;
        border: none;
        height: 1px;
        background: var(--line);
    }

    .stButton button {
        font-weight: 600 !important;
        border-radius: 14px !important;
        border: 1px solid var(--line) !important;
        box-shadow: none !important;
        transition:
            transform 140ms var(--ease-out),
            background 140ms var(--ease-out),
            border-color 140ms var(--ease-out),
            box-shadow 140ms var(--ease-out) !important;
        min-height: 44px !important;
    }

    .stButton button:hover { transform: translateY(-1px); }
    .stButton button:active { transform: translateY(0); }

    .stButton button:focus,
    .stButton button:focus-visible {
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(62, 139, 255, 0.18) !important;
        border-color: rgba(62, 139, 255, 0.34) !important;
    }

    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary) 0%, #4A95FF 100%) !important;
        color: white !important;
        border-color: rgba(100, 166, 255, 0.6) !important;
    }

    .stButton button[kind="primary"]:hover {
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%) !important;
        box-shadow: 0 14px 28px rgba(32, 99, 198, 0.28) !important;
    }

    .stButton button[kind="secondary"] {
        background: rgba(255,255,255,0.02) !important;
        color: var(--ink) !important;
    }

    .stButton button[kind="secondary"]:hover {
        background: rgba(62, 139, 255, 0.1) !important;
        color: var(--ink) !important;
        border-color: rgba(62, 139, 255, 0.3) !important;
    }

    .search-tag-scope {
        display: flex;
        flex-direction: column;
        gap: 0.55rem;
    }

    .search-tag-scope [data-testid="column"] {
        display: flex;
    }

    .search-tag-scope .stButton {
        width: 100%;
    }

    .search-tag-scope .stButton button {
        width: 100% !important;
        justify-content: center !important;
        background: rgba(255,255,255,0.03) !important;
        color: var(--ink-soft) !important;
        border: 1px solid rgba(148, 175, 206, 0.16) !important;
        border-radius: 999px !important;
        padding: 0.4rem 0.8rem !important;
        min-height: 38px !important;
        font-size: 0.83rem !important;
        font-weight: 650 !important;
        white-space: nowrap !important;
        box-shadow: none !important;
    }

    .search-tag-scope .stButton button:hover {
        background: rgba(62, 139, 255, 0.14) !important;
        color: #DDEBFF !important;
        border-color: rgba(62, 139, 255, 0.32) !important;
    }

    .insight-list {
        display: grid;
        gap: 0.78rem;
    }

    .timeline-stage {
        position: relative;
        padding-left: 1.2rem;
        margin-bottom: 0.9rem;
    }

    .timeline-stage::before {
        content: "";
        position: absolute;
        left: 0;
        top: 0.35rem;
        width: 10px;
        height: 10px;
        border-radius: 999px;
        background: var(--accent);
        box-shadow: 0 0 0 4px rgba(125, 226, 209, 0.12);
    }

    .timeline-stage::after {
        content: "";
        position: absolute;
        left: 4px;
        top: 1rem;
        bottom: -1rem;
        width: 1px;
        background: rgba(148, 175, 206, 0.18);
    }

    .timeline-stage:last-child::after { display: none; }

    .timeline-stage-title {
        color: var(--ink) !important;
        font-size: 0.98rem;
        font-weight: 680;
        margin-bottom: 0.2rem;
    }

    .timeline-stage-caption {
        color: var(--muted) !important;
        font-size: 0.88rem;
        line-height: 1.62;
    }

    .stDataFrame, .dataframe {
        color: var(--ink) !important;
        background: transparent !important;
    }

    .stDataFrame td, .dataframe td {
        color: var(--ink) !important;
        background: rgba(10, 20, 34, 0.92) !important;
    }

    .stDataFrame th, .dataframe th {
        color: var(--ink) !important;
        font-weight: 650 !important;
        background: rgba(18, 32, 49, 0.96) !important;
    }

    .streamlit-expanderHeader {
        color: var(--ink) !important;
        font-weight: 600 !important;
        background: linear-gradient(180deg, rgba(13, 25, 42, 0.96) 0%, rgba(9, 18, 31, 0.96) 100%) !important;
        border-radius: 16px !important;
        border: 1px solid var(--line) !important;
    }

    .streamlit-expanderContent {
        color: var(--ink) !important;
        background: transparent !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(255,255,255,0.02);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 8px;
        margin-bottom: 0.4rem;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 10px 16px;
        color: var(--muted) !important;
        background: transparent !important;
        font-weight: 650 !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(62, 139, 255, 0.18) 0%, rgba(62, 139, 255, 0.08) 100%) !important;
        color: var(--ink) !important;
        box-shadow: inset 0 0 0 1px rgba(62, 139, 255, 0.2);
    }

    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .app-hero,
        .hero-grid {
            grid-template-columns: 1fr;
        }

        .detail-item {
            display: block;
        }

        .detail-label {
            width: auto;
            margin-bottom: 0.3rem;
        }

        .card-title-row,
        .chart-header {
            flex-direction: column;
            align-items: flex-start;
        }
    }

    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def render_header():
    """渲染页面头部"""
    st.markdown("""
    <div class="app-hero">
        <div class="main-title">
            <span class="eyebrow">Fintech Intelligence Workspace</span>
            <h1>湖南大学金融科技专业导航系统</h1>
            <div class="sub-title">围绕课程、技能、证书与职业路径的决策界面，帮助你把分散信息整合成清晰的成长判断与行动路线。</div>
            <div class="hero-meta">
                <span class="badge">课程画像</span>
                <span class="badge">技能关系</span>
                <span class="badge">证书规划</span>
                <span class="badge">职业情报</span>
            </div>
        </div>
        <div class="hero-panel">
            <div class="hero-panel-card">
                <div class="hero-panel-label">Workspace focus</div>
                <div class="hero-panel-value">从学习配置到职业出口的统一视图</div>
                <div class="hero-panel-caption">保留现有逻辑与跨页跳转，把核心页面重构为更接近金融分析产品的工作台体验。</div>
            </div>
            <div class="hero-panel-card">
                <div class="hero-panel-label">Modules</div>
                <div class="hero-panel-value">6 个模块协同浏览</div>
                <div class="hero-panel-caption">课程地图、技能图谱、证书导航、职业生态、成长路线、智能搜索。</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def init_session():
    """初始化 session state"""
    if "nav_selected" not in st.session_state:
        st.session_state.nav_selected = "课程地图"
    if "selected_job" not in st.session_state:
        st.session_state.selected_job = None
    if "selected_cert" not in st.session_state:
        st.session_state.selected_cert = None
    if "jump_from_cert" not in st.session_state:
        st.session_state.jump_from_cert = False
    if "jump_from_job" not in st.session_state:
        st.session_state.jump_from_job = False
    if "show_sidebar" not in st.session_state:
        st.session_state.show_sidebar = True
    if "search_input" not in st.session_state:
        st.session_state.search_input = ""
