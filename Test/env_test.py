import sys
import os

def print_environment_info():
    # Get the current Python executable path
    python_executable = sys.executable

    # Get the Python version
    python_version = sys.version

    # Get the environment variables related to the virtual environment
    venv_vars = {
        'VIRTUAL_ENV': os.getenv('VIRTUAL_ENV'),
        'CONDA_PREFIX': os.getenv('CONDA_PREFIX'),
        'PIPENV_VENV_IN_PROJECT': os.getenv('PIPENV_VENV_IN_PROJECT'),
        'PIPENV_ACTIVE': os.getenv('PIPENV_ACTIVE'),
    }

    print("Python Executable Path:", python_executable)
    print("Python Version:", python_version)
    print("\nEnvironment Variables Related to Virtual Environments:")
    for var, value in venv_vars.items():
        print(f"{var}: {value}")

    if venv_vars['VIRTUAL_ENV']:
        print("\nYou are in a virtual environment created with venv or virtualenv.")
    elif venv_vars['CONDA_PREFIX']:
        print("\nYou are in a Conda environment.")
    elif venv_vars['PIPENV_ACTIVE']:
        print("\nYou are in a Pipenv environment.")
    else:
        print("\nYou are not in any known virtual environment.")

if __name__ == "__main__":
    print_environment_info()
