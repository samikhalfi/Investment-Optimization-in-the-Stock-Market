import yfinance as yf
import json

# Charger le fichier JSON avec les noms et symboles des entreprises
with open('companies.json', 'r') as json_file:
    companies = json.load(json_file)

# Demander à l'utilisateur le nom de l'entreprise
company_name = input("Entrez le nom de l'entreprise : ").strip()
company_name_lower = company_name.lower()

# Vérifier si le nom est dans le dictionnaire
# Convertir les noms de société dans le dictionnaire en minuscules pour la vérification
companies_lower = {name.lower(): symbol for name, symbol in companies.items()}

if company_name_lower in companies_lower:
    ticker = companies_lower[company_name_lower]
    print(f"Symbole boursier trouvé : {ticker}")

    # Récupérer les données historiques pour le dernier mois
    stock_data = yf.download(ticker, period='1mo', interval='1d')

    # Afficher les données historiques
    print(f"Données historiques pour {company_name} ({ticker}) :")
    print(stock_data)

    # Sauvegarder les données dans un fichier CSV
    stock_data.to_csv(f'historical_data.csv', index=True)
    print(f"Les données historiques ont été sauvegardées dans le fichier {company_name}_historical_data.csv")
else:
    print("Le nom de l'entreprise n'a pas été trouvé.")
