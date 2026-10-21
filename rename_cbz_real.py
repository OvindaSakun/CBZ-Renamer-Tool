import re
from pathlib import Path

# STRICTLY REAL RUN - WILL RENAME FILES
DRY_RUN = False
DIRECTORY = "." 

def clean_chapter_names():
    target_dir = Path(DIRECTORY)
    pattern = re.compile(r"(?i)(?:Chapter|Ch\.?)\s*([\d\.]+)")

    print("⚠️ EXECUTING REAL RENAME...\n")

    for file_path in target_dir.glob("*.cbz"):
        match = pattern.search(file_path.name)
        if match:
            chapter_num = match.group(1)
            new_name = f"Chapter {chapter_num}.cbz"
            new_path = file_path.with_name(new_name)

            if file_path == new_path:
                continue 

            if new_path.exists():
                print(f"⚠️ Conflict: '{file_path.name}' -> '{new_name}' (File already exists)")
                continue

            if not DRY_RUN:
                file_path.rename(new_path)
                print(f"✅ Renamed: '{file_path.name}'  ->  '{new_name}'")
        else:
            pass

if __name__ == "__main__":
    clean_chapter_names()