import streamlit as st


def inject_css():
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

            html, body, [class*="css"] {
                font-family: 'Inter', sans-serif !important;
            }

            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(249, 115, 22, .12), transparent 30%),
                    radial-gradient(circle at top right, rgba(16, 185, 129, .10), transparent 30%),
                    linear-gradient(180deg, #F8FAFC 0%, #EEF2F7 100%);
            }

            .block-container {
                padding-top: 2rem;
                padding-bottom: 3rem;
                max-width: 1280px;
            }

            h1, h2, h3 {
                color: #0F172A !important;
                letter-spacing: -0.035em;
            }

            section[data-testid="stSidebar"] {
                background: linear-gradient(180deg, #0F172A 0%, #111827 55%, #1E293B 100%);
                border-right: none;
            }

            section[data-testid="stSidebar"] * {
                color: #F8FAFC !important;
            }

            .app-hero {
                padding: 38px 42px;
                border-radius: 32px;
                color: white;
                background:
                    linear-gradient(135deg, rgba(15,23,42,.98), rgba(30,41,59,.95)),
                    radial-gradient(circle at 90% 20%, rgba(249,115,22,.55), transparent 34%);
                box-shadow: 0 18px 45px rgba(15, 23, 42, .08);
                border: 1px solid rgba(255,255,255,.10);
                margin-bottom: 26px;
            }

            .app-hero h1 {
                color: #FFFFFF !important;
                font-size: 46px;
                line-height: 1.05;
                margin: 0 0 14px 0;
                font-weight: 800;
            }

            .app-hero p {
                color: #CBD5E1 !important;
                font-size: 17px;
                max-width: 820px;
                margin: 0;
                line-height: 1.7;
            }

            .tagline {
                display: inline-flex;
                padding: 8px 13px;
                border-radius: 999px;
                background: rgba(255,255,255,.10);
                border: 1px solid rgba(255,255,255,.15);
                color: #FED7AA !important;
                font-weight: 800;
                font-size: 13px;
                margin-bottom: 16px;
            }

            .login-title {
                text-align: center;
                margin-top: 45px;
                margin-bottom: 24px;
            }

            .login-title h1 {
                font-size: 44px;
                font-weight: 800;
                margin-bottom: 8px;
            }

            .login-title p {
                color: #64748B;
                font-size: 16px;
            }

            div[data-testid="stForm"] {
                background: rgba(255,255,255,.94);
                border: 1px solid rgba(226,232,240,.95);
                border-radius: 28px;
                box-shadow: 0 18px 45px rgba(15, 23, 42, .08);
                padding: 32px 30px 28px 30px;
            }

            .login-card-header {
                text-align: center;
                margin-bottom: 18px;
            }

            .login-icon {
                width: 72px;
                height: 72px;
                border-radius: 24px;
                margin: 0 auto 14px auto;
                background: linear-gradient(135deg, #F97316, #EA580C);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 34px;
                box-shadow: 0 18px 35px rgba(249,115,22,.28);
            }

            .metric-card {
                background: rgba(255,255,255,.94);
                border: 1px solid rgba(226,232,240,.9);
                border-radius: 24px;
                box-shadow: 0 18px 45px rgba(15, 23, 42, .08);
                padding: 21px 23px;
                min-height: 132px;
                border-left: 6px solid #F97316;
            }

            .metric-label {
                font-size: 12px;
                color: #64748B;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: .07em;
                margin-bottom: 9px;
            }

            .metric-value {
                color: #0F172A;
                font-size: 34px;
                line-height: 1;
                font-weight: 800;
                letter-spacing: -0.04em;
            }

            .metric-help {
                margin-top: 10px;
                font-size: 13px;
                color: #64748B;
            }

            .feature-card {
                background: rgba(255,255,255,.94);
                border: 1px solid rgba(226,232,240,.9);
                border-radius: 24px;
                box-shadow: 0 18px 45px rgba(15, 23, 42, .08);
                padding: 25px;
                min-height: 165px;
            }

            .feature-card .icon {
                width: 50px;
                height: 50px;
                border-radius: 17px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 26px;
                background: #FFF7ED;
                margin-bottom: 15px;
            }

            .feature-card h3 {
                margin: 0 0 8px 0;
                font-size: 18px;
                font-weight: 800;
            }

            .feature-card p {
                color: #64748B;
                margin: 0;
                font-size: 14px;
                line-height: 1.6;
            }

            .section-card {
                background: rgba(255,255,255,.94);
                border: 1px solid rgba(226,232,240,.9);
                border-radius: 24px;
                box-shadow: 0 18px 45px rgba(15, 23, 42, .08);
                padding: 26px;
                margin: 12px 0 18px 0;
            }

            .info-alert,
            .success-alert,
            .soft-alert,
            .danger-alert {
                padding: 18px 20px;
                border-radius: 20px;
                margin: 14px 0;
                font-weight: 600;
            }

            .info-alert {
                background: #EFF6FF;
                border: 1px solid #BFDBFE;
                color: #1E40AF;
            }

            .success-alert {
                background: #ECFDF5;
                border: 1px solid #A7F3D0;
                color: #065F46;
            }

            .soft-alert {
                background: #FFFBEB;
                border: 1px solid #FDE68A;
                color: #92400E;
            }

            .danger-alert {
                background: #FEF2F2;
                border: 1px solid #FECACA;
                color: #991B1B;
            }

            .stButton button,
            .stDownloadButton button,
            .stFormSubmitButton button {
                border-radius: 16px !important;
                min-height: 46px;
                padding: 0 24px !important;
                font-weight: 800 !important;
                background: linear-gradient(135deg, #F97316, #EA580C) !important;
                color: white !important;
                border: none !important;
                box-shadow: 0 12px 24px rgba(249,115,22,.24) !important;
            }

            div[data-testid="stFileUploader"] section {
                border: 2px dashed #FDBA74 !important;
                background: #FFF7ED !important;
                border-radius: 24px !important;
                padding: 20px !important;
            }

            div[data-testid="stTabs"] button {
                border-radius: 999px !important;
                padding: 10px 18px !important;
                font-weight: 800 !important;
            }

            div[data-testid="stTabs"] button[aria-selected="true"] {
                background: #0F172A !important;
                color: #FFFFFF !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )


def hero(title, subtitle):
    st.markdown(
        f"""
        <div class="app-hero">
            <div class="tagline">✨RestoMind — Analyse intelligente des avis clients</div>
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def metric_card(label, value, help_text="", color="#F97316"):
    st.markdown(
        f"""
        <div class="metric-card" style="border-left-color:{color};">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-help">{help_text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def feature_card(icon, title, text):
    st.markdown(
        f"""
        <div class="feature-card">
            <div class="icon">{icon}</div>
            <h3>{title}</h3>
            <p>{text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def alert_card(text, kind="info"):
    css_class = {
        "info": "info-alert",
        "success": "success-alert",
        "warning": "soft-alert",
        "danger": "danger-alert",
    }.get(kind, "info-alert")

    st.markdown(
        f"<div class='{css_class}'>{text}</div>",
        unsafe_allow_html=True
    )


def section_title(title, subtitle=None):
    st.markdown(f"### {title}")
    if subtitle:
        st.caption(subtitle)