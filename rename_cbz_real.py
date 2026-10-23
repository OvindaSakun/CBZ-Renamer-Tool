import re
from pathlib import Path

# STRICTLY REAL RUN - WILL RENAME FILES
DRY_RUN = False
DIRECTORY = "." 

def get_user_choice():
    print("\n--- Renaming Options ---")
    print("1. Only Chapter Number (e.g., Chapter 10.cbz)")
    print("2. Keep All 3          (e.g., Chapter 10 - Defense Battle [Tenuous Scans].cbz)")
    print("3. Keep Num & Title    (e.g., Chapter 10 - Defense Battle.cbz)")
    print("4. Keep Num & Group    (e.g., Chapter 10 [Tenuous Scans].cbz)")
    
    while True:
        choice = input("\nEnter choice (1-4): ").strip()
        if choice in ('1', '2', '3', '4'):
            return int(choice)
        print("Invalid choice. Please enter 1, 2, 3, or 4.")

def format_new_name(option, group_name, chapter_num, title, opt_suffix):
    parts = [f"Chapter {chapter_num}"]
    
    if option in (2, 3) and title:
        parts.append(f"- {title}")
        
    if option in (2, 4) and group_name:
        parts.append(f"[{group_name}]")
        
    base_name = " ".join(parts)
    return f"{base_name}{opt_suffix}.cbz"

def clean_chapter_names():
    target_dir = Path(DIRECTORY)
    pattern = re.compile(r"(?i)^(.*?)(?:vol[\.\s]*\d+[\s,]*)?(?:chapter|ch\.?)\s*([\d\.]+)(.*?)(?:_[a-fA-F0-9]{6,8})?(_opt)?$")

    option = get_user_choice()

    max_digits = 0
    has_zeros = False
    
    for file_path in target_dir.glob("*.cbz"):
        match = pattern.search(file_path.stem)
        if match:
            int_part = match.group(2).split('.')[0]
            if len(int_part) > max_digits:
                max_digits = len(int_part)
            if re.search(r"^0+\d", int_part):
                has_zeros = True

    pad_zeros = False
    strip_zeros = False
    
    if has_zeros:
        print("\n--- Zero-Padding Detected ---")
        print(f"1. Standardize/Add leading zeros (e.g., Chapter {str(1).zfill(max_digits)}.cbz)")
        print("2. Remove all leading zeros      (e.g., Chapter 1.cbz)")
        while True:
            z_choice = input("Enter choice (1-2): ").strip()
            if z_choice == '1':
                pad_zeros = True
                break
            elif z_choice == '2':
                strip_zeros = True
                break
            print("Invalid choice. Please enter 1 or 2.")

    print(f"\n⚠️ EXECUTING REAL RENAME for Option {option}...\n")

    for file_path in target_dir.glob("*.cbz"):
        match = pattern.search(file_path.stem)
        if match:
            raw_group = match.group(1) or ""
            chapter_num = match.group(2)
            raw_title = match.group(3) or ""
            is_opt = match.group(4)
            
            if pad_zeros:
                parts = chapter_num.split('.')
                parts[0] = parts[0].zfill(max_digits)
                chapter_num = '.'.join(parts)
            elif strip_zeros:
                chapter_num = chapter_num.lstrip('0')
                if not chapter_num or chapter_num.startswith('.'):
                    chapter_num = '0' + chapter_num

            group_name = re.sub(r"_+(\s*_+)*$", "", raw_group).strip(" _-[]")
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