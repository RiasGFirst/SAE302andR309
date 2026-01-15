# Module Connexion System

## 📋 Description

Système de gestion des connexions distribuées avec architecture master-slave. Ce module implémente la distribution de charge entre plusieurs serveurs de compilation pour gérer un grand nombre de clients simultanés.

## 🏗️ Architecture

```
connexion_sys/
├── client/
│   └── client.py            # Client standard
└── master_server/
    ├── serve.py             # Serveur maître
    ├── models/
    │   ├── Server.py        # Modèle de serveur
    │   └── __init__.py
    └── utils/
        ├── check_compilor.py
        └── __init__.py
```

## ✨ Fonctionnalités

- **Serveur Maître** : Gestion centralisée des connexions
- **Distribution de Charge** : Redirection automatique vers serveurs disponibles
- **Monitoring** : Vérification de l'état des serveurs esclaves
- **Scalabilité** : Support de multiples serveurs de compilation
- **Failover** : Gestion des défaillances de serveurs

## 🏛️ Architecture Master-Slave

### Serveur Maître (Master)

Le serveur maître est responsable de :
- Accepter les connexions clients initiales
- Authentifier les utilisateurs
- Vérifier la disponibilité des serveurs esclaves
- Rediriger les clients vers des serveurs disponibles
- Maintenir la configuration des serveurs

### Serveurs Esclaves (Slaves)

Les serveurs esclaves :
- Sont des instances de serveur de compilation
- Reçoivent les clients redirigés
- Effectuent la compilation et l'exécution
- Reportent leur état au maître (implicitement)

## 📊 Flux de Connexion

### Scénario 1 : Serveur Maître Disponible

```
1. Client → Master: Demande de connexion
2. Master: Authentifie le client
3. Master: Vérifie sa propre disponibilité
4. Si disponible:
   Master → Client: <SEND_CLIENT_DATA>
   Client reste connecté au master
```

### Scénario 2 : Redirection vers Slave

```
1. Client → Master: Demande de connexion
2. Master: Authentifie le client
3. Master: Trop de clients connectés
4. Master: Vérifie les serveurs slaves
5. Master → Client: <CLIENT_EXCEEDED>
6. Master → Client: <SERVER_AVAILABLE>
7. Master → Client: "192.168.1.100:9999"
8. Client se déconnecte du master
9. Client → Slave: Nouvelle connexion
```

### Scénario 3 : Aucun Serveur Disponible

```
1. Client → Master: Demande de connexion
2. Master: Authentifie le client
3. Master: Trop de clients
4. Master: Vérifie les serveurs slaves
5. Tous les slaves indisponibles
6. Master → Client: <SERVER_NOT_AVAILABLE>
7. Client déconnecté
```

## 🔧 Configuration

### Fichier servers.json

```json
{
  "PASSWORD": "master_password",
  "SERVERS": {
    "slave1": {
      "IP": "192.168.1.100",
      "PORT": 9999,
      "PASSWORD": "slave1_password"
    },
    "slave2": {
      "IP": "192.168.1.101",
      "PORT": 9999,
      "PASSWORD": "slave2_password"
    },
    "slave3": {
      "IP": "192.168.1.102",
      "PORT": 9999,
      "PASSWORD": "slave3_password"
    }
  }
}
```

## 🚀 Utilisation

### Démarrage du Serveur Maître

```bash
cd master_server
python serve.py run master 5000 2
```

Arguments :
- `run` : Mode de lancement
- `master` : Type de serveur (master ou slave)
- `5000` : Port d'écoute
- `2` : Nombre maximum de clients

### Démarrage des Serveurs Esclaves

```bash
# Sur chaque machine esclave
cd server
python serve.py -p 9999 -c 5
```

### Installation Initiale

```bash
python serve.py install
```

Vérifie la présence des compilateurs :
- gcc (C)
- g++ (C++)
- javac (Java)
- python (Python)

## 🔑 Code Principal

### Modèle Server (Server.py)

```python
class Server:
    def __init__(self, name, ip, port, password):
        self.name = name
        self.ip = ip
        self.port = port
        self.password = password
        self.status = "unknown"
        
    def check_availability(self):
        """Vérifie si le serveur est disponible"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((self.ip, self.port))
            
            # Test d'authentification serveur
            s.send("<SERVER_AUTH>".encode())
            response = s.recv(1024).decode()
            
            s.close()
            
            if response == "<SERVER_AUTH_SUCCESS>":
                self.status = "AVAILABLE"
                return True
            else:
                self.status = "UNAVAILABLE"
                return False
                
        except:
            self.status = "UNAVAILABLE"
            return False
            
    def __str__(self):
        return f"Server({self.name}, {self.ip}:{self.port}, {self.status})"
```

### Gestion de la Redirection

```python
def handle_client_overflow(client_socket, client_id):
    servers_config = load_servers_config()
    
    for server_name, server_info in servers_config["SERVERS"].items():
        server = Server(
            server_name,
            server_info["IP"],
            server_info["PORT"],
            server_info["PASSWORD"]
        )
        
        if server.check_availability():
            # Informer le client de la redirection
            client_socket.send("<CLIENT_EXCEEDED>".encode())
            time.sleep(0.5)
            client_socket.send("<SERVER_AVAILABLE>".encode())
            time.sleep(0.5)
            
            redirect_info = f"{server.ip}:{server.port}"
            client_socket.send(redirect_info.encode())
            
            print(f"Client {client_id} redirigé vers {server_name}")
            return True
    
    # Aucun serveur disponible
    client_socket.send("<SERVER_NOT_AVAILABLE>".encode())
    print(f"Impossible de rediriger le client {client_id}")
    return False
```

### Vérification des Serveurs

```python
def monitor_servers():
    """Thread de monitoring des serveurs"""
    while True:
        servers_config = load_servers_config()
        
        for server_name, server_info in servers_config["SERVERS"].items():
            server = Server(
                server_name,
                server_info["IP"],
                server_info["PORT"],
                server_info["PASSWORD"]
            )
            
            is_available = server.check_availability()
            
            print(f"[Monitor] {server_name}: {server.status}")
        
        time.sleep(30)  # Vérifier toutes les 30 secondes
```

## 📊 Métriques et Monitoring

### État des Serveurs

```python
server_metrics = {
    'master': {
        'clients_connected': 2,
        'max_clients': 2,
        'uptime': '2h 34m',
        'requests_handled': 156
    },
    'slave1': {
        'status': 'AVAILABLE',
        'clients_connected': 3,
        'last_check': '2024-01-15 10:30:00'
    },
    'slave2': {
        'status': 'UNAVAILABLE',
        'clients_connected': 0,
        'last_check': '2024-01-15 10:30:00'
    }
}
```

## 🔒 Sécurité

### Authentification Serveur-Serveur

```python
def authenticate_slave(slave_socket, expected_password):
    slave_socket.send("<SERVER_AUTH_REQUEST>".encode())
    
    received_password = slave_socket.recv(1024).decode()
    
    if received_password == expected_password:
        slave_socket.send("<SERVER_AUTH_SUCCESS>".encode())
        return True
    else:
        slave_socket.send("<SERVER_AUTH_FAILED>".encode())
        return False
```

## 🎓 Objectif Pédagogique

Ce module enseigne :
- Architecture distribuée master-slave
- Load balancing (distribution de charge)
- Failover et haute disponibilité
- Monitoring de services
- Communication inter-serveurs
- Gestion de configuration distribuée

## 💡 Améliorations Possibles

### Round-Robin Load Balancing

```python
class LoadBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.current_index = 0
        
    def get_next_server(self):
        """Rotation circulaire entre les serveurs"""
        available_servers = [s for s in self.servers if s.is_available()]
        
        if not available_servers:
            return None
            
        server = available_servers[self.current_index % len(available_servers)]
        self.current_index += 1
        
        return server
```

### Least Connections

```python
def get_least_loaded_server(servers):
    """Retourne le serveur avec le moins de connexions"""
    available_servers = [s for s in servers if s.is_available()]
    
    if not available_servers:
        return None
        
    return min(available_servers, key=lambda s: s.get_client_count())
```

### Health Checks Actifs

```python
def active_health_check(server):
    """Test complet de santé du serveur"""
    checks = {
        'network': test_connectivity(server),
        'authentication': test_auth(server),
        'compilation': test_compile(server),
        'resources': check_resources(server)
    }
    
    return all(checks.values())
```

### Service Discovery

```python
def discover_servers():
    """Découverte automatique de serveurs"""
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    # Broadcast de découverte
    broadcast_socket.sendto(
        b"<DISCOVER_SERVERS>",
        ('255.255.255.255', 9998)
    )
    
    # Écoute des réponses
    servers = []
    while True:
        try:
            data, addr = broadcast_socket.recvfrom(1024)
            server_info = json.loads(data.decode())
            servers.append(server_info)
        except socket.timeout:
            break
    
    return servers
```

## 🔗 Intégration

Ce système est utilisé dans :
- Système principal avec `files/servers.json`
- Module `authFileExec/` pour distribution
- Production : `/SAE302/server/`

## 👤 Auteur

Marcelin TRAG - RT22 DevCloud FA
