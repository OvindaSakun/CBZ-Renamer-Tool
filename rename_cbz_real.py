import re
from pathlib import Path

# STRICTLY REAL RUN - WILL RENAME FILES
DRY_RUN = False
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
    
    if option in (2, 4) and group_name:
        parts.append(f"[{group_name}]")
    
    parts.append(f"Chapter {chapter_num}")
    
    if option in (2, 3) and title:
        parts.append(f"- {title}")
        
    base_name = " ".join(parts)
    return f"{base_name}{opt_suffix}.cbz"

def clean_chapter_names():
    target_dir = Path(DIRECTORY)
    option = get_user_choice()

    pattern = re.compile(r"^(.*?_)?(?:Vol\.\d+\s+)?(?i)(?:Chapter|Ch\.?)\s*([\d\.]+)(.*?)(?:_[a-fA-F0-9]{6,8})?(_opt)?$")

    print(f"\n⚠️ EXECUTING REAL RENAME for Option {option}...\n")

    for file_path in target_dir.glob("*.cbz"):
        match = pattern.search(file_path.stem)
        if match:
            raw_group = match.group(1) or ""
            chapter_num = match.group(2)
            raw_title = match.group(3) or ""
            is_opt = match.group(4)
            
            group_name = re.sub(r"_+(\s*_+)*$", "", raw_group).strip(" _-")
            title = re.sub(r"^[-–—_\s]+", "", raw_title).strip(" _-")
            opt_suffix = "_opt" if is_opt else ""

            new_name = format_new_name(option, group_name, chapter_num, title, opt_suffix)
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