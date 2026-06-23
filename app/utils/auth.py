import streamlit as st


def init_session_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "history" not in st.session_state:
        st.session_state.history = []

    if "uploaded_results" not in st.session_state:
        st.session_state.uploaded_results = None

    if "uploaded_filename" not in st.session_state:
        st.session_state.uploaded_filename = None


def login_page():
    st.markdown(
        """
        <div class="login-title">
            <h1>RestoMind</h1>
            <p>Connectez-vous pour accéder à votre espace d’analyse des avis clients.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col_left, col_center, col_right = st.columns([1.15, 1, 1.15])

    with col_center:
        st.markdown(
            """
            <div class="login-card-header">
                <div class="login-icon">🍽️</div>
                <h2>Connexion Gérant</h2>
                <p>Accès sécurisé au tableau de bord restaurant</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.form("login_form"):
            email = st.text_input("Email", placeholder="admin@gmail.com")
            password = st.text_input("Mot de passe", type="password", placeholder="admin123")

            submitted = st.form_submit_button("Se connecter", use_container_width=True)

            if submitted:
                if email == "admin@gmail.com" and password == "admin123":
                    st.session_state.logged_in = True
                    st.success("Connexion réussie")
                    st.rerun()
                else:
                    st.error("Email ou mot de passe incorrect")


def show_sidebar():
    st.sidebar.markdown("## 🍽️ RestoMind")
    st.sidebar.success("Gérant connecté")

    st.sidebar.markdown("---")

    st.sidebar.markdown(
        """
        ### Fonctionnalités

        - 📤 Import des avis clients  
        - 🤖 Analyse de sentiment  
        - 🏷️ Détection des thèmes  
        - 📊 Dashboard KPI  
        - 💡 Recommandations IA  
        - 📥 Export CSV  
        """
    )

    st.sidebar.markdown("---")

    if st.session_state.uploaded_results is not None:
        st.sidebar.markdown("### Fichier actif")
        st.sidebar.info(st.session_state.uploaded_filename)
        st.sidebar.metric("Avis analysés", len(st.session_state.uploaded_results))
    else:
        st.sidebar.warning("Aucun fichier analysé")

    st.sidebar.markdown("---")

    if st.sidebar.button("Se déconnecter", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()