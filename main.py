# -*- coding: utf-8 -*-
"""
============================================================
  File Organizer - Beginner Python Project
  Author  : Python Learner
  Version : 1.0
  Purpose : Automatically organise files in a selected folder
            by moving them into sub-folders based on file type.
============================================================
"""

import os       # For folder / file operations (checking paths, listing files, etc.)
import shutil   # For moving files from one place to another


# ─────────────────────────────────────────────
# CATEGORY MAP
# Maps each category name to a list of extensions
# that belong to it.  Extensions are stored in
# lower-case so comparisons are case-insensitive.
# ─────────────────────────────────────────────
CATEGORY_MAP = {
    "Images":     [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Documents":  [".pdf", ".doc", ".docx", ".txt", ".pptx", ".xlsx"],
    "Videos":     [".mp4", ".mkv", ".avi", ".mov"],
    "Music":      [".mp3", ".wav", ".aac"],
    "Archives":   [".zip", ".rar", ".7z"],
    "Python Files": [".py"],
    "Code Files": [".java", ".cpp", ".c", ".html", ".css", ".js"],
}

# Files whose extension is NOT in any category above
# will be placed here.
DEFAULT_CATEGORY = "Others"


# ──────────────────────────────────────────────────────────────────────────────
# FUNCTION 1 ─ get_folder_path
# ──────────────────────────────────────────────────────────────────────────────
def get_folder_path() -> str:
    """
    Repeatedly prompts the user to enter a folder path until a valid,
    existing folder is provided.

    Returns
    -------
    str
        The absolute path of the validated folder.

    How it works
    ------------
    1. Print a welcome banner.
    2. Ask the user to type a folder path.
    3. Strip any accidental leading/trailing spaces from the input.
    4. Call validate_path() to check whether the path is a real folder.
    5. If valid → return the path.
       If invalid → show an error and loop back to step 2.
    """
    print("=" * 60)
    print("        [FILE ORGANIZER]")
    print("=" * 60)
    print("This tool will sort all files in a folder you choose")
    print("into sub-folders based on their file type.\n")

    while True:                                      # Keep asking until valid
        folder_path = input("Enter the folder path to organise: ").strip()

        if validate_path(folder_path):               # Path is good → break out
            return folder_path
        else:
            print(f"  [ERROR] '{folder_path}' is not a valid folder.  Please try again.\n")


# ──────────────────────────────────────────────────────────────────────────────
# FUNCTION 2 ─ validate_path
# ──────────────────────────────────────────────────────────────────────────────
def validate_path(path: str) -> bool:
    """
    Checks whether a given path points to an existing folder/directory.

    Parameters
    ----------
    path : str
        The file-system path entered by the user.

    Returns
    -------
    bool
        True  → path is a real, existing directory.
        False → path is empty, doesn't exist, or points to a file.

    How it works
    ------------
    • os.path.isdir()  returns True only when the path exists AND is a folder.
    • A path that points to a file (not a folder) will return False.
    • An empty string will also return False.
    """
    if not path:                        # Guard against empty input
        return False
    return os.path.isdir(path)          # True if it is an existing directory


# ──────────────────────────────────────────────────────────────────────────────
# FUNCTION 3 ─ get_file_category
# ──────────────────────────────────────────────────────────────────────────────
def get_file_category(filename: str) -> str:
    """
    Determines which category a file belongs to based on its extension.

    Parameters
    ----------
    filename : str
        The name of the file (e.g. "photo.JPG", "notes.txt").

    Returns
    -------
    str
        The category name (e.g. "Images", "Documents", "Others").

    How it works
    ------------
    1. os.path.splitext() splits the filename into (name, extension).
       Example → ("photo", ".JPG")
    2. Convert the extension to lower-case so ".JPG" matches ".jpg".
    3. Loop through every entry in CATEGORY_MAP.
    4. If the extension is in a category's list → return that category.
    5. If no match is found → return DEFAULT_CATEGORY ("Others").
    """
    _, extension = os.path.splitext(filename)   # Split "photo.JPG" → ".JPG"
    extension = extension.lower()               # Normalise to lower-case

    for category, extensions in CATEGORY_MAP.items():
        if extension in extensions:
            return category                     # Found a matching category

    return DEFAULT_CATEGORY                     # No match → "Others"


# ──────────────────────────────────────────────────────────────────────────────
# FUNCTION 4 ─ create_category_folders
# ──────────────────────────────────────────────────────────────────────────────
def create_category_folders(folder_path: str) -> dict:
    """
    Creates sub-folders for every category inside the target folder
    (only if they don't already exist).

    Parameters
    ----------
    folder_path : str
        The root folder chosen by the user.

    Returns
    -------
    dict
        A dictionary mapping each category name to its full path.
        Example → {"Images": "C:/Downloads/Images", "Documents": "C:/Downloads/Documents", …}

    How it works
    ------------
    1. Collect all category names: keys from CATEGORY_MAP + DEFAULT_CATEGORY.
    2. For each category, build its full path using os.path.join().
    3. os.makedirs(exist_ok=True) creates the folder (and any missing
       parent folders) without raising an error if it already exists.
    4. Store the mapping in a dict and return it.
    """
    # All categories we need folders for
    all_categories = list(CATEGORY_MAP.keys()) + [DEFAULT_CATEGORY]
    category_paths = {}

    for category in all_categories:
        # Build full path, e.g. "C:/Downloads/Images"
        category_folder = os.path.join(folder_path, category)

        # Create the folder; exist_ok=True means no error if it already exists
        os.makedirs(category_folder, exist_ok=True)

        # Remember the path so move_files() can use it later
        category_paths[category] = category_folder

    print(f"\n  [OK] Category folders are ready inside: {folder_path}\n")
    return category_paths


# ──────────────────────────────────────────────────────────────────────────────
# FUNCTION 5 ─ get_unique_destination
# ──────────────────────────────────────────────────────────────────────────────
def get_unique_destination(destination_folder: str, filename: str) -> str:
    """
    Builds a unique file path so that existing files are never overwritten.

    If "report.pdf" already exists in the destination, this function will
    return a path for "report(1).pdf", then "report(2).pdf", and so on.

    Parameters
    ----------
    destination_folder : str
        The folder where the file will be moved.
    filename : str
        The original file name (e.g. "report.pdf").

    Returns
    -------
    str
        A full path that does not yet exist.

    How it works
    ------------
    1. Split the filename into the base name and extension.
       "report.pdf" → base="report", ext=".pdf"
    2. Try the simple path first (destination_folder/report.pdf).
    3. If that path already exists, try report(1).pdf, report(2).pdf, …
    4. Return the first path that does NOT exist.
    """
    base_name, extension = os.path.splitext(filename)
    destination_path = os.path.join(destination_folder, filename)
    counter = 1

    # Keep incrementing counter until we find a free filename
    while os.path.exists(destination_path):
        new_filename = f"{base_name}({counter}){extension}"
        destination_path = os.path.join(destination_folder, new_filename)
        counter += 1

    return destination_path


# ──────────────────────────────────────────────────────────────────────────────
# FUNCTION 6 ─ move_files
# ──────────────────────────────────────────────────────────────────────────────
def move_files(folder_path: str, category_paths: dict) -> dict:
    """
    Scans the target folder, categorises every file, and moves it to the
    correct category sub-folder.

    Parameters
    ----------
    folder_path   : str
        Root folder to organise.
    category_paths : dict
        Mapping of category name → destination folder path
        (returned by create_category_folders).

    Returns
    -------
    dict
        A summary dictionary with counts:
        {
            "total"   : <int>,  # all files found (excluding sub-folders)
            "moved"   : <int>,  # files successfully moved
            "skipped" : <int>,  # files that were skipped
            "errors"  : <int>,  # files that caused an exception
        }

    How it works
    ------------
    1. os.listdir() returns the names of everything inside folder_path.
    2. For each entry we check os.path.isfile() to skip sub-folders.
    3. Skip files that live inside one of our category sub-folders
       (i.e. the script itself being run from the same folder is excluded).
    4. Determine the category with get_file_category().
    5. Build a unique destination path with get_unique_destination().
    6. shutil.move() physically moves the file.
    7. Count successes and failures.
    """
    # Counters that will form our summary
    summary = {
        "total"  : 0,
        "moved"  : 0,
        "skipped": 0,
        "errors" : 0,
    }

    # The names of our category folders (so we can skip files inside them)
    category_folder_names = set(os.path.basename(p) for p in category_paths.values())

    print("-" * 60)
    print("  >> Organising files ...")
    print("-" * 60)

    # List everything inside the selected folder
    for item_name in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item_name)

        # ── Skip if it is a folder (we only process files) ──
        if not os.path.isfile(item_path):
            continue

        # ── Skip files that are category folder names themselves ──
        # (Shouldn't happen, but a safety guard)
        if item_name in category_folder_names:
            summary["skipped"] += 1
            continue

        summary["total"] += 1    # We found a valid file to process

        try:
            # Step 1: Find out where this file should go
            category = get_file_category(item_name)
            dest_folder = category_paths[category]

            # Step 2: Build a unique destination path (handles name conflicts)
            dest_path = get_unique_destination(dest_folder, item_name)

            # Step 3: Move the file
            shutil.move(item_path, dest_path)

            # Step 4: Report and count success
            moved_name = os.path.basename(dest_path)
            print(f"  [MOVED]   {item_name}  ->  {category}/{moved_name}")
            summary["moved"] += 1

        except PermissionError:
            # The file might be open in another program
            print(f"  [SKIP]  SKIPPED  (permission denied): {item_name}")
            summary["skipped"] += 1

        except FileNotFoundError:
            # The file disappeared between listing and moving
            print(f"  [SKIP]  SKIPPED  (file not found): {item_name}")
            summary["skipped"] += 1

        except Exception as error:
            # Catch any other unexpected error
            print(f"  [ERROR] moving '{item_name}': {error}")
            summary["errors"] += 1

    return summary


# ──────────────────────────────────────────────────────────────────────────────
# FUNCTION 7 ─ display_summary
# ──────────────────────────────────────────────────────────────────────────────
def display_summary(summary: dict, folder_path: str) -> None:
    """
    Prints a neatly formatted summary of what the organiser did.

    Parameters
    ----------
    summary     : dict
        The dictionary returned by move_files() with counts.
    folder_path : str
        The root folder that was organised (shown in the output).

    How it works
    ------------
    Simply reads the values from the summary dict and prints them
    in a formatted block.  A success or warning message is shown
    depending on whether any errors occurred.
    """
    print("\n" + "=" * 60)
    print("         ORGANISATION SUMMARY")
    print("=" * 60)
    print(f"  Folder organised : {folder_path}")
    print(f"  Total files found: {summary['total']}")
    print(f"  [OK]  Files moved   : {summary['moved']}")
    print(f"  [!!]  Files skipped : {summary['skipped']}")
    print(f"  [X]   Errors        : {summary['errors']}")
    print("-" * 60)

    # Show a final status message
    if summary["errors"] == 0:
        print("  SUCCESS! All done! Your folder has been organised successfully.")
    else:
        print("  WARNING: Finished with some errors. Check the output above.")

    print("=" * 60)


# ──────────────────────────────────────────────────────────────────────────────
# ENTRY POINT ─ main
# ──────────────────────────────────────────────────────────────────────────────
def main():
    """
    The main driver function.  Calls all other functions in order:

    1. get_folder_path()         → ask user for a valid folder
    2. create_category_folders() → make the destination sub-folders
    3. move_files()              → sort and move every file
    4. display_summary()         → print the result
    """
    try:
        # Step 1 ─ Get a valid folder from the user
        folder_path = get_folder_path()

        # Step 2 ─ Create destination sub-folders
        category_paths = create_category_folders(folder_path)

        # Step 3 ─ Move files to the correct folders
        summary = move_files(folder_path, category_paths)

        # Step 4 ─ Show what was done
        display_summary(summary, folder_path)

    except KeyboardInterrupt:
        # User pressed Ctrl+C
        print("\n\n  Operation cancelled by user.  Goodbye!\n")


# ─────────────────────────────────────────────
# Run main() only when the script is executed
# directly (not when imported as a module).
# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()
