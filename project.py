import json
import os
import importlib.util

class Project:
    def __init__(self, path: str):
        self.path = os.path.abspath(path)
        self.config = {}

        # Default settings
        self.name = "Unknown Project"
        self.width = 800
        self.height = 600
        self.fps = 60

        # Icon
        self.icon_path = os.path.join(self.path, "arts", "icon.png")

        self.main_module = None

    # =========================
    # LOAD CONFIG
    # =========================
    def load(self) -> bool:
        config_path = os.path.join(self.path, "config.json")

        if not os.path.exists(config_path):
            print("[PayEngine] ERROR: config.json not found!")
            return False

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        except Exception as e:
            print(f"[PayEngine] ERROR reading config: {e}")
            return False

        # Apply config
        self.name = self.config.get("name", self.name)
        self.width = self.config.get("width", self.width)
        self.height = self.config.get("height", self.height)
        self.fps = self.config.get("fps", self.fps)

        print(f"[PayEngine] Loaded project: {self.name}")
        print(f"[PayEngine] Resolution: {self.width}x{self.height} | FPS: {self.fps}")

        return True

    # =========================
    # LOAD ICON (PYGAME)
    # =========================
    def apply_icon(self):
        if not os.path.exists(self.icon_path):
            print("[PayEngine] WARNING: icon.png not found")
            return

        try:
            import pygame
            icon = pygame.image.load(self.icon_path)
            pygame.display.set_icon(icon)
            print("[PayEngine] Icon loaded successfully")
        except Exception as e:
            print(f"[PayEngine] ERROR loading icon: {e}")

    # =========================
    # LOAD MAIN MODULE
    # =========================
    def load_main(self) -> bool:
        main_path = os.path.join(self.path, "main.py")

        if not os.path.exists(main_path):
            print("[PayEngine] ERROR: main.py not found!")
            return False

        try:
            spec = importlib.util.spec_from_file_location("project_main", main_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            self.main_module = module
            return True

        except Exception as e:
            print(f"[PayEngine] ERROR loading main module: {e}")
            return False

    # =========================
    # RUN PROJECT
    # =========================
    def run(self):
        if not self.load_main():
            return

        print(f"[PayEngine] Starting project: {self.name}")

        try:
            import pygame
            pygame.init()
            pygame.display.set_caption(self.name)

            # 👇 aplica o ícone AQUI
            self.apply_icon()

        except:
            print("[PayEngine] Pygame not initialized yet")

        # Start game
        if hasattr(self.main_module, "start"):
            try:
                self.main_module.start(self)
            except Exception as e:
                print(f"[PayEngine] ERROR running start(): {e}")
        else:
            print("[PayEngine] WARNING: No start(project) function found")

    # =========================
    # VALIDATE
    # =========================
    def validate(self) -> bool:
        required = ["config.json", "main.py"]

        missing = [
            file for file in required
            if not os.path.exists(os.path.join(self.path, file))
        ]

        if missing:
            print("[PayEngine] Missing files:")
            for f in missing:
                print(f" - {f}")
            return False

        return True

    # =========================
    # GET INFO
    # =========================
    def get_info(self) -> dict:
        return {
            "name": self.name,
            "resolution": (self.width, self.height),
            "fps": self.fps,
            "icon": self.icon_path,
            "path": self.path
        }