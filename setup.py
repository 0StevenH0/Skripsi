import os
import subprocess
import sys
import venv
import shutil

class VenvManager:
    def __init__(self):
        self.venv_name = ".venv"
        self.requirements_file = "requirements.txt"
        self.current_dir = os.getcwd()
        self.venv_path = os.path.join(self.current_dir, self.venv_name)

    def remove_venv(self):
        if os.path.exists(self.venv_path):
            print(f"Removing existing virtual environment '{self.venv_name}'...")
            shutil.rmtree(self.venv_path)
            print("Virtual environment removed.")

    def create_venv(self):
        if not os.path.exists(self.venv_path):
            print(f"Creating virtual environment '{self.venv_name}' in the current directory...")
            venv.create(self.venv_path, with_pip=True)
            print(f"Virtual environment created successfully.")
        else:
            print(f"Virtual environment already exists in the current directory.")

    def get_venv_python(self):
        if sys.platform == "win32":
            return os.path.join(self.venv_path, "Scripts", "python.exe")
        return os.path.join(self.venv_path, "bin", "python")

    def install_requirements(self):
        if os.path.exists(self.requirements_file):
            print(f"Installing requirements from '{self.requirements_file}'...")
            venv_python = self.get_venv_python()
            subprocess.run([venv_python, "-m", "pip", "install", "-r", self.requirements_file], check=True)
            print("Requirements installed successfully.")
        else:
            print(f"Error: Requirements file '{self.requirements_file}' not found.")

    def run(self):
        # ONLY USE IF NECESSARRY
        # self.remove_venv()

        self.create_venv()
        self.install_requirements()
        print("\nVirtual environment setup complete and requirements installed.")
        print(f"to run : {self.get_activate_command()}")

    def run_script(self, script_name):
        venv_python = self.get_venv_python()
        print(f"Running {script_name} in the virtual environment...")
        subprocess.run([venv_python, script_name])

    def get_activate_command(self):
        if sys.platform == "win32":
            return os.path.join(self.venv_name, "Scripts", "activate")
        else:
            return f"source {os.path.join(self.venv_path, 'bin', 'activate')}"

if __name__ == "__main__":
    manager = VenvManager()
    manager.run()
