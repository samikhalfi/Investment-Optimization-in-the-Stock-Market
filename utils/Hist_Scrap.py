import requests
from bs4 import BeautifulSoup
import yfinance as yf
import pandas as pd

# URL de la page Wikipedia
url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

# Faire une requête HTTP à la page
response = requests.get(url)

# Vérifier si la requête a réussi
if response.status_code == 200:
    # Analyser le contenu de la page
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Trouver le tableau contenant les données
    table = soup.find('table', {'class': 'wikitable'})
    
    # Extraire les symboles de la colonne 'Symbol' et les noms des entreprises
    ticker_symbols = []
    company_names = []
    for row in table.find_all('tr')[1:]:  # Ignorer l'en-tête
        cols = row.find_all('td')
        if cols:  # Vérifier si la ligne a des colonnes
            symbol = cols[0].text.strip()  # Le symbole est dans la première colonne
            name = cols[1].text.strip()    # Le nom de l'entreprise est dans la deuxième colonne
            ticker_symbols.append(symbol)
            company_names.append(name)

else:
    print(f"Erreur lors de la récupération de la page : {response.status_code}")

# Récupérer les données historiques pour chaque entreprise
def get_stock_data(ticker, period):
    stock_data = yf.download(ticker, period=period, interval='1d')
    return stock_data

# Initialiser un DataFrame vide pour stocker toutes les données
all_data = pd.DataFrame()

# Récupérer et stocker les données dans un seul DataFrame
for i, ticker in enumerate(ticker_symbols):
    stock_data = get_stock_data(ticker, period='1mo')  # '1mo' pour 1 mois
    stock_data['Company'] = company_names[i]  # Ajouter une colonne pour le nom de l'entreprise
    stock_data['Ticker'] = ticker  # Ajouter une colonne pour le symbole boursier
    all_data = pd.concat([all_data, stock_data])

# Sauvegarder toutes les données dans un fichier CSV unique
all_data.to_csv('all_companies_historical_data.csv', index=True)