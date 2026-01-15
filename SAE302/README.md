# SAE302 - Système de Compilation Client-Serveur Distribué

## 📋 Description

SAE302 est un système de compilation client-serveur distribué permettant aux clients d'envoyer des fichiers de code source à un serveur pour compilation et exécution à distance. Le système supporte plusieurs langages de programmation (Python, C, C++, Java) et gère l'authentification des utilisateurs ainsi que la distribution de charge entre plusieurs serveurs.

## 🏗️ Architecture

Le projet est organisé en plusieurs composants principaux :

```
SAE302/
├── client/          # Application cliente avec interface graphique PyQt6
├── server/          # Serveur de compilation principal
├── docs/            # Documentation PDF et vidéos
└── sources/         # Code source des différentes itérations et modules
```

## ✨ Fonctionnalités

- **Authentification sécurisée** : Système de login/password pour les clients
- **Compilation multi-langage** : Support de Python, C, C++, Java
- **Distribution de charge** : Redirection automatique vers des serveurs secondaires
- **Interface graphique** : Client PyQt6 convivial
- **Gestion de fichiers** : Upload et gestion des fichiers source
- **Exécution à distance** : Compilation et exécution sur le serveur

## 🚀 Installation Rapide

### Prérequis

- Python 3.x
- gcc (pour C)
- g++ (pour C++)
- javac (pour Java)
- PyQt6 (pour le client GUI)

### Installation du Serveur

```bash
cd server
chmod +x install.sh
./install.sh
```

Le script d'installation :
1. Crée un environnement virtuel Python
2. Configure les dossiers nécessaires
3. Initialise les fichiers de configuration (users.txt, servers.json)
4. Vérifie la présence des compilateurs

### Lancement du Serveur

```bash
cd server
python serve.py -p <port> -c <max_clients>
```

Paramètres :
- `-p, --port` : Port d'écoute (défaut: 9999)
- `-c, --max_client` : Nombre maximum de clients (défaut: 1)

### Lancement du Client

```bash
cd client
python client.py
```

## 📚 Documentation Complète

Pour une documentation détaillée, consultez :
- [Documentation Générale](docs/SAE302_General_Doc.pdf)
- [Guide d'Installation](docs/SAE302_Installation_Doc.pdf)
- [Vidéo de Démonstration](docs/SAE302_Video.mkv)

## 📁 Structure Détaillée

- **[client/](client/README.md)** : Application cliente avec interface graphique
- **[server/](server/README.md)** : Serveur principal de compilation
- **[docs/](docs/README.md)** : Documentation PDF et ressources
- **[sources/](sources/README.md)** : Modules et itérations de développement

## 🔧 Protocole de Communication

Le système utilise un protocole TCP personnalisé avec des commandes préfixées par `<>` :

- `<CLIENT_AUTH>` : Demande d'authentification
- `<CLIENT_FILE>` : Envoi de fichier pour compilation
- `<CLIENT_QUIT>` : Déconnexion du client
- `<FILE_SERVICE>` : Service de fichier activé
- `<EXEC_FILE>` : Exécution du fichier compilé

## 👤 Auteur

Marcelin TRAG - RT22 DevCloud FA

## 📄 Licence

Projet académique SAE302 - Tous droits réservés
