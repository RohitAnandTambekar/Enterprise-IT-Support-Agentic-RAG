from pathlib import Path

path_obj= Path()

root = Path.cwd()

folders = [
    "app/api",
    "app/core",
    "app/rag",
    "app/services",
    "data",
    "templates",
    "static",
    "uploads",
    "tests",
]

files = [
    "app/main.py",
    "ingest_sample_kb.py",
    "run.py",
    ".env",
]

# print(root)

# for folder_path in folders:
#     sub_folder = root / folder_path
#     sub_folder.mkdir(parents=True, exist_ok=True)

for file_path in files:
    file = root / file_path
    file.touch(exist_ok=True)