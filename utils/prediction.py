import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Chargement des données de sentiment
sentiment_data = pd.read_csv('sentiment_data.csv')

# Chargement des données historiques
historical_data = pd.read_csv('historical_data.csv')

# Affichage des données
print("Données de sentiment :")
print(sentiment_data)
print("\nDonnées historiques :")
print(historical_data)

# Calcul du score de sentiment moyen
average_sentiment_score = sentiment_data['sentiment_score'].mean()
print(f"\nScore de sentiment moyen : {average_sentiment_score:.4f}")

# Sélection de la dernière ligne des données historiques pour prédire le prix de clôture
last_row = historical_data.iloc[-1]

# Préparation des caractéristiques pour le modèle
X = np.array([[average_sentiment_score]])
y = np.array([last_row['Close']])

# Création et entraînement du modèle de régression linéaire
model = LinearRegression()
model.fit(X, y)

# Prédiction du prix pour le lendemain en fonction du score de sentiment
predicted_price = model.predict(X)

# Affichage du prix prédit
print(f"\nPrix prédit du stock pour demain : {predicted_price[0]:.2f}")
