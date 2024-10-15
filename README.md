
# Stock Trader Prophet

📈 **IStock Trader Prophet** est une application Streamlit conçue pour analyser les données du marché boursier et visualiser les tendances. Ce tableau de bord permet aux utilisateurs de prendre des décisions d'investissement éclairées en fournissant des données historiques, une analyse des sentiments à partir d'articles d'actualités et des aperçus prédictifs.

## Features

- **Visualisation des données** : Graphiques interactifs pour visualiser les tendances des prix des actions.
- **Analyse des sentiments** : Analysez les titres d'actualités pour évaluer le sentiment du marché.
- **Prédictions** : Prévisions des prix futurs des actions à l'aide de modèles statistiques.
- **Interface conviviale** : Navigation simple pour passer entre les pages de données et de visualisation.

## Installation

Pour exécuter ce projet localement, suivez ces étapes :

1. **Clonez le dépôt** :
   ```bash
   git clone https://github.com/yourusername/investment-dashboard.git
   cd investment-dashboard
   ```

2. **Créez un environnement virtuel (optionnel mais recommandé)** :
   ```bash
   python -m venv venv
   source venv/bin/activate   # Sur Windows utilisez `venv\Scripts\activate`
   ```

3. **Installez les packages requis** :

   Assurez-vous d'avoir Python 3.7+ installé, puis installez les packages requis :
   ```bash
   pip install -r requirements.txt
   ```

4. **Exécutez l'application** :
   ```bash
   streamlit run app.py
   ```

## Usage

1. Après avoir exécuté l'application, naviguez vers l'URL locale fournie par Streamlit (généralement `http://localhost:8501`).
2. Utilisez la barre latérale pour naviguer entre les sections **Données** et **Visualisation**.
3. Dans la section **Données**, vous pouvez consulter et analyser les données historiques des actions.
4. Dans la section **Visualisation**, vous pouvez visualiser des graphiques et faire des prévisions sur les prix des actions.

## Assets

Assurez-vous de placer vos images dans le répertoire `assets`. Les images suivantes sont requises :
- `dashboard_logo.png` : Le logo principal du tableau de bord.
- `logo.png` : L'icône affichée au-dessus du logo principal.

## Contributing

Les contributions sont les bienvenues ! Si vous avez des suggestions d'améliorations ou de fonctionnalités, n'hésitez pas à forker le dépôt et à soumettre une demande de tirage.

## License

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Contact

Pour toute question, veuillez contacter :
- Votre Nom - [your.email@example.com](mailto:your.email@example.com)
