import pandas as pd


def load_uploaded_reviews(uploaded_file):
    """
    Charge un fichier CSV ou Excel contenant des avis clients.
    Gère plusieurs cas :
    - CSV classique
    - CSV avec séparateur automatique
    - fichier texte simple avec un avis par ligne
    - Excel xlsx
    """

    if uploaded_file.name.endswith(".csv"):
        try:
            uploaded_file.seek(0)
            uploaded_df = pd.read_csv(uploaded_file)

        except Exception:
            uploaded_file.seek(0)

            try:
                uploaded_df = pd.read_csv(
                    uploaded_file,
                    sep=None,
                    engine="python"
                )

            except Exception:
                uploaded_file.seek(0)
                content = uploaded_file.read().decode("utf-8", errors="ignore")

                lines = [
                    line.strip()
                    for line in content.splitlines()
                    if line.strip()
                ]

                uploaded_df = pd.DataFrame({"Review": lines})

    elif uploaded_file.name.endswith(".xlsx"):
        uploaded_file.seek(0)
        uploaded_df = pd.read_excel(uploaded_file)

    else:
        raise ValueError("Format de fichier non supporté. Veuillez importer un fichier CSV ou Excel.")

    return uploaded_df


def find_review_column(uploaded_df):
    """
    Détecte automatiquement la colonne qui contient les avis clients.
    """

    possible_columns = [
        "Review",
        "Avis",
        "Comment",
        "Commentaire",
        "Feedback",
        "Text",
        "ReviewText",
        "CustomerReview",
        "comment",
        "review",
        "avis",
        "text",
        "Commentaires",
        "comments",
        "reviews"
    ]

    for col in uploaded_df.columns:
        if str(col).strip() in possible_columns:
            return col

    if len(uploaded_df.columns) == 1:
        return uploaded_df.columns[0]

    return None