import re

import nltk
import pandas as pd
import streamlit as st
import torch
import torch.nn.functional as F

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


@st.cache_resource
def load_nltk_resources():
    nltk.download("stopwords")
    nltk.download("wordnet")

    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()

    return stop_words, lemmatizer


def clean_text(text):
    stop_words, lemmatizer = load_nltk_resources()

    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z]", " ", text)
    words = text.split()

    words = [
        lemmatizer.lemmatize(word)
        for word in words
        if word not in stop_words
    ]

    return " ".join(words)


def detect_theme(review):
    review = str(review).lower()
    themes = []

    if any(word in review for word in ["service", "waiter", "staff", "employee", "served", "rude"]):
        themes.append("Service")

    if any(word in review for word in ["food", "meal", "dish", "taste", "flavor", "menu", "pizza", "burger", "cold", "delicious"]):
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


def predict_with_confidence(text, bert_tokenizer, bert_model):
    inputs = bert_tokenizer(
        str(text),
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


def analyze_reviews_dataframe(input_df, bert_tokenizer, bert_model):
    results = []

    total_reviews = len(input_df)
    progress_bar = st.progress(0)
    status_text = st.empty()

    for i, review in enumerate(input_df["Review"]):
        if str(review).strip() == "" or str(review).lower() == "nan":
            continue

        sentiment, confidence = predict_with_confidence(
            review,
            bert_tokenizer,
            bert_model
        )

        themes = detect_theme(review)

        results.append({
            "Avis": review,
            "Sentiment": sentiment,
            "Confiance (%)": round(confidence * 100, 2),
            "Thèmes": ", ".join(themes)
        })

        progress = int((i + 1) / total_reviews * 100)
        progress_bar.progress(progress)
        status_text.write(f"Analyse en cours : {i + 1}/{total_reviews} avis traités")

    progress_bar.progress(100)
    status_text.success("Analyse terminée avec succès.")

    return pd.DataFrame(results)