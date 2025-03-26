import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# Charger le fichier CSV
file_path = "smoking.csv"
df = pd.read_csv(file_path)

# Renommer les colonnes
df.columns = [
    "Country", "Year", "Daily_Cigarettes", "Percentage_Male", "Percentage_Female",
    "Percentage_Total", "Smokers_Total", "Smokers_Female", "Smokers_Male"
]

# Convertir les colonnes numériques
numeric_cols = ["Year", "Daily_Cigarettes", "Percentage_Male", "Percentage_Female",
                "Percentage_Total", "Smokers_Total", "Smokers_Female", "Smokers_Male"]
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Filtrer uniquement le Maroc
df_morocco = df[df["Country"] == "Morocco"]


# Algorithme de Collatz (Hailstone)
def collatz_steps(n):
    """Retourne le nombre d'itérations nécessaires pour atteindre 1 avec l'algorithme de Collatz."""
    steps = 0
    while n > 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps

# Appliquer Collatz sur la colonne "Smokers_Total"
df_morocco["Collatz_Steps"] = df_morocco["Smokers_Total"].apply(lambda x: collatz_steps(int(x)))

# Visualiser les résultats avec Matplotlib
plt.figure(figsize=(10, 5))
plt.bar(df_morocco["Year"], df_morocco["Collatz_Steps"], color='skyblue')
plt.xticks(rotation=45)
plt.xlabel("Année")
plt.ylabel("Nombre d'itérations Collatz")
plt.title("Nombre d'itérations avant 1 (Algorithme de Collatz) pour Smokers_Total")
plt.show()

def first_digit(n):
    """Retourne le premier chiffre significatif d'un nombre."""
    while n >= 10:
        n //= 10
    return n

# Extraire le premier chiffre de "Smokers_Total"
first_digits = df_morocco["Smokers_Total"].dropna().apply(lambda x: first_digit(int(x)))
digit_counts = Counter(first_digits)

# Distribution théorique de Benford
benford_distribution = [np.log10(1 + 1/d) for d in range(1, 10)]
benford_labels = list(range(1, 10))

# Comparer la loi de Benford avec les données
plt.figure(figsize=(10, 5))
plt.bar(benford_labels, [digit_counts[d] / sum(digit_counts.values()) for d in benford_labels], color='blue', alpha=0.6, label="Données")
plt.plot(benford_labels, benford_distribution, marker='o', linestyle='-', color='red', label="Benford")
plt.xlabel("Premier chiffre")
plt.ylabel("Fréquence")
plt.title("Comparaison des données avec la loi de Benford")
plt.legend()
plt.grid(True)
plt.show()
