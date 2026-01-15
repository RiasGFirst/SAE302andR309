# Module AuthFileExec

## 📋 Description

Module complet intégrant l'authentification, la gestion de fichiers, et la compilation/exécution. C'est la version finale et aboutie du système SAE302 avant déploiement en production.

## 🏗️ Structure

```
authFileExec/
└── server/
    ├── serve.py                  # Serveur complet
    ├── files/
    │   ├── users.txt            # Base utilisateurs
    │   └── servers.json         # Configuration serveurs
    └── utils/
        ├── auth.py                  # Authentification
        ├── file_services.py         # Gestion fichiers
        ├── compile_services.py      # Compilation/exécution
        ├── check_server.py          # Vérification serveurs
        ├── check_compilor.py        # Vérification compilateurs
        └── __init__.py
```

## ✨ Fonctionnalités Complètes

### 1. Authentification
- ✅ Login/password sécurisé
- ✅ Gestion des sessions
- ✅ Limitation du nombre de clients

### 2. Gestion de Fichiers
- ✅ Upload de fichiers source
- ✅ Validation des extensions
- ✅ Stockage organisé par utilisateur

### 3. Compilation et Exécution
- ✅ Support Python, C, C++, Java
- ✅ Détection automatique du langage
- ✅ Compilation et exécution
- ✅ Retour des résultats ou erreurs

### 4. Distribution de Charge
- ✅ Redirection vers serveurs secondaires
- ✅ Gestion de la surcharge
- ✅ Vérification de disponibilité

## 🔄 Flux Complet

```
┌─────────────────────────────────────────────────────────┐
│                    FLUX AUTHFILEEXEC                    │
└─────────────────────────────────────────────────────────┘

1. CONNEXION
   Client → Server: Connexion TCP

2. AUTHENTIFICATION
   Client ↔ Server: Échange credentials
   Server: Vérifie users.txt
   
3. VÉRIFICATION DISPONIBILITÉ
   Si serveur plein:
      Server: Cherche serveur backup
      Server → Client: Redirection
   Sinon:
      Server → Client: <SEND_CLIENT_DATA>

4. ENVOI FICHIER
   Client → Server: <CLIENT_FILE>
   Client → Server: Métadonnées + Contenu
   Server: Stocke dans client/<username>/

5. COMPILATION
   Server: Détecte langage (extension)
   Server: Compile avec gcc/g++/javac/python
   
6. EXÉCUTION
   Server: Exécute le programme compilé
   Server: Capture stdout/stderr

7. RETOUR RÉSULTAT
   Server → Client: Sortie du programme
   
8. DÉCONNEXION
   Client → Server: <CLIENT_QUIT>
   Server: Nettoie la session
```

## 🚀 Utilisation

### Installation

```bash
cd server
# Configuration automatique
python serve.py install
```

Le mode `install` :
- Vérifie gcc, g++, javac, python
- Affiche les compilateurs disponibles
- Prépare l'environnement

### Lancement

```bash
python serve.py -p 5000 -c 3
```

**Arguments** :
- `-p, --port` : Port d'écoute (défaut: 9999)
- `-c, --max_client` : Clients max simultanés (défaut: 1)

## 🔑 Architecture du Code

### serve.py - Point d'Entrée

```python
def reception_message(client_socket, max_client):
    global client_connected
    client_type = None
    client_id = None
    
    while True:
        try:
            message = client_socket.recv(1024).decode()
        except (ConnectionResetError, ConnectionAbortedError):
            cleanup_client(client_type, client_id)
            return
        
        if client_type == "client" and client_id is not None:
            # Client authentifié - traiter les commandes
            
            if message == "<CLIENT_QUIT>":
                handle_disconnect(client_socket, client_id)
                return
                
            elif message == "<CLIENT_FILE>":
                # Pipeline complet: receive → compile → execute → return
                file_services.file_services(client_socket, client_id)
                
        else:
            # Non authentifié - demander l'auth
            if message == "<CLIENT_AUTH>":
                client_type, client_id = auth.authentificate(
                    client_socket, 
                    client_connected, 
                    max_client
                )

def serve(port, max_client):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(max_client + 1)
    
    print(f"[*] Serveur accepte {max_client} clients")
    print(f"[*] Écoute sur port {port}")
    
    while True:
        client, addr = server.accept()
        print(f"[*] Connexion de {addr}")
        
        # Thread par client
        t = threading.Thread(
            target=reception_message, 
            args=(client, max_client)
        )
        t.daemon = True
        t.start()
```

### file_services.py - Orchestration

```python
def file_services(client_socket, client_id):
    """
    Orchestre: réception → stockage → compilation
    """
    # 1. Réception du fichier
    server_dir = os.getcwd()
    client_dir = f"{server_dir}/client/{client_id}"
    
    os.makedirs(client_dir, exist_ok=True)
    
    client_socket.send('<FILE_SERVICE>'.encode())
    client_socket.send('<FILE_DATA_REQUESTS>'.encode())
    
    file_name = client_socket.recv(1024).decode()
    file_size = client_socket.recv(1024).decode()
    
    # 2. Validation
    if not check_extension(file_name):
        client_socket.send('<FILE_DATA_NOT_READY>'.encode())
        return
    
    # 3. Stockage
    client_socket.send('<FILE_DATA_READY>'.encode())
    
    file_bytes = receive_file_content(client_socket)
    save_file(client_dir, file_name, file_bytes)
    
    client_socket.send('<FILE_RECEIVED>'.encode())
    
    # 4. Compilation et exécution
    compile_services.compile(
        client_socket, 
        f"{client_dir}/{file_name}", 
        client_id
    )
```

### compile_services.py - Compilation

```python
def compile(client_socket, file_name, client_id):
    """
    Détecte le langage et compile/exécute
    """
    client_socket.send("<EXEC_FILE>".encode())
    
    if client_socket.recv(1024).decode() != "<EXEC_FILE_READY>":
        return
    
    file_extension = file_name.split('.')[-1]
    
    # Dispatch selon le langage
    compilers = {
        'py': ('<PYTHON>', compile_python),
        'c': ('<C>', compile_c),
        'cpp': ('<CPP>', compile_cpp),
        'cc': ('<CPP>', compile_cpp),
        'java': ('<JAVA>', compile_java)
    }
    
    if file_extension in compilers:
        lang_tag, compiler_func = compilers[file_extension]
        client_socket.send(lang_tag.encode())
        
        # Compiler et exécuter
        output = compiler_func(file_name, client_id)
        client_socket.send(output.encode())
    else:
        client_socket.send("<ERROR>".encode())

def compile_c(file, client_id):
    """Compile et exécute du code C"""
    output_file = file.replace('.c', '')
    
    # Compilation
    compile_proc = subprocess.run(
        ['gcc', file, '-o', output_file],
        capture_output=True,
        text=True
    )
    
    if compile_proc.returncode != 0:
        return compile_proc.stderr
    
    # Exécution
    exec_proc = subprocess.run(
        [output_file],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    return exec_proc.stdout or exec_proc.stderr
```

## 📊 Exemple d'Utilisation

### Côté Client

```python
# 1. Connexion
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5000))

# 2. Authentification
client.send("<CLIENT_AUTH>".encode())
# ... échange credentials ...

# 3. Envoi de fichier
client.send("<CLIENT_FILE>".encode())
# ... envoi métadonnées et contenu ...

# 4. Réception du résultat
result = client.recv(4096).decode()
print(f"Résultat: {result}")

# 5. Déconnexion
client.send("<CLIENT_QUIT>".encode())
client.close()
```

### Logs Serveur

```
[*] Serveur accepte 3 clients
[*] Écoute sur port 5000
[*] Connexion de ('127.0.0.1', 54321)
[*] client alice authentifié
[*] alice envoie program.py (245 bytes)
[*] Fichier program.py reçu
[*] Compilation de program.py pour alice
[*] Exécution réussie
[*] client alice déconnecté
```

## 🎓 Objectif Pédagogique

Ce module final démontre :
- **Intégration complète** de multiples fonctionnalités
- **Architecture modulaire** avec séparation des responsabilités
- **Pipeline de traitement** (auth → file → compile → execute)
- **Gestion d'état** complexe
- **Multi-threading** pour concurrence
- **Protocole applicatif** complet

## 🔒 Considérations de Sécurité

### Implémenté
- ✅ Authentification obligatoire
- ✅ Isolation des fichiers utilisateur
- ✅ Validation des extensions
- ✅ Timeout d'exécution (30s)
- ✅ Capture des erreurs

### À Améliorer
- ⚠️ Chiffrement des mots de passe
- ⚠️ SSL/TLS pour les communications
- ⚠️ Sandbox d'exécution (Docker)
- ⚠️ Limites de ressources (CPU, RAM)
- ⚠️ Rate limiting
- ⚠️ Logs de sécurité

## 💡 Migration vers Production

Ce module sert de base pour `/SAE302/server/` avec ajouts :

1. **Script d'installation** : `install.sh`
2. **Interface cliente** : PyQt6 GUI
3. **Documentation** : README complets
4. **Tests** : Scripts de validation

## 🔗 Relation avec Autres Modules

```
authentification  ──┐
                    ├──> authAndFile ──┐
file_sending     ──┘                   ├──> authFileExec → PRODUCTION
                                       │
programm_executing ────────────────────┘
```

## 👤 Auteur

Marcelin TRAG - RT22 DevCloud FA
