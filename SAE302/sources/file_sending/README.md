# Module File Sending

## 📋 Description

Module dédié à l'envoi et la réception de fichiers entre client et serveur via TCP. Ce module implémente le protocole de transfert de fichiers utilisé dans le système SAE302.

## 🏗️ Structure

```
file_sending/
├── client/
│   └── client.py      # Client d'envoi de fichiers
└── server/
    ├── serve.py       # Serveur de réception
    └── utils/
        └── [modules utilitaires]
```

## ✨ Fonctionnalités

- Upload de fichiers via TCP
- Transmission du nom et de la taille du fichier
- Validation des extensions autorisées
- Stockage organisé par utilisateur
- Confirmation de réception

## 🚀 Utilisation

### Lancement du Serveur

```bash
cd server
python serve.py -p 5000
```

### Envoi d'un Fichier

```bash
cd client
python client.py <server_ip> <server_port> <file_path>
```

Exemple :
```bash
python client.py 127.0.0.1 5000 /path/to/program.py
```

## 🔌 Protocole de Transfert

```
1. Client → Server: <CLIENT_FILE>
2. Server → Client: <FILE_SERVICE>
3. Server → Client: <FILE_DATA_REQUESTS>
4. Client → Server: filename (ex: "program.py")
5. Client → Server: filesize (ex: "1234")
6. Server → Client: <FILE_DATA_READY> ou <FILE_DATA_NOT_READY>
7. Client → Server: [contenu du fichier]<END>
8. Server → Client: <FILE_RECEIVED>
```

## 📝 Extensions Supportées

Le serveur accepte uniquement :
- `.py` - Python
- `.c` - C
- `.cpp` - C++
- `.cc` - C++
- `.java` - Java

## 🔑 Code Clé

### Client (client.py)
```python
# Lecture et envoi du fichier
with open(file_path, "rb") as f:
    file_data = f.read()

# Envoi des métadonnées
client_socket.send(file_name.encode())
client_socket.send(str(file_size).encode())

# Attendre confirmation
if server_response == "<FILE_DATA_READY>":
    # Envoi du contenu
    client_socket.sendall(file_data)
    client_socket.send(b"<END>")
```

### Serveur (file_services.py)
```python
def file_services(client_socket, client_id):
    # Réception des métadonnées
    file_name = client_socket.recv(1024).decode()
    file_size = client_socket.recv(1024).decode()
    
    # Validation de l'extension
    if check_extension(file_name):
        client_socket.send('<FILE_DATA_READY>'.encode())
        
        # Réception du contenu
        file_bytes = b""
        while not done:
            data = client_socket.recv(1024)
            file_bytes += data
            if file_bytes[-5:] == b'<END>':
                done = True
        
        # Sauvegarde
        file.write(file_bytes[:-5])
        client_socket.send('<FILE_RECEIVED>'.encode())
```

## 📁 Stockage des Fichiers

Les fichiers sont stockés dans :
```
server/client/<username>/
├── program1.py
├── test.c
└── output
```

Chaque utilisateur a son propre dossier isolé.

## 🔒 Validation et Sécurité

### Validations Actuelles
- Vérification de l'extension de fichier
- Création automatique des dossiers utilisateur
- Isolement des fichiers par utilisateur

### Points de Sécurité à Améliorer
- Limite de taille de fichier (pas implémentée)
- Validation du contenu du fichier
- Sanitisation des noms de fichiers
- Quotas utilisateur
- Antivirus/scanning

## 🐛 Gestion des Erreurs

Le module gère :
- Extensions non autorisées
- Erreurs de lecture/écriture
- Déconnexions pendant le transfert
- Fichiers corrompus (détection basique)

## 📊 Flux de Données

```
[Fichier local] → [Client TCP] → [Réseau] → [Serveur TCP] → [Stockage]
     (lecture)       (envoi)                   (réception)     (écriture)
```

## 🎓 Objectif Pédagogique

Ce module démontre :
- Transfert de fichiers binaires via TCP
- Protocole de communication personnalisé
- Gestion de buffer et chunking
- Marqueurs de fin de transmission
- Organisation du stockage serveur

## 💡 Améliorations Possibles

- Support de fichiers volumineux (chunking progressif)
- Checksum/hash pour vérifier l'intégrité
- Compression des fichiers
- Reprise en cas d'interruption
- Transfert multipart pour gros fichiers
- Barre de progression

## 🔗 Intégration

Ce module est intégré dans :
- `authAndFile/` : Avec authentification
- `authFileExec/` : Avec compilation
- Système principal : `/SAE302/server/`

## 👤 Auteur

Marcelin TRAG - RT22 DevCloud FA
