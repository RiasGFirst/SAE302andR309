# Module File System

## 📋 Description

Module de gestion du système de fichiers côté serveur. Il organise le stockage, la récupération et la gestion des fichiers des utilisateurs de manière structurée et sécurisée.

## 🏗️ Structure

```
file_sys/
├── client/
│   └── client.py      # Client de test
└── server/
    ├── serve.py       # Serveur avec système de fichiers
    └── utils/
        └── [modules de gestion de fichiers]
```

## ✨ Fonctionnalités

- Organisation hiérarchique des fichiers
- Isolation par utilisateur
- Création automatique des dossiers
- Gestion des permissions (basique)
- Stockage persistant

## 📁 Organisation des Fichiers

### Structure du Serveur

```
server/
├── client/                    # Dossier racine des utilisateurs
│   ├── alice/                # Dossier de l'utilisateur alice
│   │   ├── program.py       # Fichier source
│   │   ├── program          # Exécutable compilé
│   │   └── output.txt       # Résultats d'exécution
│   ├── bob/                 # Dossier de l'utilisateur bob
│   │   ├── test.c
│   │   └── test
│   └── charlie/
│       └── app.java
└── files/                    # Configuration serveur
    ├── users.txt
    └── servers.json
```

## 🚀 Utilisation

### Lancement du Serveur

```bash
cd server
python serve.py -p 5000 -c 3
```

### Test du Client

```bash
cd client
python client.py 127.0.0.1 5000
```

## 🔑 Fonctions Principales

### Création de Dossier Utilisateur

```python
def create_user_directory(client_id):
    server_dir = os.getcwd()
    user_dir = os.path.join(server_dir, 'client', client_id)
    
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    
    return user_dir
```

### Stockage de Fichier

```python
def save_user_file(client_id, filename, content):
    user_dir = create_user_directory(client_id)
    file_path = os.path.join(user_dir, filename)
    
    with open(file_path, 'wb') as f:
        f.write(content)
    
    return file_path
```

### Liste des Fichiers Utilisateur

```python
def list_user_files(client_id):
    user_dir = os.path.join(os.getcwd(), 'client', client_id)
    
    if os.path.exists(user_dir):
        return os.listdir(user_dir)
    
    return []
```

## 🔒 Sécurité et Isolation

### Isolation des Utilisateurs

Chaque utilisateur a son propre dossier :
- Empêche l'accès aux fichiers d'autres utilisateurs
- Évite les conflits de noms de fichiers
- Facilite la gestion des quotas

### Validation des Chemins

```python
def validate_path(client_id, filename):
    # Empêcher les path traversal attacks
    if '..' in filename or filename.startswith('/'):
        return False
    
    user_dir = os.path.join('client', client_id)
    file_path = os.path.join(user_dir, filename)
    
    # Vérifier que le chemin reste dans le dossier utilisateur
    return os.path.commonpath([user_dir]) == os.path.commonpath([user_dir, file_path])
```

## 📊 Gestion de l'Espace

### Structure de Données

```python
user_storage = {
    'alice': {
        'files': ['program.py', 'test.c'],
        'size': 15234,  # en bytes
        'last_access': '2024-01-15 10:30:00'
    },
    'bob': {
        'files': ['app.java'],
        'size': 8192,
        'last_access': '2024-01-15 09:45:00'
    }
}
```

## 🧹 Nettoyage et Maintenance

### Suppression des Fichiers Temporaires

```python
def cleanup_user_directory(client_id):
    user_dir = os.path.join('client', client_id)
    
    # Supprimer les exécutables compilés
    for file in os.listdir(user_dir):
        if not file.endswith(('.py', '.c', '.cpp', '.java')):
            os.remove(os.path.join(user_dir, file))
```

### Politique de Rétention

```python
def cleanup_old_files(days=7):
    current_time = time.time()
    
    for user_dir in os.listdir('client'):
        for file in os.listdir(os.path.join('client', user_dir)):
            file_path = os.path.join('client', user_dir, file)
            file_age = current_time - os.path.getmtime(file_path)
            
            if file_age > days * 86400:  # 86400 sec = 1 jour
                os.remove(file_path)
```

## 🎓 Objectif Pédagogique

Ce module enseigne :
- Organisation de système de fichiers
- Gestion des permissions Linux
- Path traversal prevention
- Isolation multi-tenant
- Gestion de l'espace disque

## 🔒 Vulnérabilités Connues

⚠️ **À améliorer** :
- Pas de quotas utilisateur stricts
- Pas de chiffrement des fichiers au repos
- Pas de backup automatique
- Pas de versioning des fichiers

## 💡 Améliorations Possibles

### Quotas Utilisateur

```python
MAX_USER_STORAGE = 100 * 1024 * 1024  # 100 MB

def check_quota(client_id, new_file_size):
    user_dir = os.path.join('client', client_id)
    current_size = sum(
        os.path.getsize(os.path.join(user_dir, f))
        for f in os.listdir(user_dir)
    )
    
    return (current_size + new_file_size) < MAX_USER_STORAGE
```

### Versioning

```python
def save_with_version(client_id, filename, content):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    versioned_name = f"{filename}.{timestamp}"
    # Sauvegarder avec timestamp
```

### Métadonnées

```python
file_metadata = {
    'filename': 'program.py',
    'size': 1234,
    'created': '2024-01-15 10:00:00',
    'modified': '2024-01-15 10:30:00',
    'owner': 'alice',
    'permissions': 'rw-r--r--',
    'hash': 'sha256:abc123...'
}
```

## 🔗 Intégration

Utilisé dans :
- `authAndFile/` : Stockage des fichiers après auth
- `authFileExec/` : Stockage avant compilation
- Système principal : `/SAE302/server/`

## 👤 Auteur

Marcelin TRAG - RT22 DevCloud FA
