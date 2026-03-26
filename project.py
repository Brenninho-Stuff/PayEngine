import json
import os

class Project:
    def __init__(self, path: str):
        self.path = path
        self.config = {}

        # Default settings
        self.name = "Unknown Project"
        self.width = 800
        self.height = 600
        self.fps = 60

    def load(self) -> bool:
        config_path = os.path.join(self.path, "config.json")

        if not os.path.exists(config_path):
            print("[PayEngine] config.json not found!")
            return False

        try:
            with open(config_path, "r") as f:
                self.config = json.load(f)
        except Exception as e:
            print(f"[PayEngine] Failed to load config: {e}")
            return False

        # Load config values
        self.name = self.config.get("name", self.name)
        self.width = self.config.get("width", self.width)
        self.height = self.config.get("height", self.height)
        self.fps = self.config.get("fps", self.fps)

        print(f"[PayEngine] Project loaded: {self.name}")
        return True

    def run(self):
        main_file = os.path.join(self.path, "main.py")

        if not os.path.exists(main_file):
            print("[PayEngine] main.py not found!")
            return

        print(f"[PayEngine] Starting project: {self.name}")

        # Execute the project's main file
        try:
            with open(main_file, "r") as f:
                code = f.read()

            exec(code, {
                "__name__": "__main__",
                "__file__": main_file
            })

        except Exception as e:
            print(f"[PayEngine] Error while running project: {e}")
