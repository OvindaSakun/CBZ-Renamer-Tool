# CBZ Renamer Tool

A simple, interactive Python script to clean up and standardize downloaded manga and comic `.cbz` filenames. It automatically removes random hashes, strips out messy volume tags, and formats chapter numbers cleanly.

---

## Features

- **Interactive Format Selection:** Choose between 4 clean naming layouts:
  1. Only Chapter Number (`Chapter 10.cbz`)
  2. Number, Title & Scanlation Group (`Chapter 10 - Defense Battle [Group].cbz`)
  3. Number & Title (`Chapter 10 - Defense Battle.cbz`)
  4. Number & Scanlation Group (`Chapter 10 [Group].cbz`)
- **Zero-Padding Standardization:** Detects padded files (`Chapter 0001.cbz`) and lets you choose to either pad all chapters to match or strip all leading zeros.
- **Hash Removal:** Automatically strips trailing hex hashes (e.g. `_a7acd2`).
- **Optimization Tag Safe:** Preserves `_opt` suffixes created by image compression tools.
- **Dry-Run Preview:** Includes a test script to inspect every rename action before applying it.
- **Conflict Safe:** Skips renaming if a destination file already exists.

---

## Basic Usage

1. Place both scripts (`rename_cbz_test.py` and `rename_cbz_real.py`) in a single folder (e.g., `C:\Tools\`).
2. Open your Command Prompt (`cmd`) in the folder that contains your downloaded `.cbz` files.
3. Run the test script first to safely preview the new names:
   ```bash
   python \Your-Directory\rename_cbz_test.py
   ```
4. If the preview looks correct, run the real script to execute the changes:
   ```bash
   python \Your-Directory\rename_cbz_real.py
   ```
