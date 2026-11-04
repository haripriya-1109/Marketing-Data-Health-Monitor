
import streamlit as st


def render_sidebar(pages):

    with st.sidebar:

        # Brand header
        st.html("""
<div style="display:flex; align-items:center; gap:12px;
            padding:12px 6px 24px 6px;
            border-bottom:1px solid #E6EBF2;
            margin-bottom:22px;">

    <div style="width:42px; height:42px; flex-shrink:0;
                border-radius:11px; background:#EFF6FF;
                color:#2563EB; display:flex;
                align-items:center; justify-content:center;
                font-size:21px; font-weight:800;">
        M
    </div>

    <div>
        <div style="color:#172B4D; font-size:15px;
                    font-weight:750;">
            Marketing Intelligence
        </div>
        <div style="color:#64748B; font-size:11px;
                    margin-top:3px;">
            DATA QUALITY PLATFORM
        </div>
    </div>
</div>

<div style="color:#94A3B8; font-size:10px;
            font-weight:700; letter-spacing:1.2px;
            margin:0 0 12px 6px;">
    WORKSPACE
</div>
""")

        # Navigation links
        for page in pages:
            st.page_link(
                page,
                label=page.title,
                icon=page.icon
            )

        # Database status
        st.html("""
<div style="margin-top:30px; padding:16px 8px;
            border-top:1px solid #E6EBF2;">

    <div style="display:flex; align-items:center;
                gap:8px; color:#475569;
                font-size:12px; font-weight:600;">
        <span style="width:8px; height:8px;
                     border-radius:50%; background:#16A34A;
                     display:inline-block;"></span>
        Database Workspace
    </div>

    <div style="color:#94A3B8; font-size:11px;
                margin:7px 0 0 16px;">
        MarketingDataHealth
    </div>
</div>
""")
