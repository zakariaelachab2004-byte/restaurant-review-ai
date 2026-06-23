import plotly.express as px
import streamlit as st

from style import metric_card, alert_card, section_title


def prepare_themes_dataframe(analyzed_df):
    themes_df = analyzed_df.copy()
    themes_df["Thèmes"] = themes_df["Thèmes"].str.split(", ")
    themes_df = themes_df.explode("Thèmes")
    themes_df = themes_df[themes_df["Thèmes"] != "Autre"]

    return themes_df


def get_kpis(analyzed_df):
    total = len(analyzed_df)
    positive = analyzed_df[analyzed_df["Sentiment"] == "Positif"].shape[0]
    negative = analyzed_df[analyzed_df["Sentiment"] == "Négatif"].shape[0]
    satisfaction = positive / total * 100 if total > 0 else 0
    dissatisfaction = 100 - satisfaction if total > 0 else 0

    return total, positive, negative, satisfaction, dissatisfaction


def show_dashboard(analyzed_df):
    total, positive, negative, satisfaction, dissatisfaction = get_kpis(analyzed_df)

    ratio = f"{positive}/{negative}" if negative > 0 else f"{positive}/0"

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card("Total avis", total, "Nombre total d’avis analysés", "#2563EB")

    with col2:
        metric_card("Avis positifs", positive, "Clients satisfaits", "#10B981")

    with col3:
        metric_card("Avis négatifs", negative, "Avis nécessitant une action", "#EF4444")

    with col4:
        metric_card("Satisfaction", f"{satisfaction:.1f}%", "Score global de satisfaction", "#F97316")

    st.markdown("<br>", unsafe_allow_html=True)

    col5, col6 = st.columns(2)

    with col5:
        metric_card("Insatisfaction", f"{dissatisfaction:.1f}%", "Part des avis négatifs", "#EF4444")

    with col6:
        metric_card("Ratio positif/négatif", ratio, "Comparaison entre avis positifs et négatifs", "#7C3AED")

    st.divider()

    section_title("Répartition des sentiments", "Vue globale des avis positifs et négatifs")

    sentiment_counts = analyzed_df["Sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["Sentiment", "Nombre"]

    fig_sentiment = px.pie(
        sentiment_counts,
        names="Sentiment",
        values="Nombre",
        hole=0.45,
        color="Sentiment",
        color_discrete_map={
            "Positif": "#10B981",
            "Négatif": "#EF4444"
        }
    )

    fig_sentiment.update_layout(
        height=430,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=-0.1)
    )

    st.plotly_chart(fig_sentiment, use_container_width=True)

    st.divider()

    themes_df = prepare_themes_dataframe(analyzed_df)

    if not themes_df.empty:
        col_a, col_b = st.columns(2)

        with col_a:
            section_title("Répartition des thèmes", "Nombre d’avis par sujet détecté")

            theme_counts = themes_df["Thèmes"].value_counts().reset_index()
            theme_counts.columns = ["Thème", "Nombre"]

            fig_theme = px.bar(
                theme_counts,
                x="Thème",
                y="Nombre",
                text="Nombre",
                color="Thème",
                color_discrete_sequence=px.colors.qualitative.Set2
            )

            fig_theme.update_layout(
                height=430,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False,
                xaxis_title="",
                yaxis_title="Nombre d’avis"
            )

            st.plotly_chart(fig_theme, use_container_width=True)

        with col_b:
            section_title("Satisfaction par thème", "Pourcentage d’avis positifs selon le sujet")

            theme_satisfaction = (
                themes_df.groupby("Thèmes")["Sentiment"]
                .apply(lambda x: (x == "Positif").mean() * 100)
                .reset_index()
                .sort_values("Sentiment")
            )

            theme_satisfaction.columns = ["Thème", "Satisfaction (%)"]

            fig_satisfaction = px.bar(
                theme_satisfaction,
                x="Satisfaction (%)",
                y="Thème",
                orientation="h",
                text="Satisfaction (%)",
                color="Satisfaction (%)",
                color_continuous_scale=["#EF4444", "#F97316", "#10B981"]
            )

            fig_satisfaction.update_traces(
                texttemplate="%{text:.1f}%",
                textposition="outside"
            )

            fig_satisfaction.update_layout(
                height=430,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                coloraxis_showscale=False,
                xaxis_title="Satisfaction (%)",
                yaxis_title=""
            )

            st.plotly_chart(fig_satisfaction, use_container_width=True)

        st.divider()

        section_title("Tableau résumé par thème", "Synthèse exploitable pour le gérant")

        theme_summary = themes_df.groupby("Thèmes").agg(
            Nombre_avis=("Avis", "count"),
            Satisfaction_moyenne=("Sentiment", lambda x: round((x == "Positif").mean() * 100, 2))
        ).reset_index()

        theme_summary = theme_summary.rename(columns={
            "Thèmes": "Thème",
            "Nombre_avis": "Nombre d’avis",
            "Satisfaction_moyenne": "Satisfaction moyenne (%)"
        })

        st.dataframe(theme_summary, use_container_width=True)

    else:
        alert_card("Aucun thème métier détecté dans les avis importés.", "info")