# 📁 File Organizer

A simple, beginner-friendly Python command-line tool that automatically
organises files in any folder by sorting them into sub-folders based on
their file type.

---

## 📋 Project Description

Have you ever opened a folder and found hundreds of files of all types
jumbled together — photos, PDFs, videos, ZIP archives, code files — and
wished you could sort them instantly?

**File Organizer** does exactly that.  You give it a folder path, and it
automatically moves every file into a neatly named sub-folder
(`Images`, `Documents`, `Videos`, etc.).  Files with the same name are
renamed automatically so nothing is ever overwritten.

---

## ✨ Features

- ✅ Validates the folder path before doing anything
- ✅ Organises files into **8 categories** (Images, Documents, Videos, Music, Archives, Python Files, Code Files, Others)
- ✅ Creates destination sub-folders automatically
- ✅ Handles **duplicate file names** by renaming (`file(1).pdf`, `file(2).pdf`, …)
- ✅ Skips sub-folders — only processes files
- ✅ Displays a **summary** (total / moved / skipped / errors)
- ✅ Handles common errors gracefully (permission denied, file not found, etc.)
- ✅ Works on **Windows, macOS, and Linux**
- ✅ Uses **only Python standard libraries** — nothing to install

Requirements
# This project uses ONLY Python standard libraries.
# No external packages need to be installed.

Standard libraries used:
# - os     : Built-in. Used for path validation, listing files, and folder creation.
# - shutil : Built-in. Used for moving files between directories.

# To run this project, you only need Python 3.6 or higher installed.
# No `pip install` is required.
