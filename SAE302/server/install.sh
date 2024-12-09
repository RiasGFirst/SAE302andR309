#!/bin/bash

# Mettre le répertoire actuel dans une variable
current_dir=$(pwd)
echo "Le répertoire actuel est : $current_dir"

# Créer un environnement virtuel Python
echo "Création d'un environnement virtuel Python..."
python3 -m venv "$current_dir/venv"
echo "Environnement virtuel créé dans $current_dir/venv"

# Créer un dossier client
client_dir="$current_dir/client"
if [ ! -d "$client_dir" ]; then
  mkdir "$client_dir"
  echo "Dossier 'client' créé dans $client_dir"
else
  echo "Le dossier 'client' existe déjà."
fi

# Créer un dossier files pour les utilisateurs
files_dir="$current_dir/files"
if [ ! -d "$files_dir" ]; then
  mkdir "$files_dir"
  echo "Dossier 'files' créé dans $files_dir"
else
  echo "Le dossier 'files' existe déjà."
fi

# Demander si l'utilisateur souhaite créer des utilisateurs
users_file="$files_dir/users.txt"
echo "Ajout des utilisateurs (min 1). Entrez 'stop' pour terminer."

while true; do
  read -p "Entrez le nom d'utilisateur (ou 'stop' pour terminer) : " username
  if [[ "$username" == "stop" ]]; then
    break
  fi
  read -p "Entrez le mot de passe pour $username : " password
  echo "$username:$password" >> "$users_file"
  echo "Utilisateur $username ajouté."
done

echo "Les utilisateurs ont été enregistrés dans $users_file."

# Ajouter des serveurs
read -p "Souhaitez-vous ajouter des serveurs ? (oui/non) : " add_servers
if [[ "$add_servers" == "oui" ]]; then
  servers_file="$files_dir/servers.json"
  echo "Ajout des serveurs. Entrez 'stop' pour terminer."

  # Demander le mot de passe principal
  read -p "Entrez le mot de passe principal du serveur : " thisserver_password

  # Créer la structure JSON initiale
  echo "{
  \"PASSWORD\": \"$thisserver_password\",
  \"SERVERS\": {
  }
}" > "$servers_file"

  # Ajouter des serveurs
  while true; do
    read -p "Entrez un nom pour le serveur (ou 'stop' pour terminer) : " server_name
    if [[ "$server_name" == "stop" ]]; then
      break
    fi

    read -p "Entrez l'adresse IP du serveur : " server_ip
    read -p "Entrez le port du serveur : " server_port
    read -p "Entrez le mot de passe du serveur : " server_password

    # Ajouter le serveur au fichier JSON
    python3 - <<EOF
import json

file_path = "$servers_file"

# Charger le fichier JSON existant
with open(file_path, "r") as f:
    data = json.load(f)

# Ajouter un serveur
data["SERVERS"]["$server_name"] = {
    "IP": "$server_ip",
    "PORT": int($server_port),
    "PASSWORD": "$server_password"
}

# Enregistrer les modifications
with open(file_path, "w") as f:
    json.dump(data, f, indent=2)
EOF

    echo "Serveur $server_name ajouté."
  done

  echo "Tous les serveurs ont été enregistrés dans $servers_file."
else
  echo "Aucun serveur n'a été ajouté."
fi

echo "Installation terminée."
echo "Pour activer l'environnement virtuel, exécutez : source $current_dir/venv/bin/activate"

# Lancer le serveur
echo "Pour lancer le serveur, exécutez : python $current_dir/server.py"