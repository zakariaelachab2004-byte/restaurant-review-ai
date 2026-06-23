import sqlite3
from pathlib import Path

DB_PATH = Path("database/reviews_history.db")

print("Chemin DB :", DB_PATH.resolve())

if not DB_PATH.exists():
    print("❌ La base de données n'existe pas encore.")
    print("Lance l'application, importe un fichier et clique sur Analyser les avis.")
else:
    print("✅ La base de données existe.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("\n--- Tables dans la base ---")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        print(table[0])

    print("\n--- Historique des analyses ---")
    cursor.execute("SELECT * FROM analyses;")
    analyses = cursor.fetchall()

    if len(analyses) == 0:
        print("Aucune analyse trouvée.")
    else:
        for row in analyses:
            print(row)

    print("\n--- Résultats des avis, limite 10 ---")
    cursor.execute("SELECT * FROM review_results LIMIT 10;")
    results = cursor.fetchall()

    if len(results) == 0:
        print("Aucun résultat trouvé.")
    else:
        for row in results:
            print(row)

    conn.close()