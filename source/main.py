import os
import sys

# Add root folder to path (so we can import project.py)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from project import Project

# =========================
# ENGINE ENTRY POINT
# =========================

def main():
    print("[PayEngine] Booting...")

    # Default project path
    project_path = os.path.join("projects", "MyGame")

    # Create project instance
    project = Project(project_path)

    # Validate project structure
    if not os.path.exists(project_path):
        print(f"[PayEngine] Project folder not found: {project_path}")
        return

    if not project.load():
        print("[PayEngine] Failed to load project.")
        return

    # Run project
    project.run()


# =========================
# START
# =========================

if __name__ == "__main__":
    main()
