import json

# Nom du fichier à vérifier
file_name = "hentai.py"
file_extension = file_name.split(".")[-1]
print(file_extension)
# Liste des extensions possibles
extensions = ['cpp', 'c', 'java', 'py']

# Charger le fichier JSON contenant les informations sur les compilateurs
with open("compilateurs.json", "r") as file:
    data = json.load(file)
    if file_extension not in extensions:
        print(f"L'extension '.{file_extension}' n'est pas supportée.")
    else:
        ext_lang_mapping = {
            "cpp": "C++",
            "c": "C",
            "java": "Java",
            "py": "Python"
        }
        language = ext_lang_mapping.get(file_extension)

        # Vérifier si le langage est exécutable
        if language and data.get(language, False):
            print(f"L'extension '.{file_extension}' est exécutable.")
        else:
            print(f"L'extension '.{file_extension}' n'est pas exécutable.")

