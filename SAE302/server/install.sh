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
read -p "Souhaitez-vous créer des utilisateurs ? (oui/non) : " create_users
if [[ "$create_users" == "oui" ]]; then
  users_file="$files_dir/users.txt"
  echo "Ajout des utilisateurs. Entrez 'stop' pour terminer."

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
else
  echo "Aucun utilisateur n'a été créé. Le serveur n'acceptera pas de connexion."
fi

read -p "Souhaitez-vous ajouter des serveurs ? (oui/non) : " add_servers
if [[ "$add_servers" == "oui" ]]; then
  servers_file="$files_dir/servers.json"
else
  echo "Aucun serveur n'a été ajouté."
fi
