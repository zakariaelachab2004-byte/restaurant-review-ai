import streamlit as st
import pandas as pd
import joblib
import re
import nltk
import torch
import torch.nn.functional as F

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification

# =========================
# Configuration Streamlit
# =========================
st.set_page_config(
    page_title="Restaurant Review AI - NLP",
    layout="wide"
)

# =========================
# Session state
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# Sidebar
# =========================
st.sidebar.title("Restaurant Review AI")
st.sidebar.info(
    """
    Projet NLP
    
    - Analyse de sentiment
    - DistilBERT
    - Détection des thèmes
    - KPIs
    - Recommandations
    - Export CSV
    """
)

# =========================
# Ressources NLP
# =========================
nltk.download("stopwords")
nltk.download("wordnet")

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

# =========================
# Chargement modèles + données
# =========================
@st.cache_resource
def load_classic_model():
    model = joblib.load("models/sentiment_model.pkl")
    vectorizer = joblib.load("models/vectorizer.pkl")
    return model, vectorizer

@st.cache_resource
def load_bert_model():
    tokenizer = DistilBertTokenizerFast.from_pretrained("models/distilbert_model")
    model = DistilBertForSequenceClassification.from_pretrained("models/distilbert_model")
    model.eval()
    return tokenizer, model

@st.cache_data
def load_data():
    return pd.read_csv("data/raw/Restaurant_Reviews.tsv", sep="\t")

model, vectorizer = load_classic_model()
bert_tokenizer, bert_model = load_bert_model()
df = load_data()

# =========================
# Fonctions NLP
# =========================
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z]", " ", text)
    words = text.split()
    words = [
        lemmatizer.lemmatize(word)
        for word in words
        if word not in stop_words
    ]
    return " ".join(words)


def detect_theme(review):
    review = review.lower()
    themes = []

    if any(word in review for word in ["service", "waiter", "staff", "employee", "served"]):
        themes.append("Service")

    if any(word in review for word in ["food", "meal", "dish", "taste", "flavor", "menu", "pizza", "burger"]):
        themes.append("Qualité des plats")

    if any(word in review for word in ["price", "expensive", "cheap", "overpriced", "cost"]):
        themes.append("Prix")

    if any(word in review for word in ["clean", "dirty", "hygiene", "table", "bathroom"]):
        themes.append("Hygiène")

    if any(word in review for word in ["slow", "wait", "waiting", "late", "time"]):
        themes.append("Temps d’attente")

    if any(word in review for word in ["ambience", "atmosphere", "music", "place", "decor"]):
        themes.append("Ambiance")

    if len(themes) == 0:
        themes.append("Autre")

    return themes


def recommendation_agent(review):
    review = review.lower()
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
            "Action recommandée": "Former le personnel à l’accueil, la communication et la relation client.",
            "Priorité": "Élevée"
        })

    if any(word in review for word in ["expensive", "price", "overpriced", "cost"]):
        recommendations.append({
            "Problème": "Prix",
            "Cause probable": "Prix perçu comme élevé par rapport à la qualité",
            "Action recommandée": "Revoir la politique tarifaire ou proposer des offres promotionnelles.",
            "Priorité": "Moyenne"
        })

    if any(word in review for word in ["cold", "taste", "bad food", "food", "meal", "dish"]):
        recommendations.append({
            "Problème": "Qualité des plats",
            "Cause probable": "Goût, température ou qualité insuffisante",
            "Action recommandée": "Contrôler la qualité, le goût et la température des plats avant le service.",
            "Priorité": "Élevée"
        })

    if any(word in review for word in ["dirty", "clean", "hygiene", "table", "bathroom"]):
        recommendations.append({
            "Problème": "Hygiène",
            "Cause probable": "Manque de contrôle de propreté",
            "Action recommandée": "Renforcer les contrôles d’hygiène et de nettoyage.",
            "Priorité": "Élevée"
        })

    if len(recommendations) == 0:
        recommendations.append({
            "Problème": "Non identifié",
            "Cause probable": "Avis trop général",
            "Action recommandée": "Analyser manuellement l’avis pour identifier la cause principale.",
            "Priorité": "Faible"
        })

    return recommendations


def predict_with_confidence(text):
    inputs = bert_tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    with torch.no_grad():
        outputs = bert_model(**inputs)

    probabilities = F.softmax(outputs.logits, dim=1)

    predicted_class = torch.argmax(probabilities, dim=1).item()
    confidence = probabilities[0][predicted_class].item()

    sentiment = "Positif" if predicted_class == 1 else "Négatif"

    return sentiment, confidence

# =========================
# Préparation des données
# =========================
df["clean_review"] = df["Review"].apply(clean_text)
df["themes"] = df["Review"].apply(detect_theme)
themes_df = df.explode("themes")

# =========================
# Interface principale
# =========================
st.title("Restaurant Review AI")
st.write(
    "Système intelligent d’analyse des avis clients pour l’amélioration "
    "des services de restauration."
)

tab1, tab2, tab3, tab4 = st.tabs([
    "Dashboard global",
    "Analyse d’un avis",
    "Comparaison des modèles",
    "Historique / Export"
])

# =========================
# TAB 1 : Dashboard global
# =========================
with tab1:
    st.header("Dashboard global")

    total_reviews = len(df)
    positive_reviews = df[df["Liked"] == 1].shape[0]
    negative_reviews = df[df["Liked"] == 0].shape[0]
    satisfaction_rate = df["Liked"].mean() * 100
    negative_rate = 100 - satisfaction_rate

    # KPIs principaux
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Nombre total d'avis", total_reviews)
    col2.metric("Avis positifs", positive_reviews)
    col3.metric("Avis négatifs", negative_reviews)
    col4.metric("Taux de satisfaction", f"{satisfaction_rate:.2f}%")

    # KPIs avancés
    col5, col6, col7 = st.columns(3)

    col5.metric("Taux d'insatisfaction", f"{negative_rate:.2f}%")
    col6.metric("Ratio positif/négatif", f"{positive_reviews}/{negative_reviews}")
    col7.metric("Nombre de thèmes détectés", themes_df["themes"].nunique())

    st.divider()

    # Répartition sentiments
    st.subheader("Répartition des sentiments")

    sentiment_counts = df["Liked"].map({
        1: "Positif",
        0: "Négatif"
    }).value_counts()

    st.bar_chart(sentiment_counts)

    st.divider()

    # Mots-clés globaux
    st.subheader("Mots-clés les plus fréquents")

    all_words = " ".join(df["clean_review"]).split()
    word_counts = Counter(all_words)
    top_words = word_counts.most_common(15)

    keywords_df = pd.DataFrame(top_words, columns=["Mot", "Fréquence"])

    col_words1, col_words2 = st.columns(2)

    with col_words1:
        st.dataframe(keywords_df)

    with col_words2:
        st.bar_chart(keywords_df.set_index("Mot"))

    st.divider()

    # Mots négatifs fréquents
    st.subheader("Mots négatifs les plus fréquents")

    negative_df = df[df["Liked"] == 0]

    negative_sentiment_words = {
    "bad", "worst", "disappointed", "slow", "wait", "waited",
    "bland", "cold", "rude", "dirty", "terrible", "horrible",
    "awful", "poor", "overpriced", "expensive", "disgusting",
    "nasty", "unfriendly", "dry", "burnt", "tasteless",
    "mediocre", "waste", "disappointing", "sucks", "problem",
    "wrong", "late", "long", "never"
    }

    negative_words = " ".join(negative_df["clean_review"]).split()

    filtered_negative_words = [
    word
    for word in negative_words
    if word in negative_sentiment_words
    ]

    negative_word_counts = Counter(filtered_negative_words)

    top_negative_words = negative_word_counts.most_common(15)

    negative_keywords_df = pd.DataFrame(
    top_negative_words,
    columns=["Mot négatif", "Fréquence"]
    )

    st.dataframe(negative_keywords_df)
    st.bar_chart(negative_keywords_df.set_index("Mot négatif"))
    # Analyse des thèmes
    st.subheader("Analyse des thèmes")

    themes_df_filtered = themes_df[themes_df["themes"] != "Autre"]

    theme_counts = themes_df_filtered["themes"].value_counts()
    theme_satisfaction = themes_df_filtered.groupby("themes")["Liked"].mean() * 100
    theme_satisfaction = theme_satisfaction.sort_values()

    col_theme1, col_theme2 = st.columns(2)

    with col_theme1:
        st.write("Nombre d’avis par thème")
        st.bar_chart(theme_counts)

    with col_theme2:
        st.write("Taux de satisfaction par thème")
        st.bar_chart(theme_satisfaction)

    st.divider()

    # Tableau résumé par thème
    st.subheader("Tableau résumé par thème")

    themes_df_filtered = themes_df[themes_df["themes"] != "Autre"]
    theme_summary = themes_df_filtered.groupby("themes").agg(
        Nombre_avis=("Review", "count"),
        Satisfaction_moyenne=("Liked", "mean")
    ).reset_index()

    theme_summary["Satisfaction_moyenne"] = (
        theme_summary["Satisfaction_moyenne"] * 100
    ).round(2)

    theme_summary = theme_summary.sort_values(
        by="Satisfaction_moyenne",
        ascending=True
    )

    st.dataframe(theme_summary)

    st.divider()

    # Insights automatiques
    st.subheader("Insights automatiques")

    worst_theme = theme_satisfaction.idxmin()
    worst_score = theme_satisfaction.min()

    best_theme = theme_satisfaction.idxmax()
    best_score = theme_satisfaction.max()

    most_discussed_theme = theme_counts.idxmax()
    most_discussed_count = theme_counts.max()

    st.write(
        f"- Le thème le plus problématique est **{worst_theme}** "
        f"avec un taux de satisfaction de **{worst_score:.2f}%**."
    )

    st.write(
        f"- Le thème le plus performant est **{best_theme}** "
        f"avec un taux de satisfaction de **{best_score:.2f}%**."
    )

    st.write(
        f"- Le thème le plus mentionné est **{most_discussed_theme}** "
        f"avec **{most_discussed_count} avis**."
    )

    if worst_score < 50:
        st.warning(
            f"Priorité élevée : améliorer le thème **{worst_theme}**."
        )
    else:
        st.success(
            "La satisfaction globale par thème est relativement correcte."
        )

    st.divider()

    # Recommandations globales
    st.subheader("Recommandations globales")

    if negative_rate > 40:
        st.error(
            "Le taux d’insatisfaction est élevé. Il est recommandé de traiter rapidement les causes principales des avis négatifs."
        )
    elif negative_rate > 25:
        st.warning(
            "Le taux d’insatisfaction est moyen. Des actions d’amélioration ciblées sont recommandées."
        )
    else:
        st.success(
            "Le niveau global de satisfaction est bon. Il faut maintenir les points forts identifiés."
        )

    st.write(
        f"- Priorité 1 : travailler sur **{worst_theme}**."
    )
    st.write(
        f"- Priorité 2 : surveiller les mots négatifs fréquents comme : "
        f"**{', '.join(negative_keywords_df['Mot négatif'].head(5))}**."
    )

# =========================
# TAB 2 : Analyse individuelle
# =========================
with tab2:
    st.header("Analyse d’un nouvel avis avec DistilBERT")

    example_reviews = [
        "",
        "The food was amazing and the service was excellent",
        "The service was slow and the waiter was rude",
        "The food was good but the service was bad",
        "The restaurant was clean and the food was delicious",
        "The price was too expensive for the quality"
    ]

    selected_example = st.selectbox(
        "Choisir un exemple d’avis :",
        example_reviews
    )

    review = st.text_area(
        "Entrez un avis client :",
        value=selected_example,
        height=150
    )

    if st.button("Analyser l’avis"):
        if review.strip() == "":
            st.warning("Veuillez entrer un avis.")
        else:
            sentiment, confidence = predict_with_confidence(review)
            detected_themes = detect_theme(review)

            st.subheader("Résultat de l’analyse")

            if sentiment == "Positif":
                st.success("Sentiment détecté : Positif")
                st.write("Le client semble satisfait.")
            else:
                st.error("Sentiment détecté : Négatif")
                st.write("Le client semble insatisfait.")

            st.metric("Score de confiance", f"{confidence * 100:.2f}%")
            st.progress(float(confidence))

            st.write("Modèle utilisé : **DistilBERT**")

            st.subheader("Thème(s) détecté(s)")
            st.write(", ".join(detected_themes))

            st.subheader("Recommandations proposées")

            if sentiment == "Négatif":
                recommendations = recommendation_agent(review)

                for rec in recommendations:
                    with st.expander(
                        f"Problème : {rec['Problème']} | Priorité : {rec['Priorité']}"
                    ):
                        st.write("Cause probable :", rec["Cause probable"])
                        st.write("Action recommandée :", rec["Action recommandée"])
            else:
                st.success("Maintenir les points forts identifiés dans cet avis.")

            st.session_state.history.append({
                "Avis": review,
                "Sentiment": sentiment,
                "Confiance (%)": round(confidence * 100, 2),
                "Thèmes": ", ".join(detected_themes)
            })

# =========================
# TAB 3 : Comparaison modèles
# =========================
with tab3:
    st.header("Comparaison des modèles")

    model_results = pd.DataFrame({
        "Modèle": [
            "Logistic Regression",
            "Naive Bayes",
            "SVM",
            "DistilBERT"
        ],
        "Accuracy": [
            0.735,
            0.770,
            0.750,
            0.915
        ]
    })

    st.dataframe(model_results)

    st.bar_chart(model_results.set_index("Modèle"))

    best_model = model_results.sort_values(
        by="Accuracy",
        ascending=False
    ).iloc[0]

    st.success(
        f"Le meilleur modèle est **{best_model['Modèle']}** "
        f"avec une accuracy de **{best_model['Accuracy'] * 100:.2f}%**."
    )

    st.info(
        "Les modèles classiques ont été utilisés comme baseline. "
        "DistilBERT a été retenu comme modèle avancé grâce à sa meilleure performance."
    )

# =========================
# TAB 4 : Historique / Export
# =========================
with tab4:
    st.header("Historique des analyses")

    if len(st.session_state.history) == 0:
        st.info("Aucun avis analysé pour le moment.")
    else:
        history_df = pd.DataFrame(st.session_state.history)

        st.dataframe(history_df)

        csv = history_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Télécharger l’historique en CSV",
            data=csv,
            file_name="historique_avis.csv",
            mime="text/csv"
        )