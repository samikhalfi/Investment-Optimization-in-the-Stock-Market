import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# Charger les données
data = pd.read_csv(r'C:\Users\anask\Desktop\Investment-Optimization-in-the-Stock-Market-main\Data\Final_Data.csv')
df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Choisir le modèle ARIMA
model = ARIMA(df['Close'], order=(1, 1, 1))  # Ajustez les paramètres si nécessaire
model_fit = model.fit()

# Faire une prévision pour les 3 jours suivants
forecast = model_fit.forecast(steps=3)
predicted_prices = forecast.values

# Dates pour les prévisions
forecast_dates = pd.date_range(start='2024-10-15', periods=3)

# Afficher les prix prévus
for date, price in zip(forecast_dates, predicted_prices):
    print(f'Prix prédit pour le {date.date()}: {price}')

# Visualisation des résultats
plt.figure(figsize=(10, 5))
plt.plot(df['Close'], label='Prix Réel', marker='o')
plt.axvline(x=pd.to_datetime('2024-10-15'), color='r', linestyle='--', label='Date de prévision')
plt.scatter(forecast_dates, predicted_prices, color='green', label='Prix Prévu', marker='x')
plt.title('Prévision du Prix de Stock')
plt.xlabel('Date')
plt.ylabel('Prix')
plt.legend()
plt.show()
