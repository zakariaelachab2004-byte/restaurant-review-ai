import sqlite3
from pathlib import Path
from datetime import datetime

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[2]
DB_DIR = ROOT_DIR / "database"
DB_PATH = DB_DIR / "reviews_history.db"


def get_connection():
    DB_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    return conn


def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            analysis_date TEXT NOT NULL,
            total_reviews INTEGER,
            positive_reviews INTEGER,
            negative_reviews INTEGER,
            satisfaction REAL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS review_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            analysis_id INTEGER,
            review_text TEXT,
            sentiment TEXT,
            confidence REAL,
            themes TEXT,
            FOREIGN KEY (analysis_id) REFERENCES analyses(id)
        )
        """
    )

    conn.commit()
    conn.close()


def save_analysis(filename, analyzed_df):
    conn = get_connection()
    cursor = conn.cursor()

    total_reviews = len(analyzed_df)
    positive_reviews = analyzed_df[analyzed_df["Sentiment"] == "Positif"].shape[0]
    negative_reviews = analyzed_df[analyzed_df["Sentiment"] == "Négatif"].shape[0]
    satisfaction = positive_reviews / total_reviews * 100 if total_reviews > 0 else 0

    analysis_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """
        INSERT INTO analyses (
            filename,
            analysis_date,
            total_reviews,
            positive_reviews,
            negative_reviews,
            satisfaction
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            filename,
            analysis_date,
            total_reviews,
            positive_reviews,
            negative_reviews,
            satisfaction
        )
    )

    analysis_id = cursor.lastrowid

    for _, row in analyzed_df.iterrows():
        cursor.execute(
            """
            INSERT INTO review_results (
                analysis_id,
                review_text,
                sentiment,
                confidence,
                themes
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                analysis_id,
                row["Avis"],
                row["Sentiment"],
                row["Confiance (%)"],
                row["Thèmes"]
            )
        )

    conn.commit()
    conn.close()

    return analysis_id


def get_all_analyses():
    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT
            id,
            filename AS "Fichier",
            analysis_date AS "Date d'analyse",
            total_reviews AS "Total avis",
            positive_reviews AS "Avis positifs",
            negative_reviews AS "Avis négatifs",
            ROUND(satisfaction, 2) AS "Satisfaction (%)"
        FROM analyses
        ORDER BY id DESC
        """,
        conn
    )

    conn.close()
    return df


def get_analysis_results(analysis_id):
    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT
            review_text AS "Avis",
            sentiment AS "Sentiment",
            confidence AS "Confiance (%)",
            themes AS "Thèmes"
        FROM review_results
        WHERE analysis_id = ?
        """,
        conn,
        params=(analysis_id,)
    )

    conn.close()
    return df


def delete_analysis(analysis_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM review_results WHERE analysis_id = ?",
        (analysis_id,)
    )

    cursor.execute(
        "DELETE FROM analyses WHERE id = ?",
        (analysis_id,)
    )

    conn.commit()
    conn.close()