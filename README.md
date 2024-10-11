# 🚀 NetSpeedX

NetSpeedX est une application avancée de test de performance réseau, qui mesure la latence, le débit descendant, et le débit montant. Elle fonctionne avec un serveur hébergé sous Linux et un client exécuté sur Windows, utilisant des protocoles TCP et UDP pour évaluer efficacement la qualité de connexion.

## ✨ Fonctionnalités
- 📶 **Test de latence** : Mesure le temps de réponse du serveur pour les paquets UDP, offrant une indication précise de la qualité de connexion.
- ⬇️ **Test de débit descendant** : Transfert massif de données du serveur vers le client pour estimer la capacité de téléchargement.
- ⬆️ **Test de débit montant** : Envoi massif de données du client vers le serveur pour évaluer la vitesse de téléversement.

## 🛠️ Technologies Utilisées
- 🐍 **Python** : Langage principal pour les scripts serveur et client, garantissant une implémentation rapide et robuste.
- 📡 **Sockets** : Utilisation des sockets TCP et UDP pour assurer une communication client-serveur efficace et fiable.
- 🔄 **Threading** : Gestion des connexions multiples et des tests simultanés pour une meilleure performance.

## ⚙️ Prérequis
- **Serveur** : Linux avec Python 3 installé.
- **Client** : Windows avec Python 3 installé.
- **Ports** : Port 5000 disponible pour TCP et UDP.

## 🚀 Installation
### Serveur (Linux)
1. **Cloner le dépôt sur le serveur Linux** :
   ```bash
   git clone https://github.com/username/NetSpeedX.git
   cd NetSpeedX
   ```
2. **Exécuter le script du serveur** :
   ```bash
   python3 server.py
   ```

### Client (Windows)
1. **Cloner le dépôt sur votre machine Windows** :
   ```cmd
   git clone https://github.com/username/NetSpeedX.git
   cd NetSpeedX
   ```
2. **Exécuter le script du client** :
   ```cmd
   python client.py
   ```

## 📊 Utilisation
NetSpeedX permet d'exécuter une série de tests de performance :
1. **Latence** : ⚡ Envoi de paquets UDP pour mesurer le temps de réponse et détecter d'éventuelles fluctuations.
2. **Débit descendant** : ⬇️ Le serveur envoie des données aléatoires au client pendant une durée définie pour évaluer la vitesse de téléchargement.
3. **Débit montant** : ⬆️ Le client envoie des données aléatoires au serveur pour mesurer la vitesse de téléversement.

### 🔍 Explications Techniques
- **Serveur** : Le script du serveur écoute sur les ports TCP et UDP, gère les connexions entrantes, et envoie/reçoit des données pour les tests de débit, permettant une évaluation détaillée de la connexion.
- **Client** : Le client se connecte au serveur, envoie des commandes pour démarrer les tests de débit, et calcule la vitesse en fonction du volume de données échangées.
- **Protocole UDP** : Utilisé pour les tests de latence, car il offre une transmission rapide sans contrôle de flux, idéale pour mesurer les temps de réponse.
- **Protocole TCP** : Utilisé pour les tests de débit descendant et montant, garantissant une communication fiable et précise.

## 📈 Visualisation des Résultats
Après avoir effectué les tests, les résultats sont affichés de manière claire :
- **Latence** : ⏱️ Affichée en millisecondes (ms), avec une indication de la meilleure latence observée.
- **Débit Descendant et Montant** : 💾 Affichés en mégabits par seconde (Mbps), permettant de facilement évaluer la capacité du réseau.

## 🤝 Contribution
Nous accueillons chaleureusement toutes les contributions ! 🙌Que ce soit pour corriger des bugs, améliorer les fonctionnalités, ou ajouter de nouvelles idées, n'hésitez pas à créer une issue ou à soumettre une pull request. Merci de contribuer à faire de NetSpeedX un outil encore plus performant.

## 📄 License
Ce projet est sous licence MIT - consultez le fichier [LICENSE](LICENSE) pour plus de détails.

## 👥 Auteurs
- **Nyx-Off** - *Idée originale et développement*

## 💡 Remarques Complémentaires
- 🔒 **Sécurité** : Assurez-vous que les ports nécessaires sont ouverts et sécurisés pour permettre une connexion sans risque.
- 🌐 **Compatibilité Réseau** : Fonctionne sur des réseaux locaux et des connexions distantes, ce qui en fait un outil polyvalent pour tester les performances réseau.
- 📊 **Scalabilité** : NetSpeedX est conçu pour gérer des connexions multiples en parallèle, permettant des tests à grande échelle.

---
🚀 **NetSpeedX** - Mesurez. Analysez. Optimisez. 🌟
