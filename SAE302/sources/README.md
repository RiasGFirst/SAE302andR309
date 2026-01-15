# Sources SAE302

## 📋 Description

Ce dossier contient les différentes itérations et modules de développement du projet SAE302. Chaque sous-dossier représente une étape ou une fonctionnalité spécifique du système de compilation client-serveur.

## 📁 Structure des Modules

### Modules de Fonctionnalités Individuelles

#### [authentification/](authentification/README.md)
Module de base pour l'authentification des clients.
- Système de login/password
- Gestion des sessions
- Version simple sans gestion de fichiers

#### [file_sending/](file_sending/README.md)
Module dédié à l'envoi de fichiers.
- Upload de fichiers source
- Protocole de transfert TCP
- Validation des fichiers

#### [file_sys/](file_sys/README.md)
Système de gestion de fichiers côté serveur.
- Organisation des fichiers par utilisateur
- Stockage et récupération
- Gestion des permissions

#### [programm_executing/](programm_executing/README.md)
Module d'exécution de programmes.
- Compilation de code
- Exécution sécurisée
- Retour des résultats

#### [client_gui/](client_gui/README.md)
Interface graphique utilisateur.
- Application PyQt6
- Interface moderne et intuitive
- Gestion visuelle des connexions

#### [connexion_sys/](connexion_sys/README.md)
Système de gestion des connexions et serveur maître.
- Serveur maître (master_server)
- Distribution de charge
- Gestion des serveurs esclaves

### Modules Combinés

#### [authAndFile/](authAndFile/README.md)
Combinaison authentification + gestion de fichiers.
- Authentification intégrée
- Upload de fichiers authentifié
- Base pour le système complet

#### [authFileExec/](authFileExec/README.md)
Système complet : authentification + fichiers + exécution.
- Authentification
- Transfert de fichiers
- Compilation et exécution
- Version finale intégrée

### Dossiers de Test

#### test/
Scripts de test pour le développement.
- `compilator_check_testing.py` : Test des compilateurs
- `file_sending.py` : Test d'envoi de fichiers
- `test.py`, `test2.py` : Tests divers
- `compilateurs.json` : Configuration de test

#### testfile/
Fichiers de test pour la compilation.
- `file.c` : Exemple C
- `file.cc` : Exemple C++
- `file.java` : Exemple Java
- `file.py` : Exemple Python
- `file.txt` : Fichier texte de test

## 🔄 Évolution du Projet

Le projet a suivi une approche modulaire de développement :

```
1. authentification          → Système d'auth basique
2. file_sending             → Ajout transfert de fichiers
3. file_sys                 → Système de fichiers
4. programm_executing       → Compilation et exécution
5. authAndFile             → Intégration auth + fichiers
6. client_gui              → Interface graphique
7. connexion_sys           → Système distribué
8. authFileExec            → Version complète intégrée
```

## 🎯 Utilisation des Modules

### Modules Indépendants

Chaque module peut être testé indépendamment pour comprendre une fonctionnalité spécifique :

```bash
# Test de l'authentification
cd authentification/server
python serve.py -p 5000

# Test du GUI
cd client_gui/client
python client.py
```

### Version Complète

Pour le système complet, utiliser les dossiers à la racine :
- `/SAE302/server/` : Serveur de production
- `/SAE302/client/` : Client de production

## 🔍 Navigation

Pour explorer un module spécifique, consultez son README :

- [authentification/README.md](authentification/README.md)
- [file_sending/README.md](file_sending/README.md)
- [file_sys/README.md](file_sys/README.md)
- [programm_executing/README.md](programm_executing/README.md)
- [client_gui/README.md](client_gui/README.md)
- [connexion_sys/README.md](connexion_sys/README.md)
- [authAndFile/README.md](authAndFile/README.md)
- [authFileExec/README.md](authFileExec/README.md)

## 📚 Documentation

Chaque module contient :
- Code source (client et/ou server)
- Fichiers de configuration d'exemple
- Scripts de test si applicable

## 💡 Pour les Développeurs

### Ajout de Nouvelles Fonctionnalités

1. Créer un nouveau module dans `sources/`
2. Tester indépendamment
3. Intégrer dans le système principal (`/SAE302/server/` et `/SAE302/client/`)
4. Documenter dans un README.md

### Structure Recommandée

```
nouveau_module/
├── README.md
├── client/
│   └── client.py
└── server/
    ├── serve.py
    └── utils/
```

## 🐛 Débogage

Pour déboguer une fonctionnalité :
1. Identifier le module correspondant
2. Tester le module isolément
3. Comparer avec la version intégrée
4. Utiliser les fichiers de test

## 👤 Auteur

Marcelin TRAG - RT22 DevCloud FA
