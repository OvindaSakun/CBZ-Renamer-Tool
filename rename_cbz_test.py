import re
from pathlib import Path

# STRICTLY DRY RUN - WILL NOT RENAME
DRY_RUN = True
DIRECTORY = "." 

def clean_chapter_names():
    target_dir = Path(DIRECTORY)
    
    # 1. Match Chapter or Ch.
    # 2. Capture the number
    # 3. Capture the title (everything else up to the hash)
    # 4. Ignore the _hash at the end (6 to 8 hex characters)
    pattern = re.compile(r"(?i)(?:Chapter|Ch\.?)\s*([\d\.]+)(.*?)(?:_[a-fA-F0-9]{6,8})?$")

    print("🔍 DRY RUN: Checking what will be renamed...\n")
    
    for file_path in target_dir.glob("*.cbz"):
        match = pattern.search(file_path.stem) # Search the filename without .cbz
        if match:
            chapter_num = match.group(1)
            raw_title = match.group(2).strip()
            
            # Clean up any leading hyphens or spaces from the title so we don't get double hyphens
            clean_title = re.sub(r"^[-–—\s]+", "", raw_title)

            # Format the new name depending on whether a title exists
            if clean_title:
                new_name = f"Chapter {chapter_num} - {clean_title}.cbz"
            else:
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