import os
import subprocess
import sys


def main():
    # Ruta a tu entorno virtual (ajusta según tu proyecto)
    venv_path = os.path.join(os.path.dirname(__file__), '.venv')

    # Comandos a ejecutar
    commands = [
        f'call {os.path.join(venv_path, "Scripts", "activate")}',
        'python manage.py runserver'
    ]

    # Ejecutar comandos en secuencia
    for cmd in commands:
        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar: {cmd}")
            print(e)
            sys.exit(1)


if __name__ == "__main__":
    main()