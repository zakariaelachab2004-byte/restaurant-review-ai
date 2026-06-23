from pathlib import Path

import joblib
import streamlit as st
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification


ROOT_DIR = Path(__file__).resolve().parents[2]


@st.cache_resource
def load_classic_model():
    model_path = ROOT_DIR / "models" / "sentiment_model.pkl"
    vectorizer_path = ROOT_DIR / "models" / "vectorizer.pkl"

    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    return model, vectorizer


@st.cache_resource
def load_bert_model():
    bert_path = ROOT_DIR / "models" / "distilbert_model"

    tokenizer = DistilBertTokenizerFast.from_pretrained(bert_path)
    model = DistilBertForSequenceClassification.from_pretrained(bert_path)
    model.eval()

    return tokenizer, model