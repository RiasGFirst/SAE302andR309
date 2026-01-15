# Serveur SAE302

## 📋 Description

Serveur de compilation multi-langage qui accepte les connexions clients, authentifie les utilisateurs, reçoit des fichiers source et compile/exécute le code dans un environnement sécurisé.

## 🏗️ Architecture

```
server/
├── serve.py              # Point d'entrée du serveur
├── install.sh            # Script d'installation
├── requirements.txt      # Dépendances Python
└── utils/               # Modules utilitaires
    ├── auth.py          # Gestion de l'authentification
    ├── file_services.py # Gestion des fichiers
    ├── compile_services.py # Compilation et exécution
    ├── check_compilor.py   # Vérification des compilateurs
    └── check_server.py     # Vérification des serveurs secondaires
```

## ✨ Fonctionnalités

- **Authentification Multi-Utilisateurs** : Gestion des logins/passwords dans `files/users.txt`
- **Compilation Multi-Langage** : Python, C, C++, Java
- **Distribution de Charge** : Redirection vers serveurs secondaires si surcharge
- **Multi-Threading** : Gestion simultanée de plusieurs clients
- **Gestion de Fichiers** : Stockage organisé par utilisateur dans `client/<username>/`

## 🚀 Installation

### Script d'Installation Automatique

```bash
chmod +x install.sh
./install.sh
```

Le script effectue :
1. Création d'un environnement virtuel Python
2. Création du dossier `client/` (stockage des fichiers utilisateurs)
3. Création du dossier `files/` (configuration)
4. Configuration des utilisateurs dans `files/users.txt`
5. Configuration des serveurs secondaires dans `files/servers.json`

### Configuration Manuelle

#### Fichier users.txt
Format : `username:password` (un par ligne)
```
alice:password123
bob:secret456
```

#### Fichier servers.json
```json
{
  "PASSWORD": "master_password",
  "SERVERS": {
    "server1": {
      "IP": "192.168.1.100",
      "PORT": 9999,
      "PASSWORD": "server1_pass"
    }
  }
}
```

## 🎮 Utilisation

### Lancement du Serveur

```bash
python serve.py -p <port> -c <max_clients>
```

**Arguments :**
- `-p, --port` : Port d'écoute (défaut: 9999)
- `-c, --max_client` : Nombre maximum de clients simultanés (défaut: 1)

**Exemple :**
```bash
python serve.py -p 8080 -c 5
```

### Vérification des Compilateurs

Au démarrage, le serveur vérifie automatiquement la présence de :
- `gcc` (compilateur C)
- `g++` (compilateur C++)
- `javac` (compilateur Java)
- `python` (interpréteur Python)

## 🔧 Modules Utilitaires

### auth.py
Gère l'authentification des clients et des serveurs.

**Fonctions principales :**
- `authentificate()` : Authentification et gestion de la limite de clients
- `login()` : Vérification des identifiants
- Redirection vers serveurs secondaires si surcharge

### file_services.py
Gère la réception et le stockage des fichiers.

**Fonctions principales :**
- `file_services()` : Orchestration du service de fichiers
- `check_extension()` : Validation des extensions de fichiers autorisées

**Extensions supportées :** `.py`, `.c`, `.cpp`, `.cc`, `.java`

### compile_services.py
Gère la compilation et l'exécution du code.

**Fonctions principales :**
- `compile()` : Détection du langage et appel du compilateur approprié
- `compile_python()` : Exécution de code Python
- `compile_c()` : Compilation et exécution de code C
- `compile_cpp()` : Compilation et exécution de code C++
- `compile_java()` : Compilation et exécution de code Java

### check_compilor.py
Vérifie la disponibilité des compilateurs.

**Fonction :**
- `verify_compile()` : Teste chaque compilateur et affiche les résultats

### check_server.py
Vérifie la disponibilité des serveurs secondaires.

**Fonction :**
- `check_server()` : Teste la connexion à un serveur distant

## 🔌 Protocole de Communication

### Flux d'Authentification
```
Client -> Server: <CLIENT_AUTH>
Server -> Client: <SEND_CLIENT_ID>
Client -> Server: "client"
Client -> Server: username
Client -> Server: password
Server -> Client: <CLIENT_AUTH_SUCCESS> ou <CLIENT_AUTH_FAILED>
Server -> Client: <SEND_CLIENT_DATA> ou <CLIENT_EXCEEDED>
```

### Flux de Compilation
```
Client -> Server: <CLIENT_FILE>
Server -> Client: <FILE_SERVICE>
Server -> Client: <FILE_DATA_REQUESTS>
Client -> Server: filename
Client -> Server: filesize
Server -> Client: <FILE_DATA_READY> ou <FILE_DATA_NOT_READY>
Client -> Server: [file_content]<END>
Server -> Client: <FILE_RECEIVED>
Server -> Client: <EXEC_FILE>
Client -> Server: <EXEC_FILE_READY>
Server -> Client: <PYTHON|C|CPP|JAVA>
Server -> Client: [compilation_output]
```

## 📁 Structure des Dossiers

```
server/
├── files/
│   ├── users.txt        # Base de données des utilisateurs
│   └── servers.json     # Configuration des serveurs secondaires
└── client/
    ├── alice/           # Fichiers de l'utilisateur alice
    │   ├── program.py
    │   └── output
    └── bob/             # Fichiers de l'utilisateur bob
        └── test.c
```

## 🔒 Sécurité

### Points de Sécurité Actuels
- Validation des extensions de fichiers
- Limite de clients simultanés
- Isolation des fichiers par utilisateur

### Points d'Amélioration
- Chiffrement des mots de passe (actuellement en clair)
- SSL/TLS pour les communications
- Sandbox d'exécution pour les programmes compilés
- Rate limiting pour prévenir les abus
- Validation et sanitisation du code source

## 🐛 Gestion des Erreurs

Le serveur gère :
- Déconnexions inattendues des clients
- Erreurs de compilation
- Ports déjà utilisés
- Fichiers corrompus ou invalides
- Serveurs secondaires indisponibles

## 📊 Logging

Le serveur affiche des logs colorés :
- 🟢 Vert : Connexions et succès
- 🔴 Rouge : Déconnexions et erreurs
- Messages détaillés pour chaque opération

## 💡 Améliorations Possibles

- Ajout de quotas utilisateurs (CPU, mémoire, disque)
- Support de langages supplémentaires (Go, Rust, etc.)
- API REST en complément du protocole TCP
- Dashboard web pour monitoring
- Logs persistants dans des fichiers
- Support Docker pour l'isolation des exécutions
