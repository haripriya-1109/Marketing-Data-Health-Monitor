
import streamlit as st


def apply_custom_styles():

    st.markdown("""
    <style>

    /* =====================================
       GLOBAL DESIGN
    ===================================== */

    :root {
        --primary: #2563EB;
        --primary-dark: #1D4ED8;
        --navy: #172B4D;
        --text: #334155;
        --muted: #64748B;
        --background: #F5F7FB;
        --surface: #FFFFFF;
        --border: #E2E8F0;
        --success: #15803D;
        --warning: #B45309;
        --danger: #B91C1C;
    }

    .stApp {
        background-color: var(--background);
        color: var(--text);
    }

    .main .block-container {
        padding-top: 2.2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }


    /* =====================================
       TYPOGRAPHY
    ===================================== */

    h1, h2, h3, h4 {
        color: var(--navy) !important;
        font-weight: 650 !important;
        letter-spacing: -0.4px;
    }

    h1 {
        font-size: 2rem !important;
    }

    h2 {
        font-size: 1.45rem !important;
    }

    h3 {
        font-size: 1.15rem !important;
    }

    p, label, li {
        color: var(--text);
    }

    [data-testid="stCaptionContainer"] p {
        color: var(--muted) !important;
        font-size: 0.88rem;
    }


    /* =====================================
       SIDEBAR
    ===================================== */


    /* =====================================
   SIDEBAR
===================================== */

    [data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid var(--border);
    }
    

    [data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
    }
   

    [data-testid="stSidebar"] p {
    color: var(--text);
    }
   

    [data-testid="stSidebarNav"] {
    padding-top: 1rem;
    }
   

    [data-testid="stSidebarNav"] a {
    border-radius: 8px;
    margin: 3px 8px;
    transition: background-color 0.2s ease;
    }
   

    [data-testid="stSidebarNav"] a:hover {
    background-color: #EFF6FF;
    color: var(--primary);
    }
    

    [data-testid="stSidebarNav"] a[aria-current="page"] {
    background-color: #EFF6FF;
    color: var(--primary);
    font-weight: 650;
    }
    

    

    /* =====================================
       METRIC CARDS
    ===================================== */

    [data-testid="stMetric"] {
        background-color: var(--surface);
        padding: 18px 20px;
        border-radius: 12px;
        border: 1px solid var(--border);
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
        transition: box-shadow 0.2s ease,
                    transform 0.2s ease;
    }

    [data-testid="stMetric"]:hover {
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.06);
        transform: translateY(-2px);
    }

    [data-testid="stMetricLabel"] p {
        color: var(--muted) !important;
        font-size: 0.84rem;
        font-weight: 500;
    }

    [data-testid="stMetricValue"] {
        color: var(--navy) !important;
        font-weight: 700;
    }


    /* =====================================
       BUTTONS
    ===================================== */

    .stButton > button,
    .stDownloadButton > button {
        border-radius: 8px;
        font-weight: 600;
        border: 1px solid var(--border);
        transition: all 0.2s ease;
    }

    .stButton > button[kind="primary"] {
        background-color: var(--primary);
        color: white;
        border: 1px solid var(--primary);
    }

    .stButton > button[kind="primary"]:hover {
        background-color: var(--primary-dark);
        border-color: var(--primary-dark);
    }

    .stButton > button:focus-visible,
    input:focus-visible,
    textarea:focus-visible {
        outline: 3px solid rgba(37, 99, 235, 0.35);
        outline-offset: 2px;
    }


    /* =====================================
       INPUTS AND FILTERS
    ===================================== */

    [data-baseweb="select"] > div,
    [data-baseweb="input"] > div,
    [data-baseweb="textarea"] {
        border-radius: 8px;
        border-color: var(--border);
        background-color: white;
    }

    [data-baseweb="select"] > div:focus-within,
    [data-baseweb="input"] > div:focus-within {
        border-color: var(--primary);
        box-shadow: 0 0 0 1px var(--primary);
    }

    [data-testid="stSelectbox"],
    [data-testid="stMultiSelect"],
    [data-testid="stTextInput"] {
        margin-bottom: 0.5rem;
    }


    /* =====================================
       DATA TABLES
    ===================================== */

    [data-testid="stDataFrame"] {
        background-color: white;
        border: 1px solid var(--border);
        border-radius: 10px;
        overflow: hidden;
    }

    [data-testid="stDataFrame"] iframe {
        border-radius: 10px;
    }


    /* =====================================
       EXPANDERS
    ===================================== */

    [data-testid="stExpander"] {
        background-color: white;
        border: 1px solid var(--border);
        border-radius: 10px;
        margin-bottom: 10px;
    }

    [data-testid="stExpander"] summary {
        color: var(--navy);
        font-weight: 600;
    }


    /* =====================================
       TABS
    ===================================== */

    [data-baseweb="tab-list"] {
        gap: 1.2rem;
        border-bottom: 1px solid var(--border);
    }

    [data-baseweb="tab"] {
        color: var(--muted);
        font-weight: 500;
    }

    [data-baseweb="tab"][aria-selected="true"] {
        color: var(--primary);
    }


    /* =====================================
       ALERTS AND NOTIFICATIONS
    ===================================== */

    [data-testid="stAlert"] {
        border-radius: 10px;
        border: 1px solid var(--border);
    }


    /* =====================================
       DIVIDERS AND SPACING
    ===================================== */

    hr {
        border-color: var(--border);
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
    }

    [data-testid="stVerticalBlock"] {
        gap: 1rem;
    }


    /* =====================================
       RESPONSIVE LAYOUT
    ===================================== */

    @media (max-width: 768px) {

        .main .block-container {
            padding: 1rem;
        }

        h1 {
            font-size: 1.65rem !important;
        }

        [data-testid="stMetric"] {
            padding: 14px;
        }
    }

    
         
/* =================================
   CUSTOM APPLICATION SIDEBAR
================================= */

[data-testid="stSidebar"] {
background: #FFFFFF;
border-right: 1px solid #E6EBF2;
}

[data-testid="stSidebar"] > div:first-child {
padding: 1.5rem 1rem;
}

/* Brand area */

.brand-container {
padding: 12px 8px 28px 8px;
border-bottom: 1px solid #E9EDF3;
margin-bottom: 24px;
}

.brand-icon {
width: 42px;
height: 42px;
display: flex;
align-items: center;
justify-content: center;
background: #2457C5;
color: white;
border-radius: 11px;
font-size: 21px;
font-weight: 750;
margin-bottom: 15px;
box-shadow: 0 3px 8px rgba(36, 87, 197, 0.18);
}

.brand-name {
color: #172B4D;
font-size: 17px;
font-weight: 750;
letter-spacing: 0.5px;
}

.brand-subtitle {
color: #94A3B8;
font-size: 10px;
font-weight: 600;
letter-spacing: 1.3px;
margin-top: 4px;
}

/* Navigation section label */

.sidebar-section {
color: #94A3B8;
font-size: 10px;
font-weight: 700;
letter-spacing: 1.4px;
padding: 0 10px 12px 10px;
}

/* Navigation links */

[data-testid="stSidebar"] [data-testid="stPageLink"] a {
border-radius: 8px;
padding: 10px 12px;
margin: 3px 0;
color: #475569;
font-size: 13px;
font-weight: 550;
transition: background 0.2s ease;
}

[data-testid="stSidebar"] [data-testid="stPageLink"] a:hover {
background: #F1F5F9;
color: #2457C5;
}

/* Workspace footer */

.sidebar-footer {
border-top: 1px solid #E9EDF3;
margin-top: 30px;
padding: 20px 8px 8px 8px;
color: #475569;
font-size: 12px;
font-weight: 600;
line-height: 1.8;
}

.sidebar-footer span {
color: #94A3B8;
font-size: 11px;
font-weight: 400;
}

.status-dot {
display: inline-block;
width: 8px;
height: 8px;
background: #16A36A;
border-radius: 50%;
margin-right: 8px;
}

    </style>
    """, unsafe_allow_html=True)
