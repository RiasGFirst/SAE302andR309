# Module Program Executing

## 📋 Description

Module responsable de la compilation et de l'exécution des programmes soumis par les clients. Supporte plusieurs langages de programmation avec détection automatique basée sur l'extension du fichier.

## 🏗️ Structure

```
programm_executing/
├── client/
│   └── client.py      # Client de test
└── server/
    └── server.py      # Serveur de compilation/exécution
```

## ✨ Fonctionnalités

- **Compilation Multi-Langage** : Python, C, C++, Java
- **Détection Automatique** : Basée sur l'extension de fichier
- **Exécution Sécurisée** : Capture de stdout/stderr
- **Retour des Résultats** : Sortie ou erreurs de compilation

## 🔧 Langages Supportés

### Python (.py)
- **Interpréteur** : `python`
- **Commande** : `python script.py`
- **Pas de compilation** : Exécution directe

### C (.c)
- **Compilateur** : `gcc`
- **Commande** : `gcc -o output input.c && ./output`
- **Génère** : Exécutable binaire

### C++ (.cpp, .cc)
- **Compilateur** : `g++`
- **Commande** : `g++ -o output input.cpp && ./output`
- **Génère** : Exécutable binaire

### Java (.java)
- **Compilateur** : `javac`
- **Commandes** : 
  - Compilation : `javac Program.java`
  - Exécution : `java Program`
- **Génère** : Fichier .class

## 🚀 Utilisation

### Lancement du Serveur

```bash
cd server
python server.py -p 5000
```

### Test avec le Client

```bash
cd client
python client.py 127.0.0.1 5000 program.py
```

## 🔌 Protocole d'Exécution

```
1. Client → Server: <EXEC_FILE>
2. Server → Client: <EXEC_FILE_READY>
3. Client → Server: <EXEC_FILE_READY>
4. Server détecte le langage (extension)
5. Server → Client: <PYTHON|C|CPP|JAVA>
6. Server compile et exécute
7. Server → Client: [résultat ou erreur]
```

## 🔑 Code Clé

### Fonction Principale de Compilation

```python
def compile(client_socket, file_name, client_id):
    client_socket.send("<EXEC_FILE>".encode())
    msg = client_socket.recv(1024).decode()
    
    if msg == "<EXEC_FILE_READY>":
        file_extension = file_name.split('.')[-1]
        
        if file_extension == "py":
            client_socket.send("<PYTHON>".encode())
            output = compile_python(file_name)
            client_socket.send(output.encode())
            
        elif file_extension == "c":
            client_socket.send("<C>".encode())
            output, error = compile_c(file_name, client_id)
            client_socket.send((output or error).encode())
            
        # ... autres langages
```

### Compilation Python

```python
def compile_python(file):
    result = subprocess.run(
        ['python', file],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.returncode == 0:
        return result.stdout
    else:
        return result.stderr
```

### Compilation C

```python
def compile_c(file, client_id):
    output_file = file.replace('.c', '')
    
    # Compilation
    compile_result = subprocess.run(
        ['gcc', file, '-o', output_file],
        capture_output=True,
        text=True
    )
    
    if compile_result.returncode != 0:
        return None, compile_result.stderr
    
    # Exécution
    exec_result = subprocess.run(
        [output_file],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    return exec_result.stdout, None
```

### Compilation C++

```python
def compile_cpp(file, client_id):
    output_file = file.replace('.cpp', '').replace('.cc', '')
    
    # Compilation avec g++
    compile_result = subprocess.run(
        ['g++', file, '-o', output_file],
        capture_output=True,
        text=True
    )
    
    if compile_result.returncode != 0:
        return None, compile_result.stderr
    
    # Exécution
    exec_result = subprocess.run(
        [output_file],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    return exec_result.stdout, None
```

### Compilation Java

```python
def compile_java(file):
    # Compilation
    compile_result = subprocess.run(
        ['javac', file],
        capture_output=True,
        text=True
    )
    
    if compile_result.returncode != 0:
        return compile_result.stderr
    
    # Extraction du nom de classe
    class_name = os.path.basename(file).replace('.java', '')
    class_dir = os.path.dirname(file)
    
    # Exécution
    exec_result = subprocess.run(
        ['java', '-cp', class_dir, class_name],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    return exec_result.stdout or exec_result.stderr
```

## 🔒 Sécurité

### Mesures Actuelles

- **Timeout** : Limite de 30 secondes par exécution
- **Capture des Sorties** : stdout et stderr capturés
- **Isolation** : Exécution dans le dossier utilisateur

### Vulnérabilités

⚠️ **Limitations de sécurité** :
- Pas de sandbox (le code s'exécute directement sur le serveur)
- Pas de limite de ressources (CPU, mémoire)
- Possibilité d'accès au système de fichiers
- Possibilité d'exécuter des commandes système

### Améliorations Recommandées

```python
# Utiliser Docker pour l'isolation
def compile_in_docker(language, file):
    docker_image = f"compiler-{language}"
    
    result = subprocess.run([
        'docker', 'run', '--rm',
        '--network', 'none',  # Pas d'accès réseau
        '--memory', '512m',   # Limite mémoire
        '--cpus', '1',        # Limite CPU
        '-v', f'{file}:/code/input',
        docker_image,
        '/compile.sh'
    ], capture_output=True, timeout=30)
    
    return result.stdout, result.stderr
```

## 📊 Gestion des Erreurs

### Types d'Erreurs Gérées

1. **Erreurs de Compilation**
   - Syntaxe invalide
   - Imports manquants
   - Erreurs de typage

2. **Erreurs d'Exécution**
   - Exceptions runtime
   - Segmentation faults
   - Timeouts

3. **Erreurs Système**
   - Compilateur manquant
   - Permissions insuffisantes
   - Espace disque insuffisant

### Retour des Erreurs

```python
def format_error(error_type, error_message):
    return f"""
    ═══════════════════════════════
    ❌ ERREUR DE {error_type.upper()}
    ═══════════════════════════════
    
    {error_message}
    
    ═══════════════════════════════
    """
```

## 🎓 Objectif Pédagogique

Ce module démontre :
- Utilisation de subprocess en Python
- Gestion de processus système
- Capture de flux stdout/stderr
- Timeouts et gestion des ressources
- Chaîne de compilation/exécution

## 💡 Améliorations Possibles

### Support de Plus de Langages

```python
LANGUAGE_CONFIG = {
    'go': {
        'compile': ['go', 'build', '-o', 'output'],
        'run': ['./output']
    },
    'rust': {
        'compile': ['rustc', '-o', 'output'],
        'run': ['./output']
    },
    'javascript': {
        'run': ['node']
    }
}
```

### Limites de Ressources

```python
import resource

def set_resource_limits():
    # Limite de temps CPU (secondes)
    resource.setrlimit(resource.RLIMIT_CPU, (5, 5))
    
    # Limite de mémoire (bytes)
    resource.setrlimit(resource.RLIMIT_AS, (512*1024*1024, 512*1024*1024))
```

### Cache de Compilation

```python
import hashlib

def compile_with_cache(file_content):
    file_hash = hashlib.sha256(file_content).hexdigest()
    cache_path = f"cache/{file_hash}"
    
    if os.path.exists(cache_path):
        with open(cache_path) as f:
            return f.read()
    
    # Compiler et cacher le résultat
    result = compile(file_content)
    with open(cache_path, 'w') as f:
        f.write(result)
    
    return result
```

## 🔗 Intégration

Utilisé dans :
- `authFileExec/` : Compilation après réception de fichier
- Système principal : `/SAE302/server/utils/compile_services.py`

## 👤 Auteur

Marcelin TRAG - RT22 DevCloud FA
