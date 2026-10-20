# Assignment 03: Automated File Organizer

Part of **CodeCraft Python Studio** — Third Independent Python Internship Submission.

---

## Overview
A resilient command-line filesystem utility engineered to scan unstructured folders and sort files into 9 standardized functional directories. Employs `pathlib` and `shutil` for cross-platform reliability, provides non-destructive collision renaming, guards against operating on root or system folders, and outputs structured execution logs.

---

## The 9 Classification Categories

| Category | File Extensions Handled |
| :--- | :--- |
| **Documents** | `.pdf`, `.docx`, `.doc`, `.txt`, `.rtf`, `.odt`, `.md` |
| **Images** | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.svg`, `.webp`, `.tiff` |
| **Videos** | `.mp4`, `.mkv`, `.avi`, `.mov`, `.wmv`, `.flv`, `.webm` |
| **Audio** | `.mp3`, `.wav`, `.aac`, `.flac`, `.ogg`, `.m4a` |
| **Archives** | `.zip`, `.tar`, `.gz`, `.7z`, `.rar`, `.bz2` |
| **Source Code** | `.py`, `.js`, `.ts`, `.html`, `.css`, `.java`, `.cpp`, `.c`, `.rs`, `.go`, `.json`, `.xml`, `.sql` |
| **Spreadsheets** | `.xlsx`, `.xls`, `.csv`, `.tsv`, `.ods` |
| **Presentations** | `.pptx`, `.ppt`, `.key`, `.odp` |
| **Other** | All unmapped or unrecognized file types (safely segregated) |

---

## Safety Controls & Safeguards
- **Root Directory Guard**: Blocks execution if the target path is a drive root (`C:\`, `/`) or Windows system folder (`C:\Windows`).
- **Dry-Run Preview**: The `--dry-run` flag performs full category analysis and logs planned actions without moving files or creating folders.
- **Collision Protection**: If a file of the same name already exists in the destination folder, the incoming file is automatically renamed to `filename_1.ext`, `filename_2.ext` rather than overwriting.
- **Loop Prevention**: Automatically ignores already-created category subfolders, symlinks, and hidden dotfiles.

---

## Execution Guide

### Dry-Run Preview (Recommended First)
```bash
python assignment_three/file_sorter.py --target "path/to/my_folder" --dry-run
```

### Live Organization with Confirmation
```bash
python assignment_three/file_sorter.py --target "path/to/my_folder" --interactive
```

### Running Unit Tests
```bash
python -m unittest discover -s assignment_three/tests -v
```
