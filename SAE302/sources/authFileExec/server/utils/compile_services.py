import subprocess


def compile_python(file_name):
    compile_process = subprocess.run(['python', file_name], capture_output=True, text=True)

    if compile_process.returncode == 0:
        print(compile_process.stdout)
    else:
        print(compile_process.stderr)


