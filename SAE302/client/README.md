# Client SAE302

## 📋 Description

Application cliente avec interface graphique PyQt6 permettant de se connecter au serveur de compilation, envoyer des fichiers source et recevoir les résultats de compilation.

## 🎯 Fonctionnalités

- **Interface Graphique Intuitive** : Interface PyQt6 moderne et facile à utiliser
- **Connexion Sécurisée** : Authentification par login/password
- **Upload de Fichiers** : Sélection et envoi de fichiers source
- **Console Intégrée** : Affichage des logs et résultats de compilation
- **Gestion de Session** : Connexion/déconnexion fluide

## 🚀 Utilisation

### Installation des Dépendances

```bash
pip install -r requirements.txt
```

Dépendances requises :
- PyQt6

### Lancement du Client

```bash
python client.py
```

## 🖥️ Interface Utilisateur

L'interface graphique comprend :

1. **Panneau de Connexion**
   - Champ Host (adresse IP du serveur)
   - Champ Port (port du serveur)
   - Champ Username
   - Champ Password
   - Boutons Connexion/Déconnexion

2. **Panneau de Fichiers**
   - Bouton de sélection de fichier
   - Bouton d'envoi
   - Affichage du nom du fichier sélectionné

3. **Console de Sortie**
   - Logs de connexion
   - Messages du serveur
   - Résultats de compilation
   - Messages d'erreur

## 🔌 Protocole Client

Le client communique avec le serveur via TCP en suivant ce workflow :

1. **Connexion** : Établissement de la connexion TCP
2. **Authentification** : Envoi de `<CLIENT_AUTH>` et des identifiants
3. **Envoi de Fichier** : 
   - Envoi de `<CLIENT_FILE>`
   - Transmission du nom et de la taille du fichier
   - Envoi du contenu du fichier
4. **Réception des Résultats** : Affichage de la sortie de compilation
5. **Déconnexion** : Envoi de `<CLIENT_QUIT>`

## 📝 Code Principal

Le fichier `client.py` contient :

- `server_connection()` : Gère la connexion et l'authentification
- `logout_from_server()` : Gère la déconnexion
- `send_file()` : Envoie un fichier au serveur pour compilation
- `log_to_console()` : Affiche les messages dans la console
- Interface PyQt6 avec layouts et widgets

## 🔒 Sécurité

- Les mots de passe sont transmis en clair (amélioration possible avec SSL/TLS)
- Vérification de l'authentification côté serveur
- Gestion des déconnexions intempestives

## 🐛 Gestion des Erreurs

Le client gère :
- Échecs de connexion réseau
- Erreurs d'authentification
- Déconnexions serveur
- Fichiers invalides

## 💡 Améliorations Possibles

- Chiffrement SSL/TLS
- Sauvegarde des préférences de connexion
- Historique des fichiers envoyés
- Éditeur de code intégré
- Support multi-serveurs avec sélection automatique
