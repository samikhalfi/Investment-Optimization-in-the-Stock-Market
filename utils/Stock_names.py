import requests
from bs4 import BeautifulSoup
import json

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
    companies = {}
    for row in table.find_all('tr')[1:]:  # Ignorer l'en-tête
        cols = row.find_all('td')
        if cols:  # Vérifier si la ligne a des colonnes
            symbol = cols[0].text.strip()  # Le symbole est dans la première colonne
            name = cols[1].text.strip() 
            name = name.lower()   # Le nom de l'entreprise est dans la deuxième colonne
            companies[name] = symbol

    # Sauvegarder les données dans un fichier JSON
    with open('companies.json', 'w') as json_file:
        json.dump(companies, json_file)

    print("Le fichier JSON a été créé avec succès.")
else:
    print(f"Erreur lors de la récupération de la page : {response.status_code}")