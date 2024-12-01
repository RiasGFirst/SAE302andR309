import subprocess
import json
import os

def verify_compile(compilateurs) -> None:
    """
    :param compilateurs:
    :return:
    """
    current_directory = os.getcwd()
    json_data = {}
    for language, command in compilateurs.items():
        print(f"Vérification du compilateur {language} :")
        try:
            # Exécute la commande avec l'option `--version` ou `-version` pour obtenir sa version
            result = subprocess.run([command, "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"{command} est installé :\n{result.stdout.splitlines()[0]}")
                json_data[language] = True
        except FileNotFoundError:
            print(f"{command} n'est pas installé.")
            json_data[language] = False
        print()
    if os.path.exists(f"{current_directory}/files/compilateurs.json"):
        os.remove(f"{current_directory}/files/compilateurs.json")
    json_data = json.dumps(json_data)
    with open(f"{current_directory}/files/compilateurs.json", "w") as file:
        file.write(json_data)