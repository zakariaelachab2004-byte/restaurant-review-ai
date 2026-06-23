import pandas as pd
import streamlit as st

from style import inject_css, hero, feature_card, metric_card, alert_card, section_title

from utils.auth import init_session_state, login_page, show_sidebar
from utils.model_loader import load_bert_model
from utils.file_utils import load_uploaded_reviews, find_review_column
from utils.nlp_utils import analyze_reviews_dataframe, predict_with_confidence, detect_theme
from utils.dashboard_utils import show_dashboard, get_kpis
from utils.recommendations import show_global_recommendations, recommendation_agent
from utils.db_utils import (
    init_database,
    save_analysis,
    get_all_analyses,
    get_analysis_results,
    delete_analysis
)


# =========================
# Configuration Streamlit
# =========================
st.set_page_config(
    page_title="RestoMind - Analyse des avis clients",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================
# Initialisation
# =========================
inject_css()
init_session_state()
init_database()


# =========================
# Authentification
# =========================
if not st.session_state.logged_in:
    login_page()
    st.stop()


# =========================
# Sidebar
# =========================
show_sidebar()


# =========================
# Chargement du modèle IA
# =========================
bert_tokenizer, bert_model = load_bert_model()


# =========================
# Header principal
# =========================
hero(
    "RestoMind",
    "Une application web intelligente permettant au gérant d’importer des avis clients, "
    "d’analyser automatiquement le sentiment, de détecter les thèmes importants et de "
    "générer des recommandations d’amélioration."
)


# =========================
# Onglets
# =========================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 Accueil",
    "📤 Importer des avis",
    "📊 Dashboard",
    "💡 Recommandations IA",
    "🧪 Tester un avis",
    "🗂️ Historique",
])


# =========================
# TAB 1 : Accueil
# =========================
with tab1:
    section_title(
        "Bienvenue dans votre espace d’analyse",
        "Une interface simple pour transformer les avis clients en décisions utiles."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        feature_card(
            "📤",
            "Importer les avis",
            "Ajoutez un fichier CSV ou Excel contenant les commentaires clients du restaurant."
        )

    with col2:
        feature_card(
            "🤖",
            "Analyser automatiquement",
            "Le modèle DistilBERT détecte le sentiment et calcule un score de confiance."
        )

    with col3:
        feature_card(
            "📊",
            "Décider rapidement",
            "Consultez les KPI, les thèmes critiques et les recommandations prioritaires."
        )

    st.divider()

    if st.session_state.uploaded_results is None:
        alert_card(
            "Aucun fichier analysé pour le moment. Commencez par l’onglet Importer des avis.",
            "warning"
        )
    else:
        alert_card(
            f"Un fichier a déjà été analysé : {st.session_state.uploaded_filename}. "
            "Vous pouvez consulter le dashboard.",
            "success"
        )

        analyzed_df = st.session_state.uploaded_results
        total, positive, negative, satisfaction, dissatisfaction = get_kpis(analyzed_df)

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            metric_card("Avis analysés", total, "Fichier actuellement chargé", "#2563EB")

        with col_b:
            metric_card("Avis positifs", positive, "Clients satisfaits", "#10B981")

        with col_c:
            metric_card("Satisfaction", f"{satisfaction:.1f}%", "Performance globale", "#F97316")


# =========================
# TAB 2 : Importer des avis
# =========================
with tab2:
    section_title(
        "Importer un fichier d’avis clients",
        "Le fichier doit contenir une colonne avec les avis : Review, Avis, Commentaire, Feedback, Text..."
    )

    uploaded_file = st.file_uploader(
        "Importer un fichier CSV ou Excel contenant les avis clients",
        type=["csv", "xlsx"]
    )

    if uploaded_file is not None:
        try:
            uploaded_df = load_uploaded_reviews(uploaded_file)

            alert_card("Fichier chargé avec succès.", "success")

            section_title("Aperçu du fichier", "Les premières lignes du fichier importé")
            st.dataframe(uploaded_df.head(), use_container_width=True)

            review_column = find_review_column(uploaded_df)

            if review_column is None:
                alert_card(
                    "Impossible d’identifier automatiquement la colonne contenant les avis.",
                    "warning"
                )

                review_column = st.selectbox(
                    "Choisir la colonne contenant les avis :",
                    uploaded_df.columns
                )

            alert_card(f"Colonne utilisée pour l’analyse : {review_column}", "info")

            reviews_df = pd.DataFrame()
            reviews_df["Review"] = uploaded_df[review_column].astype(str)

            if st.button("Analyser les avis", use_container_width=True):

                analyzed_df = analyze_reviews_dataframe(
                    reviews_df,
                    bert_tokenizer,
                    bert_model
                )

                st.session_state.uploaded_results = analyzed_df
                st.session_state.uploaded_filename = uploaded_file.name

                save_analysis(uploaded_file.name, analyzed_df)

                alert_card(
                    "Analyse terminée et sauvegardée dans l’historique. "
                    "Vous pouvez la consulter dans l’onglet Historique.",
                    "success"
                )

        except Exception as e:
            alert_card(f"Erreur lors du chargement du fichier : {e}", "danger")


# =========================
# TAB 3 : Dashboard
# =========================
with tab3:
    section_title(
        "Dashboard des avis importés",
        "Visualisation globale des sentiments, thèmes et scores de satisfaction."
    )

    if st.session_state.uploaded_results is None:
        alert_card("Veuillez d’abord importer et analyser un fichier d’avis.", "info")
    else:
        analyzed_df = st.session_state.uploaded_results

        show_dashboard(analyzed_df)

        st.divider()

        section_title("Résultats détaillés", "Tableau complet des avis analysés")
        st.dataframe(analyzed_df, use_container_width=True)

        csv = analyzed_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Télécharger les résultats CSV",
            data=csv,
            file_name="resultats_analyse_avis.csv",
            mime="text/csv",
            use_container_width=True
        )


# =========================
# TAB 4 : Recommandations IA
# =========================
with tab4:
    section_title(
        "Recommandations IA",
        "Actions prioritaires générées à partir des avis négatifs et des thèmes détectés."
    )

    if st.session_state.uploaded_results is None:
        alert_card("Veuillez d’abord importer et analyser un fichier d’avis.", "info")
    else:
        analyzed_df = st.session_state.uploaded_results
        show_global_recommendations(analyzed_df)


# =========================
# TAB 5 : Tester un avis
# =========================
with tab5:
    section_title(
        "Tester un avis manuellement",
        "Saisissez un avis client pour obtenir son sentiment, son score de confiance et les recommandations associées."
    )

    example_reviews = [
        "",
        "The food was amazing and the service was excellent",
        "The service was slow and the waiter was rude",
        "The food was good but the service was bad",
        "The restaurant was clean and the food was delicious",
        "The price was too expensive for the quality"
    ]

    selected_example = st.selectbox("Choisir un exemple d’avis :", example_reviews)

    review = st.text_area(
        "Entrez un avis client :",
        value=selected_example,
        height=160
    )

    if st.button("Analyser l’avis", use_container_width=True):
        if review.strip() == "":
            alert_card("Veuillez entrer un avis.", "warning")
        else:
            sentiment, confidence = predict_with_confidence(
                review,
                bert_tokenizer,
                bert_model
            )

            detected_themes = detect_theme(review)

            st.divider()

            section_title("Résultat de l’analyse")

            col1, col2, col3 = st.columns(3)

            with col1:
                color = "#10B981" if sentiment == "Positif" else "#EF4444"
                metric_card("Sentiment", sentiment, "Résultat du modèle DistilBERT", color)

            with col2:
                metric_card("Confiance", f"{confidence * 100:.2f}%", "Probabilité du modèle", "#F97316")

            with col3:
                metric_card("Thèmes", len(detected_themes), ", ".join(detected_themes), "#2563EB")

            st.progress(float(confidence))

            if sentiment == "Positif":
                alert_card(
                    "Le client semble satisfait. Il faut maintenir les points forts identifiés.",
                    "success"
                )
            else:
                alert_card(
                    "Le client semble insatisfait. Une action corrective est recommandée.",
                    "danger"
                )

            st.divider()

            section_title("Thème(s) détecté(s)")
            st.write(", ".join(detected_themes))

            st.divider()

            section_title("Recommandations proposées")

            if sentiment == "Négatif":
                recommendations = recommendation_agent(review)

                for rec in recommendations:
                    with st.expander(
                        f"Problème : {rec['Problème']} | Priorité : {rec['Priorité']}"
                    ):
                        st.write("**Cause probable :**", rec["Cause probable"])
                        st.write("**Action recommandée :**", rec["Action recommandée"])
            else:
                alert_card("Maintenir les points forts identifiés dans cet avis.", "success")

            st.session_state.history.append({
                "Avis": review,
                "Sentiment": sentiment,
                "Confiance (%)": round(confidence * 100, 2),
                "Thèmes": ", ".join(detected_themes)
            })

    if len(st.session_state.history) > 0:
        st.divider()
        section_title("Historique des tests manuels")

        history_df = pd.DataFrame(st.session_state.history)
        st.dataframe(history_df, use_container_width=True)


# =========================
# TAB 6 : Historique
# =========================
with tab6:
    section_title(
        "Historique des analyses",
        "Liste des fichiers déjà traités et sauvegardés dans la base de données."
    )

    analyses_df = get_all_analyses()

    if analyses_df.empty:
        alert_card("Aucune analyse sauvegardée pour le moment.", "info")

    else:
        st.dataframe(analyses_df, use_container_width=True)

        st.divider()

        analysis_ids = analyses_df["id"].tolist()

        def format_analysis_option(analysis_id):
            row = analyses_df[analyses_df["id"] == analysis_id].iloc[0]
            filename = row["Fichier"]

            if "Date d'analyse" in analyses_df.columns:
                date_analyse = row["Date d'analyse"]
            elif "Date d’analyse" in analyses_df.columns:
                date_analyse = row["Date d’analyse"]
            else:
                date_analyse = "Date non disponible"

            return f"{filename} - {date_analyse}"

        selected_analysis_id = st.selectbox(
            "Choisir une analyse à consulter :",
            analysis_ids,
            format_func=format_analysis_option
        )

        selected_results = get_analysis_results(selected_analysis_id)

        selected_row = analyses_df[analyses_df["id"] == selected_analysis_id].iloc[0]
        selected_filename = selected_row["Fichier"]

        section_title(
            "Résultats de l’analyse sélectionnée",
            f"Fichier : {selected_filename}"
        )

        st.dataframe(selected_results, use_container_width=True)

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Charger cette analyse dans le dashboard", use_container_width=True):
                st.session_state.uploaded_results = selected_results
                st.session_state.uploaded_filename = selected_filename

                alert_card(
                    "Analyse chargée avec succès. Vous pouvez maintenant consulter les onglets Dashboard et Recommandations IA.",
                    "success"
                )

        with col2:
            csv_history = selected_results.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="Télécharger cette analyse en CSV",
                data=csv_history,
                file_name=f"analyse_{selected_analysis_id}.csv",
                mime="text/csv",
                use_container_width=True
            )

        st.divider()

        if st.button("Supprimer cette analyse", use_container_width=True):
            delete_analysis(selected_analysis_id)
            alert_card("Analyse supprimée avec succès.", "success")
            st.rerun()