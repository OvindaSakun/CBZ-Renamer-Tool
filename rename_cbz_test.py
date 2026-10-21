import re
from pathlib import Path

# STRICTLY DRY RUN - WILL NOT RENAME
DRY_RUN = True
# Uses the current folder you are running the command from
DIRECTORY = "." 

def clean_chapter_names():
    target_dir = Path(DIRECTORY)
    pattern = re.compile(r"(?i)(?:Chapter|Ch\.?)\s*([\d\.]+)")

    print("🔍 DRY RUN: Checking what will be renamed...\n")
    
    for file_path in target_dir.glob("*.cbz"):
        match = pattern.search(file_path.name)
        if match:
            chapter_num = match.group(1)
            new_name = f"Chapter {chapter_num}.cbz"
            new_path = file_path.with_name(new_name)

            if file_path == new_path:
                continue 

            if new_path.exists():
                print(f"⚠️ Conflict: Cannot rename '{file_path.name}' -> '{new_name}' (File already exists)")
                continue

            if DRY_RUN:
                print(f"[DRY RUN] '{file_path.name}'  ->  '{new_name}'")
        else:
            pass # Skipping print for non-matches to keep terminal clean

if __name__ == "__main__":
    clean_chapter_names()