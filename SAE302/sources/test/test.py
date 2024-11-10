import subprocess

# Compiler le programme C
compile_process = subprocess.run(["gcc", "programmc.c", "-o", "programme"], capture_output=True, text=True)

# Vérifier si la compilation a réussi
if compile_process.returncode == 0:
    print("Compilation réussie.")
else:
    print(f"Erreur de compilation : {compile_process.stderr}")

# Exécuter le programme et capturer la sortie
run_process = subprocess.run(["./programme"], capture_output=True, text=True)

# Enregistrer la sortie dans un fichier
with open("output.txt", "w") as file:
    file.write(run_process.stdout)

print("Sortie enregistrée dans 'output.txt'.")

