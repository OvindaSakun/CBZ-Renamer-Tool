import re
from pathlib import Path

# STRICTLY DRY RUN - WILL NOT RENAME
DRY_RUN = True
DIRECTORY = "." 

def clean_chapter_names():
    target_dir = Path(DIRECTORY)
    
    # Updated Regex:
    # 1. Matches Chapter or Ch.
    # 2. Captures number
    # 3. Captures title (if any)
    # 4. Skips the hash (e.g. _d62595)
    # 5. Captures _opt at the very end (if it exists)
    pattern = re.compile(r"(?i)(?:Chapter|Ch\.?)\s*([\d\.]+)(.*?)(?:_[a-fA-F0-9]{6,8})?(_opt)?$")

    print("🔍 DRY RUN: Checking what will be renamed...\n")
    
    for file_path in target_dir.glob("*.cbz"):
        match = pattern.search(file_path.stem)
        if match:
            chapter_num = match.group(1)
            raw_title = match.group(2).strip()
            is_opt = match.group(3) # Will be '_opt' if found, else None
            
            # Clean up leading hyphens, underscores, or spaces from the title
            clean_title = re.sub(r"^[-–—_\s]+", "", raw_title)
            
            # Keep the _opt suffix if the original file had it
            opt_suffix = "_opt" if is_opt else ""

            if clean_title:
                new_name = f"Chapter {chapter_num} - {clean_title}{opt_suffix}.cbz"
            else:
                new_name = f"Chapter {chapter_num}{opt_suffix}.cbz"

            new_path = file_path.with_name(new_name)

            if file_path == new_path:
                continue 

            if new_path.exists():
                print(f"⚠️ Conflict: Cannot rename '{file_path.name}' -> '{new_name}' (File already exists)")
                continue

            if DRY_RUN:
                print(f"[DRY RUN] '{file_path.name}'  ->  '{new_name}'")
        else:
            pass

if __name__ == "__main__":
    clean_chapter_names()