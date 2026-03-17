# styles.py — place this in frontend/utils/styles.py

def get_styles():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    /* ===== GLOBAL ===== */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif !important;
        color: #e2e8f0 !important;
    }

    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }

    /* ===== HIDE DEFAULT TOP SIDEBAR NAV ===== */
    section[data-testid="stSidebarNav"] { display: none !important; }

    /* ===== HIDE STREAMLIT DEFAULTS ===== */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; }

    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1226 0%, #111827 100%) !important;
        border-right: 1px solid rgba(99,179,237,0.15) !important;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] a,
    section[data-testid="stSidebar"] div {
        color: #e2e8f0 !important;
    }

    /* ===== TEXT INPUT ===== */
    .stTextInput > div > div > input {
        background: #1e293b !important;
        border: 1px solid rgba(99,179,237,0.25) !important;
        border-radius: 10px !important;
        color: #f1f5f9 !important;
        font-size: 14px !important;
        caret-color: #63b3ed !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #63b3ed !important;
        box-shadow: 0 0 0 3px rgba(99,179,237,0.1) !important;
        color: #f1f5f9 !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #64748b !important;
        opacity: 1 !important;
    }

    /* ===== NUMBER INPUT ===== */
    .stNumberInput > div > div > input {
        background: #1e293b !important;
        border: 1px solid rgba(99,179,237,0.25) !important;
        border-radius: 10px !important;
        color: #f1f5f9 !important;
        font-size: 14px !important;
        caret-color: #63b3ed !important;
    }
    .stNumberInput > div > div > input:focus {
        border-color: #63b3ed !important;
        color: #f1f5f9 !important;
    }
    .stNumberInput > div > div > input::placeholder {
        color: #64748b !important;
    }

    /* ===== DATE INPUT ===== */
    .stDateInput > div > div > input {
        background: #1e293b !important;
        border: 1px solid rgba(99,179,237,0.25) !important;
        border-radius: 10px !important;
        color: #f1f5f9 !important;
        font-size: 14px !important;
    }
    .stDateInput > div > div > input:focus {
        border-color: #63b3ed !important;
        color: #f1f5f9 !important;
    }

    /* ===== SELECTBOX ===== */
    .stSelectbox > div > div {
        background: #1e293b !important;
        border: 1px solid rgba(99,179,237,0.25) !important;
        border-radius: 10px !important;
        color: #f1f5f9 !important;
    }
    /* The selected value text */
    .stSelectbox > div > div > div {
        color: #f1f5f9 !important;
    }
    .stSelectbox span {
        color: #f1f5f9 !important;
    }
    /* Dropdown arrow */
    .stSelectbox svg {
        fill: #94a3b8 !important;
    }

    /* ===== MULTISELECT ===== */
    .stMultiSelect > div > div {
        background: #1e293b !important;
        border: 1px solid rgba(99,179,237,0.25) !important;
        border-radius: 10px !important;
        color: #f1f5f9 !important;
    }
    .stMultiSelect span {
        color: #f1f5f9 !important;
    }
    /* Selected tags */
    .stMultiSelect [data-baseweb="tag"] {
        background: rgba(99,179,237,0.2) !important;
        border: 1px solid rgba(99,179,237,0.4) !important;
        border-radius: 6px !important;
    }
    .stMultiSelect [data-baseweb="tag"] span {
        color: #93c5fd !important;
    }

    /* ===== DROPDOWN POPUP (selectbox & multiselect options) ===== */
    [data-baseweb="popover"],
    [data-baseweb="popover"] * {
        background: #1e293b !important;
        color: #f1f5f9 !important;
    }
    [data-baseweb="menu"] {
        background: #1e293b !important;
        border: 1px solid rgba(99,179,237,0.2) !important;
    }
    [data-baseweb="option"] {
        background: #1e293b !important;
        color: #f1f5f9 !important;
    }
    [data-baseweb="option"]:hover,
    [data-baseweb="option"][aria-selected="true"] {
        background: rgba(99,179,237,0.15) !important;
        color: #63b3ed !important;
    }

    /* ===== ALL LABELS ===== */
    .stTextInput label,
    .stNumberInput label,
    .stSelectbox label,
    .stMultiSelect label,
    .stDateInput label,
    .stRadio label,
    .stCheckbox label {
        color: #94a3b8 !important;
        font-size: 13px !important;
        font-weight: 500 !important;
    }

    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, #63b3ed, #4fd1c5) !important;
        color: #0a0e1a !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.5rem 1.5rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(99,179,237,0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(99,179,237,0.5) !important;
    }

    /* ===== RADIO ===== */
    .stRadio > div {
        gap: 4px !important;
    }
    .stRadio > div > label {
        color: #94a3b8 !important;
    }

    /* ===== DIVIDER ===== */
    hr { border-color: rgba(99,179,237,0.15) !important; }

    /* ===== ALERTS ===== */
    .stSuccess {
        background: rgba(72,187,120,0.1) !important;
        border: 1px solid rgba(72,187,120,0.3) !important;
        border-radius: 10px !important;
        color: #68d391 !important;
    }
    .stWarning {
        background: rgba(246,173,85,0.1) !important;
        border: 1px solid rgba(246,173,85,0.3) !important;
        border-radius: 10px !important;
        color: #f6ad55 !important;
    }
    .stError {
        background: rgba(252,129,129,0.1) !important;
        border: 1px solid rgba(252,129,129,0.3) !important;
        border-radius: 10px !important;
        color: #fc8181 !important;
    }

    /* ===== DATAFRAME ===== */
    .stDataFrame {
        border: 1px solid rgba(99,179,237,0.15) !important;
        border-radius: 12px !important;
    }

    /* ===== PROGRESS BAR ===== */
    .stProgress > div > div {
        background: linear-gradient(90deg, #63b3ed, #4fd1c5) !important;
        border-radius: 10px !important;
    }

    /* ===== GENERAL TEXT ===== */
    p, h1, h2, h3, h4, h5, h6 {
        color: #e2e8f0 !important;
    }

    </style>
    """


def page_header(title, subtitle=""):
    return f"""
    <div style="
        background: linear-gradient(135deg, rgba(99,179,237,0.12), rgba(79,209,197,0.08));
        border: 1px solid rgba(99,179,237,0.2);
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 28px;
    ">
        <h1 style="
            font-family: 'Syne', sans-serif;
            font-size: 26px;
            font-weight: 800;
            background: linear-gradient(135deg, #63b3ed, #4fd1c5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0 0 4px 0;
            letter-spacing: -0.5px;
        ">{title}</h1>
        <p style="color: #64748b; font-size: 14px; margin: 0;">{subtitle}</p>
    </div>
    """


def metric_card(label, value, icon, color="#63b3ed", bg="rgba(99,179,237,0.08)"):
    return f"""
    <div style="
        background: {bg};
        border: 1px solid {color}33;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
    ">
        <div style="font-size: 28px; margin-bottom: 8px;">{icon}</div>
        <div style="
            font-family: 'Syne', sans-serif;
            font-size: 22px;
            font-weight: 800;
            color: {color};
            margin-bottom: 4px;
        ">{value}</div>
        <div style="
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #64748b;
        ">{label}</div>
    </div>
    """


def status_badge(text, color, bg):
    return f"""
    <div style="
        display: inline-block;
        background: {bg};
        border: 1px solid {color}55;
        border-radius: 20px;
        padding: 8px 20px;
        color: {color};
        font-weight: 600;
        font-size: 14px;
        margin: 8px 0;
    ">{text}</div>
    """


def section_title(title):
    return f"""
    <div style="
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 20px 0 14px 0;
    ">
        <span style="
            font-family: 'Syne', sans-serif;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: #64748b;
        ">{title}</span>
        <div style="flex:1; height:1px; background:rgba(99,179,237,0.15);"></div>
    </div>
    """


def sidebar_html():
    return """
    <div style="text-align:center;padding:10px 0 20px 0;">
        <div style="font-size:40px;">💹</div>
        <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:800;
            background:linear-gradient(135deg,#63b3ed,#4fd1c5);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;">FinSight AI</div>
        <div style="font-size:11px;color:#64748b;margin-top:4px;">AI Budget Advisor</div>
    </div>
    """