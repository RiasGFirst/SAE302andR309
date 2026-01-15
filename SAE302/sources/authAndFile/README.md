# Module AuthAndFile

## 📋 Description

Module intégrant l'authentification et la gestion de fichiers. C'est une étape intermédiaire combinant les fonctionnalités d'authentification des utilisateurs avec l'envoi et la réception de fichiers.

## 🏗️ Structure

```
authAndFile/
└── server/
    ├── serve.py             # Serveur intégré
    ├── files/
    │   ├── users.txt        # Base utilisateurs
    │   └── servers.json     # Configuration serveurs
    └── utils/
        ├── auth.py              # Authentification
        ├── file_services.py     # Gestion fichiers
        ├── check_server.py      # Vérification serveurs
        ├── check_compilor.py    # Vérification compilateurs
        └── __init__.py
```

## ✨ Fonctionnalités

- **Authentification Sécurisée** : Login/password pour accès
- **Upload de Fichiers** : Envoi de fichiers source après authentification
- **Validation** : Vérification des extensions de fichiers
- **Organisation** : Stockage par utilisateur
- **Pas de Compilation** : Ce module ne compile pas encore les fichiers

## 🔄 Évolution du Projet

```
authentification → authAndFile → authFileExec
     (auth)        (auth+files)   (auth+files+exec)
```

Ce module représente l'étape 2 sur 3 de l'intégration complète.

## 🚀 Utilisation

### Lancement du Serveur

```bash
cd server
python serve.py -p 5000 -c 3
```

### Configuration des Utilisateurs

Créer `files/users.txt` :
```
alice:password123
bob:secret456
charlie:test789
```

### Configuration des Serveurs

Créer `files/servers.json` :
```json
{
  "PASSWORD": "master_pass",
  "SERVERS": {
    "backup1": {
      "IP": "192.168.1.100",
      "PORT": 9999,
      "PASSWORD": "backup_pass"
    }
  }
}
```

## 🔌 Flux de Communication

### 1. Authentification

```
Client → Server: <CLIENT_AUTH>
Server → Client: <SEND_CLIENT_ID>
Client → Server: "client"
Client → Server: username
Client → Server: password
Server → Client: <CLIENT_AUTH_SUCCESS>
Server → Client: <SEND_CLIENT_DATA>
```

### 2. Envoi de Fichier

```
Client → Server: <CLIENT_FILE>
Server → Client: <FILE_SERVICE>
Server → Client: <FILE_DATA_REQUESTS>
Client → Server: filename
Client → Server: filesize
Server → Client: <FILE_DATA_READY>
Client → Server: [file_content]<END>
Server → Client: <FILE_RECEIVED>
```

## 🔑 Modules Clés

### auth.py

```python
def authentificate(client_socket, client_connected, max_client=1):
    """
    Authentifie le client et gère la limite de connexions
    """
    ctype, cid = login(client_socket, client_connected)
    
    if ctype is None and cid is None:
        return None, None
    
    # Vérifier la limite de clients
    if len(client_connected) > max_client:
        # Chercher un serveur de backup disponible
        redirect_to_backup_server(client_socket, client_id)
        return None, None
    
    client_socket.send("<SEND_CLIENT_DATA>".encode())
    return ctype, cid

def login(client_socket, client_connected):
    """
    Vérifie les identifiants dans users.txt
    """
    client_socket.send("<SEND_CLIENT_ID>".encode())
    
    client_type = client_socket.recv(1024).decode()
    username = client_socket.recv(1024).decode()
    password = client_socket.recv(1024).decode()
    
    # Vérifier dans users.txt
    if verify_credentials(username, password):
        client_connected.append(username)
        client_socket.send("<CLIENT_AUTH_SUCCESS>".encode())
        return client_type, username
    else:
        client_socket.send("<CLIENT_AUTH_FAILED>".encode())
        return None, None
```

### file_services.py

```python
def file_services(client_socket, client_id):
    """
    Gère la réception d'un fichier du client
    """
    server_dir = os.getcwd()
    
    # Créer le dossier utilisateur
    if not os.path.exists(f"{server_dir}/client/{client_id}"):
        os.makedirs(f"{server_dir}/client/{client_id}")
    
    client_dir = f"{server_dir}/client/{client_id}"
    
    # Confirmer le service de fichier
    client_socket.send('<FILE_SERVICE>'.encode())
    time.sleep(0.1)
    
    # Demander les métadonnées
    client_socket.send('<FILE_DATA_REQUESTS>'.encode())
    file_name = client_socket.recv(1024).decode()
    file_size = client_socket.recv(1024).decode()
    
    print(f"[*] {client_id} envoie {file_name} ({file_size} bytes)")
    
    # Vérifier l'extension
    if check_extension(file_name):
        client_socket.send('<FILE_DATA_READY>'.encode())
        
        # Recevoir le contenu
        file = open(f"{client_dir}/{file_name}", "wb")
        file_bytes = b""
        done = False
        
        while not done:
            data = client_socket.recv(1024)
            file_bytes += data
            if file_bytes[-5:] == b'<END>':
                done = True
        
        file.write(file_bytes[:-5])
        file.close()
        
        client_socket.send('<FILE_RECEIVED>'.encode())
        print(f"[*] Fichier {file_name} reçu avec succès")
    else:
        client_socket.send('<FILE_DATA_NOT_READY>'.encode())
        print(f"[*] Extension non autorisée pour {file_name}")

def check_extension(file_name):
    """
    Vérifie que l'extension est autorisée
    """
    extension_allowed = ["py", "c", "cpp", "cc", "java"]
    file_extension = file_name.split('.')[-1]
    
    return file_extension in extension_allowed
```

### serve.py

```python
def reception_message(client_socket, max_client):
    global client_connected
    client_type = None
    client_id = None
    
    while True:
        try:
            message = client_socket.recv(1024).decode()
        except (ConnectionResetError, ConnectionAbortedError):
            print(f"[*] {client_type} {client_id} déconnecté")
            client_socket.close()
            return
        
        if client_type == "client" and client_id is not None:
            # Client authentifié
            if message == "<CLIENT_QUIT>":
                client_socket.send("<CLIENT_DISCONNECT>".encode())
                client_connected.remove(client_id)
                client_socket.close()
                return
                
            elif message == "<CLIENT_FILE>":
                file_services.file_services(client_socket, client_id)
        else:
            # Pas encore authentifié
            if message == "<CLIENT_AUTH>":
                client_type, client_id = auth.authentificate(
                    client_socket, 
                    client_connected, 
                    max_client
                )
                
                if client_type is None or client_id is None:
                    client_socket.close()
                    return
```

## 📁 Organisation des Fichiers

```
server/
├── files/
│   ├── users.txt                # Configuration
│   └── servers.json             # Configuration
└── client/                      # Fichiers utilisateurs
    ├── alice/
    │   ├── program1.py
    │   └── program2.c
    ├── bob/
    │   └── test.java
    └── charlie/
        └── app.cpp
```

## 🔒 Sécurité

### Points Positifs
- Authentification requise avant upload
- Isolation des fichiers par utilisateur
- Validation des extensions
- Limite de clients simultanés

### Points à Améliorer
- Mots de passe en clair
- Pas de chiffrement des communications
- Pas de limite de taille de fichier
- Pas de sanitisation des noms de fichiers

## 🎓 Objectif Pédagogique

Ce module démontre :
- Intégration de modules indépendants
- Flux de communication séquentiel (auth puis file)
- État de connexion client
- Organisation modulaire du code

## 🚧 Limitations

- **Pas de compilation** : Les fichiers sont stockés mais pas compilés
- **Pas d'exécution** : Pas de retour de résultats
- **Stockage uniquement** : Fonctionnalité intermédiaire

## 💡 Prochaines Étapes

Pour obtenir le système complet :
1. ✅ Authentification (fait)
2. ✅ Gestion de fichiers (fait)
3. ⏭️ Compilation et exécution → Voir `authFileExec/`

## 🔗 Modules Liés

- **Précédent** : `authentification/` - Auth seule
- **Suivant** : `authFileExec/` - Avec compilation
- **Production** : `/SAE302/server/` - Version complète

## 👤 Auteur

Marcelin TRAG - RT22 DevCloud FA
