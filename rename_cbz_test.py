import re
from pathlib import Path

# STRICTLY DRY RUN - WILL NOT RENAME
DRY_RUN = True
DIRECTORY = "." 

def get_user_choice():
    print("\n--- Renaming Options ---")
    print("1. Only Chapter Number (e.g., Chapter 10.cbz)")
    print("2. Keep All 3          (e.g., [Tenuous Scans] Chapter 10 - Defense Battle.cbz)")
    print("3. Keep Num & Title    (e.g., Chapter 10 - Defense Battle.cbz)")
    print("4. Keep Group & Num    (e.g., [Tenuous Scans] Chapter 10.cbz)")
    
    while True:
        choice = input("\nEnter choice (1-4): ").strip()
        if choice in ('1', '2', '3', '4'):
            return int(choice)
        print("Invalid choice. Please enter 1, 2, 3, or 4.")

def format_new_name(option, group_name, chapter_num, title, opt_suffix):
    parts = []
    
    # Add Group if option 2 or 4 (and a group actually exists)
    if option in (2, 4) and group_name:
        parts.append(f"[{group_name}]")
    
    parts.append(f"Chapter {chapter_num}")
    
    # Add Title if option 2 or 3 (and a title actually exists)
    if option in (2, 3) and title:
        parts.append(f"- {title}")
        
    base_name = " ".join(parts)
    return f"{base_name}{opt_suffix}.cbz"

def clean_chapter_names():
    target_dir = Path(DIRECTORY)
    
    # Ask user for formatting style
    option = get_user_choice()

    # Regex properly separates Group, Chapter Number, Title, Hash, and _opt
    pattern = re.compile(r"^(.*?_)?(?:Vol\.\d+\s+)?(?i)(?:Chapter|Ch\.?)\s*([\d\.]+)(.*?)(?:_[a-fA-F0-9]{6,8})?(_opt)?$")

    print(f"\n🔍 DRY RUN: Simulating Option {option}...\n")
    
    for file_path in target_dir.glob("*.cbz"):
        match = pattern.search(file_path.stem)
        if match:
            raw_group = match.group(1) or ""
            chapter_num = match.group(2)
            raw_title = match.group(3) or ""
            is_opt = match.group(4)
            
            # Clean up extracted parts (strip leading/trailing underscores, hyphens, and spaces)
            group_name = re.sub(r"_+(\s*_+)*$", "", raw_group).strip(" _-")
            title = re.sub(r"^[-–—_\s]+", "", raw_title).strip(" _-")
            opt_suffix = "_opt" if is_opt else ""

            # Build the new name
            new_name = format_new_name(option, group_name, chapter_num, title, opt_suffix)
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