# Restaurant Review AI

## Présentation

Restaurant Review AI est une application intelligente d'analyse des avis clients dans le secteur de la restauration.

L'objectif du projet est d'exploiter les techniques de Natural Language Processing (NLP), Machine Learning et Deep Learning afin d'analyser automatiquement les avis clients, mesurer leur satisfaction et fournir des recommandations d'amélioration aux gestionnaires de restaurants.

---

## Objectifs

* Analyser automatiquement les avis clients.
* Identifier le sentiment global d'un avis (positif ou négatif).
* Détecter les thèmes abordés dans les commentaires.
* Générer des indicateurs de performance (KPIs).
* Produire des recommandations automatiques basées sur les problèmes détectés.
* Comparer plusieurs modèles de Machine Learning et Deep Learning.

---

## Dataset

Dataset utilisé :

**Restaurant Reviews Dataset**

Caractéristiques :

* 1000 avis clients
* Classification binaire :

  * 1 : avis positif
  * 0 : avis négatif

---

## Prétraitement des données

Les étapes de préparation des données comprennent :

* Conversion du texte en minuscules
* Suppression des caractères spéciaux
* Tokenisation
* Suppression des stopwords
* Lemmatisation
* Vectorisation TF-IDF

---

## Modèles implémentés

### Machine Learning

* Logistic Regression
* Naive Bayes
* Support Vector Machine (SVM)

### Deep Learning

* DistilBERT

---

## Évaluation des modèles

Les modèles ont été comparés à l'aide de plusieurs métriques :

* Accuracy
* Precision
* Recall
* F1-Score
* Matrice de confusion

Le modèle DistilBERT a obtenu les meilleures performances et a été retenu pour l'application finale.

---

## Fonctionnalités de l'application Streamlit

### Dashboard global

* Nombre total d'avis
* Avis positifs
* Avis négatifs
* Taux de satisfaction
* Taux d'insatisfaction
* Analyse des thèmes
* Mots-clés fréquents
* Mots négatifs les plus fréquents
* Insights automatiques
* Recommandations globales

### Analyse intelligente d'un avis

* Analyse de sentiment avec DistilBERT
* Score de confiance
* Détection automatique des thèmes
* Analyse des aspects mentionnés
* Recommandations automatiques

### Comparaison des modèles

* Tableau comparatif des performances
* Visualisation graphique des résultats

### Historique

* Historique des analyses réalisées
* Export des résultats au format CSV

---

## Architecture du projet

```text
restaurant-review-ai/
│
├── app/
│   └── streamlit_app.py
│
├── data/
│   ├── raw/
│   │   └── Restaurant_Reviews.tsv
│   └── processed/
│
├── models/
│   ├── sentiment_model.pkl
│   ├── vectorizer.pkl
│   └── distilbert_model/
│
├── notebooks/
│   └── 01_exploration.ipynb
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Technologies utilisées

* Python
* Pandas
* Scikit-Learn
* NLTK
* Transformers
* PyTorch
* Streamlit
* Matplotlib

---

## Lancement du projet

Installation des dépendances :

```bash
pip install -r requirements.txt
```

Lancement de l'application :

```bash
streamlit run app/streamlit_app.py
```

---

## Résultats

Le projet permet :

* d'automatiser l'analyse des avis clients ;
* d'identifier rapidement les principales sources d'insatisfaction ;
* d'aider les responsables de restaurants à prendre des décisions d'amélioration basées sur les données ;
* de démontrer l'apport des modèles NLP modernes comme DistilBERT dans l'analyse de texte.

---

## Auteur

EL ACHAB Zakaria
BENATIK Adnane

Projet réalisé dans le cadre d'un projet de Deep Learning et NLP.
