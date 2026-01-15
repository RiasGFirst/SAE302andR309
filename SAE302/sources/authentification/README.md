# Module Authentification

## 📋 Description

Module de base implémentant l'authentification des clients sur le serveur. Ce module constitue la première brique du système SAE302.

## 🏗️ Structure

```
authentification/
├── client/
│   └── client.py      # Client console simple
└── server/
    ├── serve.py       # Serveur d'authentification
    └── utils/
        ├── auth.py            # Logique d'authentification
        ├── check_server.py    # Vérification serveurs
        ├── check_compilor.py  # Vérification compilateurs
        └── __init__.py
```

## ✨ Fonctionnalités

- Authentification par username/password
- Validation des identifiants contre `users.txt`
- Gestion de sessions simples
- Envoi de messages de test après authentification

## 🚀 Utilisation

### Lancement du Serveur

```bash
cd server
python serve.py -p 5000 -c 2
```

### Lancement du Client

```bash
cd client
python client.py <server_ip> <server_port>
```

Exemple :
```bash
python client.py 127.0.0.1 5000
```

## 🔌 Flux d'Authentification

```
1. Client se connecte au serveur
2. Client envoie <CLIENT_AUTH>
3. Serveur demande <SEND_CLIENT_ID>
4. Client envoie "client"
5. Client envoie username
6. Client envoie password
7. Serveur vérifie dans users.txt
8. Serveur répond :
   - <CLIENT_AUTH_SUCCESS> si OK
   - <CLIENT_AUTH_FAILED> si erreur
9. Si succès : <SEND_CLIENT_DATA>
10. Client peut envoyer des données
```

## 📝 Format des Utilisateurs

Fichier `files/users.txt` :
```
username1:password1
username2:password2
alice:secret123
bob:test456
```

## 🔑 Code Clé

### Client (client.py)
```python
# Connexion et envoi d'authentification
s.connect((ip, port))
s.send("<CLIENT_AUTH>".encode())

# Envoi des identifiants
s.send("client".encode())
s.send(username.encode())
s.send(password.encode())

# Réception de la réponse
msg = s.recv(1024).decode()
if msg == "<CLIENT_AUTH_SUCCESS>":
    print("Authenticated!")
```

### Serveur (auth.py)
```python
def authentificate(client_socket, client_connected):
    ctype, cid = login(client_socket, client_connected)
    if ctype and cid:
        client_socket.send("<SEND_CLIENT_DATA>".encode())
        return client_type, client_id
    return None, None
```

## 🎓 Objectif Pédagogique

Ce module démontre :
- Communication TCP client-serveur basique
- Protocole personnalisé simple
- Authentification sans chiffrement (à améliorer)
- Gestion multi-clients avec threading

## 🔒 Limitations de Sécurité

⚠️ **Attention** : Ce module est éducatif et présente des limitations :
- Pas de chiffrement des mots de passe
- Pas de SSL/TLS
- Stockage en clair dans users.txt
- Pas de protection contre les attaques par force brute

## 💡 Améliorations Possibles

- Hachage des mots de passe (bcrypt, argon2)
- Chiffrement SSL/TLS
- Tokens de session
- Rate limiting
- Logs d'authentification
- Blocage après échecs multiples

## 🔗 Modules Suivants

Ce module sert de base pour :
- `authAndFile/` : Ajout de la gestion de fichiers
- `authFileExec/` : Système complet avec compilation

## 👤 Auteur

Marcelin TRAG - RT22 DevCloud FA
