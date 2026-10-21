import re
from pathlib import Path

# Set to False to actually rename the files. 
# It is currently True so you can test it safely first.
DRY_RUN = True
DIRECTORY = "." # Target directory (defaults to current folder)

def clean_chapter_names():
    target_dir = Path(DIRECTORY)
    
    # Regex looks for 'Chapter' or 'Ch.' (case insensitive) followed by numbers/decimals
    pattern = re.compile(r"(?i)(?:Chapter|Ch\.?)\s*([\d\.]+)")

    for file_path in target_dir.glob("*.cbz"):
        match = pattern.search(file_path.name)
        
        if match:
            chapter_num = match.group(1)
            new_name = f"Chapter {chapter_num}.cbz"
            new_path = file_path.with_name(new_name)

            if file_path == new_path:
                continue # Already correctly named

            if new_path.exists():
                print(f"⚠️ Conflict: Cannot rename '{file_path.name}' -> '{new_name}' (File already exists)")
                continue

            if DRY_RUN:
                print(f"[DRY RUN] '{file_path.name}'  ->  '{new_name}'")
            else:
                file_path.rename(new_path)
                print(f"✅ Renamed: '{file_path.name}'  ->  '{new_name}'")
        else:
            print(f"⏭️ Skipped (No pattern match): '{file_path.name}'")

if __name__ == "__main__":
    clean_chapter_names()