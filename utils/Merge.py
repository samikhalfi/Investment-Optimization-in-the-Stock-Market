import pandas as pd
import os

# Charger les données des scores de sentiment depuis le fichier CSV
file_path = r'C:\Users\anask\Desktop\Investment-Optimization-in-the-Stock-Market-main\Data\Processed_Company_News.csv'
df = pd.read_csv(file_path)

# Calculer la moyenne des scores de sentiment pour chaque date
df_avg_sentiment = df.groupby('date')['sentiment_score'].mean().reset_index()
df_avg_sentiment.columns = ['date', 'avg_sentiment_score']

# Charger les données historiques du fichier CSV
historical_data_file = r'C:\Users\anask\Desktop\Investment-Optimization-in-the-Stock-Market-main\Data\historical_data.csv'
df_historical = pd.read_csv(historical_data_file)

# Convertir les colonnes 'date' pour les rendre comparables (format de date identique)
df_avg_sentiment['date'] = pd.to_datetime(df_avg_sentiment['date'])
df_historical['Date'] = pd.to_datetime(df_historical['Date'])

# Fusionner les deux DataFrames sur la colonne 'date' de df_avg_sentiment et 'Date' de df_historical
df_merged = pd.merge(df_historical, df_avg_sentiment, left_on='Date', right_on='date')

# Supprimer la colonne 'date' car elle est redondante avec 'Date'
df_merged.drop(columns=['date'], inplace=True)

# Définir le chemin pour stocker le fichier final dans le dossier "Data"
output_folder = 'Data'
output_file = 'Final_Data.csv'

# Créer le dossier "Data" s'il n'existe pas déjà
os.makedirs(output_folder, exist_ok=True)

# Chemin complet pour le fichier de sortie
output_path = os.path.join(output_folder, output_file)

# Sauvegarder le DataFrame résultant en CSV
df_merged.to_csv(output_path, index=False)

print(f'Données finales sauvegardées avec succès dans {output_path}')
