# Module Client GUI

## 📋 Description

Interface graphique utilisateur développée avec PyQt6 pour le système SAE302. Fournit une interface moderne et intuitive pour interagir avec le serveur de compilation.

## 🏗️ Structure

```
client_gui/
├── client/
│   └── client.py      # Application PyQt6
└── server/
    ├── serve.py       # Serveur compatible GUI
    └── utils/
        └── [modules serveur]
```

## ✨ Fonctionnalités

- **Interface Graphique Moderne** : Design PyQt6 élégant
- **Connexion Visuelle** : Formulaire de connexion intuitif
- **Sélection de Fichiers** : Dialog de sélection intégré
- **Console Temps Réel** : Affichage des logs et résultats
- **Gestion d'État** : Indicateurs visuels de connexion

## 🎨 Composants de l'Interface

### 1. Panneau de Connexion

```python
# Champs de connexion
host_input = QLineEdit()          # IP du serveur
port_input = QLineEdit()          # Port du serveur
username_input = QLineEdit()      # Nom d'utilisateur
password_input = QLineEdit()      # Mot de passe (masqué)

# Boutons d'action
connect_button = QPushButton("Se connecter")
disconnect_button = QPushButton("Se déconnecter")
```

**Layout** :
```
┌─────────────────────────────────┐
│ Host:     [192.168.1.100]       │
│ Port:     [9999]                │
│ Username: [alice]               │
│ Password: [••••••]              │
│ [Se connecter] [Se déconnecter] │
└─────────────────────────────────┘
```

### 2. Panneau de Fichiers

```python
# Sélection de fichier
file_label = QLabel("Aucun fichier sélectionné")
select_file_button = QPushButton("Choisir un fichier")
send_file_button = QPushButton("Envoyer le fichier")
```

**Layout** :
```
┌─────────────────────────────────┐
│ Fichier: program.py             │
│ [Choisir un fichier]            │
│ [Envoyer le fichier]            │
└─────────────────────────────────┘
```

### 3. Console de Sortie

```python
# Console de logs
console_output = QTextEdit()
console_output.setReadOnly(True)
```

**Layout** :
```
┌─────────────────────────────────┐
│ > Connexion établie...          │
│ > Authentifié en tant que alice │
│ > Fichier program.py envoyé     │
│ > Compilation réussie           │
│ > Sortie: Hello World!          │
└─────────────────────────────────┘
```

## 🚀 Utilisation

### Installation des Dépendances

```bash
pip install PyQt6
```

### Lancement de l'Application

```bash
cd client
python client.py
```

## 🔑 Code Principal

### Classe Principale

```python
class CompilerClientGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("SAE302 - Client de Compilation")
        self.setGeometry(100, 100, 800, 600)
        
        # Création des widgets
        self.create_connection_panel()
        self.create_file_panel()
        self.create_console_panel()
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.connection_group)
        main_layout.addWidget(self.file_group)
        main_layout.addWidget(self.console_group)
        
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
```

### Gestion de la Connexion

```python
def server_connection(self):
    host = self.host_input.text()
    port = int(self.port_input.text())
    username = self.username_input.text()
    password = self.password_input.text()
    
    try:
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        
        # Authentification
        self.client_socket.send("<CLIENT_AUTH>".encode())
        
        if self.client_socket.recv(1024).decode() == "<SEND_CLIENT_ID>":
            self.client_socket.send("client".encode())
            time.sleep(0.5)
            self.client_socket.send(username.encode())
            time.sleep(0.5)
            self.client_socket.send(password.encode())
            
            response = self.client_socket.recv(1024).decode()
            
            if response == "<CLIENT_AUTH_SUCCESS>":
                self.is_connected = True
                self.log_to_console(f"✓ Connecté en tant que {username}")
                self.connect_button.setEnabled(False)
                self.disconnect_button.setEnabled(True)
            else:
                self.log_to_console("✗ Échec de l'authentification")
                
    except Exception as e:
        self.log_to_console(f"✗ Erreur de connexion: {e}")
```

### Envoi de Fichier

```python
def select_file(self):
    file_path, _ = QFileDialog.getOpenFileName(
        self,
        "Sélectionner un fichier",
        "",
        "Fichiers source (*.py *.c *.cpp *.cc *.java);;Tous les fichiers (*)"
    )
    
    if file_path:
        self.selected_file = file_path
        self.file_label.setText(f"Fichier: {os.path.basename(file_path)}")
        self.send_file_button.setEnabled(True)

def send_file(self):
    if not self.is_connected:
        self.log_to_console("✗ Pas de connexion active")
        return
    
    if not self.selected_file:
        self.log_to_console("✗ Aucun fichier sélectionné")
        return
    
    try:
        # Envoi du signal de fichier
        self.client_socket.send("<CLIENT_FILE>".encode())
        
        # Attendre la confirmation
        if self.client_socket.recv(1024).decode() == "<FILE_SERVICE>":
            # Envoi des métadonnées et du contenu
            self.upload_file(self.selected_file)
            
    except Exception as e:
        self.log_to_console(f"✗ Erreur d'envoi: {e}")
```

### Mise à Jour de la Console

```python
def log_to_console(self, message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    self.console_output.append(f"[{timestamp}] {message}")
    
    # Auto-scroll vers le bas
    scrollbar = self.console_output.verticalScrollBar()
    scrollbar.setValue(scrollbar.maximum())
```

## 🎨 Personnalisation de l'Interface

### Styles CSS (QSS)

```python
def apply_styles(self):
    style = """
    QMainWindow {
        background-color: #f0f0f0;
    }
    
    QGroupBox {
        border: 2px solid #cccccc;
        border-radius: 5px;
        margin-top: 10px;
        padding: 10px;
        font-weight: bold;
    }
    
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
    }
    
    QPushButton:hover {
        background-color: #45a049;
    }
    
    QPushButton:disabled {
        background-color: #cccccc;
    }
    
    QTextEdit {
        background-color: #1e1e1e;
        color: #00ff00;
        font-family: 'Courier New';
        font-size: 10pt;
    }
    """
    
    self.setStyleSheet(style)
```

## 🔄 Gestion des États

### États de l'Application

```python
class ClientState(Enum):
    DISCONNECTED = 0
    CONNECTING = 1
    CONNECTED = 2
    UPLOADING = 3
    COMPILING = 4

def update_ui_state(self, state):
    if state == ClientState.DISCONNECTED:
        self.connect_button.setEnabled(True)
        self.disconnect_button.setEnabled(False)
        self.send_file_button.setEnabled(False)
        
    elif state == ClientState.CONNECTED:
        self.connect_button.setEnabled(False)
        self.disconnect_button.setEnabled(True)
        self.send_file_button.setEnabled(True)
        
    elif state == ClientState.COMPILING:
        self.send_file_button.setEnabled(False)
        self.send_file_button.setText("Compilation en cours...")
```

## 📊 Fonctionnalités Avancées

### Thread de Réception

```python
def start_receive_thread(self):
    self.receive_thread = threading.Thread(target=self.receive_messages)
    self.receive_thread.daemon = True
    self.receive_thread.start()

def receive_messages(self):
    while self.is_connected:
        try:
            message = self.client_socket.recv(4096).decode()
            self.log_to_console(f"← {message}")
        except:
            break
```

### Barre de Progression

```python
from PyQt6.QtWidgets import QProgressBar

# Ajout d'une barre de progression
self.progress_bar = QProgressBar()
self.progress_bar.setVisible(False)

def upload_with_progress(self, file_path):
    file_size = os.path.getsize(file_path)
    bytes_sent = 0
    
    self.progress_bar.setVisible(True)
    self.progress_bar.setMaximum(file_size)
    
    with open(file_path, 'rb') as f:
        while bytes_sent < file_size:
            chunk = f.read(1024)
            self.client_socket.send(chunk)
            bytes_sent += len(chunk)
            self.progress_bar.setValue(bytes_sent)
    
    self.progress_bar.setVisible(False)
```

## 🎓 Objectif Pédagogique

Ce module démontre :
- Développement d'interfaces graphiques avec PyQt6
- Intégration réseau dans une application GUI
- Threading pour éviter le blocage de l'interface
- Gestion d'états et mise à jour UI
- Design patterns MVC

## 💡 Améliorations Possibles

- Thèmes sombre/clair
- Sauvegarde des préférences
- Historique des fichiers envoyés
- Éditeur de code intégré avec coloration syntaxique
- Support drag & drop
- Notifications système
- Multi-onglets pour plusieurs connexions

## 🔗 Intégration

Le client GUI est compatible avec :
- Tous les serveurs du projet SAE302
- Protocole standard de communication
- Version finale dans `/SAE302/client/`

## 👤 Auteur

Marcelin TRAG - RT22 DevCloud FA
