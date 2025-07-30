# BossSuperPack root __init__.py
import importlib
import os

NODE_CLASS_MAPPINGS = {}

base = os.path.dirname(__file__)
for folder in os.listdir(base):
    subdir = os.path.join(base, folder)
    if os.path.isdir(subdir) and not folder.startswith("__"):
        sub_init = os.path.join(subdir, "__init__.py")
        if os.path.isfile(sub_init):
            try:
                # Dynamically import the submodule
                module = importlib.import_module(f".{folder}", __name__)
                # Each submodule should export NODE_CLASS_MAPPINGS
                sub_mappings = getattr(module, "NODE_CLASS_MAPPINGS", None)
                if sub_mappings:
                    NODE_CLASS_MAPPINGS.update(sub_mappings)
            except Exception as e:
                print(f"[BossSuperPack] Failed to import '{folder}': {e}")

print("\033[34mBossSuperPack: \033[92mAll custom nodes loaded!\033[0m")

