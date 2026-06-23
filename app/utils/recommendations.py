import plotly.express as px
import streamlit as st

from style import metric_card, alert_card, section_title
from utils.dashboard_utils import get_kpis, prepare_themes_dataframe


def recommendation_agent(review):
    review = str(review).lower()
    recommendations = []

    if any(word in review for word in ["slow", "wait", "waiting", "late", "time"]):
        recommendations.append({
            "Problème": "Temps d’attente",
            "Cause probable": "Service lent ou mauvaise organisation",
            "Action recommandée": "Optimiser l’organisation du personnel et réduire le temps d’attente.",
            "Priorité": "Élevée"
        })

    if any(word in review for word in ["rude", "staff", "waiter", "employee", "service"]):
        recommendations.append({
            "Problème": "Qualité du service",
            "Cause probable": "Comportement du personnel ou manque de formation",
            "Action recommandée": "Former le personnel à l’accueil et à la relation client.",
            "Priorité": "Élevée"
        })

    if any(word in review for word in ["expensive", "price", "overpriced", "cost"]):
        recommendations.append({
            "Problème": "Prix",
            "Cause probable": "Prix perçu comme élevé",
            "Action recommandée": "Revoir la politique tarifaire ou proposer des offres.",
            "Priorité": "Moyenne"
        })

    if any(word in review for word in ["cold", "taste", "bad food", "food", "meal", "dish"]):
        recommendations.append({
            "Problème": "Qualité des plats",
            "Cause probable": "Goût, température ou qualité insuffisante",
            "Action recommandée": "Contrôler la qualité et la température des plats.",
            "Priorité": "Élevée"
        })

    if any(word in review for word in ["dirty", "clean", "hygiene", "table", "bathroom"]):
        recommendations.append({
            "Problème": "Hygiène",
            "Cause probable": "Manque de contrôle de propreté",
            "Action recommandée": "Renforcer les contrôles d’hygiène.",
            "Priorité": "Élevée"
        })

    if len(recommendations) == 0:
        recommendations.append({
            "Problème": "Non identifié",
            "Cause probable": "Avis trop général",
            "Action recommandée": "Analyser manuellement l’avis.",
            "Priorité": "Faible"
        })

    return recommendations


def show_global_recommendations(analyzed_df):
    total, positive, negative, satisfaction, dissatisfaction = get_kpis(analyzed_df)
    themes_df = prepare_themes_dataframe(analyzed_df)

    section_title("Analyse globale", "Résumé automatique de la situation du restaurant")

    if negative > positive:
        alert_card(
            "La majorité des avis sont négatifs. Des actions correctives sont prioritaires.",
            "danger"
        )
    else:
        alert_card(
            "La majorité des avis sont positifs. Le restaurant doit maintenir ses points forts.",
            "success"
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card("Satisfaction", f"{satisfaction:.1f}%", "Niveau global", "#10B981")

    with col2:
        metric_card("Insatisfaction", f"{dissatisfaction:.1f}%", "À surveiller", "#EF4444")

    with col3:
        metric_card("Avis négatifs", negative, "Sources d’amélioration", "#F97316")

    st.divider()

    section_title("Recommandations IA", "Actions proposées selon les problèmes les plus fréquents")

    if not themes_df.empty:
        negative_themes = themes_df[themes_df["Sentiment"] == "Négatif"]

        if not negative_themes.empty:
            theme_priority = negative_themes["Thèmes"].value_counts()
            priority_theme = theme_priority.idxmax()

            alert_card(f"Priorité principale détectée : {priority_theme}", "warning")

            recommendations_map = {
                "Temps d’attente": [
                    "Réduire les délais d’attente.",
                    "Optimiser l’organisation du service.",
                    "Prévoir plus de personnel aux heures de pointe."
                ],
                "Service": [
                    "Former le personnel à l’accueil client.",
                    "Améliorer la communication avec les clients.",
                    "Mettre en place un suivi qualité du service."
                ],
                "Qualité des plats": [
                    "Contrôler la qualité et la température des plats.",
                    "Analyser les plats les plus critiqués.",
                    "Renforcer les contrôles en cuisine."
                ],
                "Prix": [
                    "Revoir la perception du rapport qualité/prix.",
                    "Proposer des offres ou menus adaptés.",
                    "Mieux communiquer sur la valeur des plats."
                ],
                "Hygiène": [
                    "Renforcer les contrôles de propreté.",
                    "Vérifier régulièrement les tables, sanitaires et espaces clients."
                ],
                "Ambiance": [
                    "Améliorer l’atmosphère générale.",
                    "Travailler la décoration, le confort et le niveau sonore."
                ]
            }

            actions = recommendations_map.get(
                priority_theme,
                ["Analyser plus précisément les avis négatifs associés à ce thème."]
            )

            for i, action in enumerate(actions, start=1):
                st.markdown(
                    f"""
                    <div class="section-card">
                        <h3>Action {i}</h3>
                        <p>{action}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.divider()

            section_title("Classement des problèmes détectés", "Thèmes négatifs les plus fréquents")

            priority_df = theme_priority.reset_index()
            priority_df.columns = ["Thème", "Nombre d’avis négatifs"]

            fig_priority = px.bar(
                priority_df,
                x="Thème",
                y="Nombre d’avis négatifs",
                text="Nombre d’avis négatifs",
                color="Nombre d’avis négatifs",
                color_continuous_scale=["#FDBA74", "#F97316", "#EF4444"]
            )

            fig_priority.update_layout(
                height=430,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                coloraxis_showscale=False,
                xaxis_title="",
                yaxis_title="Nombre d’avis négatifs"
            )

            st.plotly_chart(fig_priority, use_container_width=True)

        else:
            alert_card("Aucun thème négatif majeur détecté.", "success")
    else:
        alert_card(
            "Pas assez d’informations thématiques pour générer des recommandations précises.",
            "info"
        )