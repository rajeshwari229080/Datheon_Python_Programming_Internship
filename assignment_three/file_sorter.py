"""Automated File Organizer - CodeCraft Python Studio

Organizes unorganized target directories by sorting files into standardized categories.
Features dry-run simulation, non-destructive collision renaming, root folder protection,
and operation logging using pathlib and shutil.
"""

from __future__ import annotations
import argparse
import logging
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

# Supported 9 categories per specification
CATEGORY_MAPPING: Dict[str, Set[str]] = {
    "Documents": {".pdf", ".docx", ".doc", ".txt", ".rtf", ".odt", ".md"},
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff"},
    "Videos": {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"},
    "Audio": {".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"},
    "Archives": {".zip", ".tar", ".gz", ".7z", ".rar", ".bz2"},
    "Source Code": {".py", ".js", ".ts", ".html", ".css", ".java", ".cpp", ".c", ".rs", ".go", ".json", ".xml", ".sql"},
    "Spreadsheets": {".xlsx", ".xls", ".csv", ".tsv", ".ods"},
    "Presentations": {".pptx", ".ppt", ".key", ".odp"},
    "Other": set()  # Fallback category
}

DEFAULT_CATEGORY_NAMES: Set[str] = set(CATEGORY_MAPPING.keys())


class FileOrganizer:
    """Manages file classification, safety verifications, collision mitigation, and directory sorting."""

    def __init__(self, target_dir: Path, dry_run: bool = False, log_file: Optional[Path] = None) -> None:
        self.raw_target = Path(target_dir)
        self.resolved_target = self.raw_target.resolve()
        self.dry_run = dry_run
        self.log_file = log_file

        self.successful_moves: List[Tuple[Path, Path]] = []
        self.skipped_files: List[Tuple[Path, str]] = []
        self.failures: List[Tuple[Path, str]] = []

        self._setup_logger()

    def _setup_logger(self) -> None:
        self.logger = logging.getLogger(f"FileOrganizer_{id(self)}")
        self.logger.setLevel(logging.INFO)
        self.logger.handlers.clear()

        # Console handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        self.logger.addHandler(ch)

        # File handler if requested
        if self.log_file:
            self.log_file.parent.mkdir(parents=True, exist_ok=True)
            fh = logging.FileHandler(self.log_file, encoding="utf-8")
            fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
            self.logger.addHandler(fh)

    def validate_target_safety(self) -> Tuple[bool, str]:
        """Prevents operating on root drives, system directories, or non-existent paths."""
        if not self.resolved_target.exists():
            return False, f"Target directory does not exist: {self.resolved_target}"
        if not self.resolved_target.is_dir():
            return False, f"Target path is a file, not a directory: {self.resolved_target}"

        # Check for system root directories (e.g. C:\, \, /)
        root_parts = {self.resolved_target.anchor, str(self.resolved_target)}
        if str(self.resolved_target).rstrip("\\/") in ("C:", "D:", "E:", "/", "\\"):
            return False, f"Safety restriction: Refusing to organize root filesystem '{self.resolved_target}'."

        if self.resolved_target.parent == self.resolved_target:
            return False, f"Safety restriction: Target is the root anchor '{self.resolved_target}'."

        # Avoid Windows system directories
        windir = os.environ.get("WINDIR", "C:\\Windows")
        if str(self.resolved_target).lower().startswith(windir.lower()):
            return False, f"Safety restriction: Refusing to organize Windows system folder '{self.resolved_target}'."

        return True, "Target directory validated successfully."

    @staticmethod
    def determine_category(file_path: Path) -> str:
        """Determines target category based on file extension."""
        ext = file_path.suffix.lower()
        for category, extensions in CATEGORY_MAPPING.items():
            if ext in extensions:
                return category
        return "Other"

    @staticmethod
    def resolve_collision_path(destination_dir: Path, original_filename: str) -> Path:
        """Generates a collision-free filename like name_1.ext, name_2.ext without overwriting."""
        dest_file = destination_dir / original_filename
        if not dest_file.exists():
            return dest_file

        stem = dest_file.stem
        suffix = dest_file.suffix
        counter = 1
        while True:
            candidate = destination_dir / f"{stem}_{counter}{suffix}"
            if not candidate.exists():
                return candidate
            counter += 1

    def scan_files(self) -> List[Path]:
        """Collects top-level candidate files, ignoring category subfolders and symlinks."""
        candidates: List[Path] = []
        try:
            with os.scandir(self.resolved_target) as entries:
                for entry in entries:
                    entry_path = Path(entry.path)
                    # Skip symlinks and directories
                    if entry.is_symlink() or entry.is_dir():
                        continue
                    # Skip special hidden files like .gitkeep or .DS_Store if configured
                    if entry.name.startswith("."):
                        self.skipped_files.append((entry_path, "Hidden or dot-file"))
                        continue
                    candidates.append(entry_path)
        except Exception as e:
            self.logger.error(f"Failed scanning directory {self.resolved_target}: {e}")
        return candidates

    def organize(self) -> Dict[str, Any]:
        """Executes the file organization or dry-run preview."""
        is_safe, msg = self.validate_target_safety()
        if not is_safe:
            self.logger.error(msg)
            return {"status": "error", "message": msg}

        self.logger.info(f"Target directory resolved: {self.resolved_target}")
        self.logger.info(f"Mode: {'DRY RUN (Preview Only - No Files Changed)' if self.dry_run else 'ACTIVE MOVE'}")

        candidates = self.scan_files()
        self.logger.info(f"Discovered {len(candidates)} file(s) eligible for classification.")

        for file_path in candidates:
            category = self.determine_category(file_path)
            category_dir = self.resolved_target / category
            dest_path = self.resolve_collision_path(category_dir, file_path.name)

            if self.dry_run:
                self.successful_moves.append((file_path, dest_path))
                self.logger.info(f"[DRY-RUN] Would move: '{file_path.name}' -> '{category}/{dest_path.name}'")
            else:
                try:
                    category_dir.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(file_path), str(dest_path))
                    self.successful_moves.append((file_path, dest_path))
                    self.logger.info(f"[MOVED] '{file_path.name}' -> '{category}/{dest_path.name}'")
                except Exception as e:
                    self.failures.append((file_path, str(e)))
                    self.logger.error(f"[FAILED] Could not move '{file_path.name}': {e}")

        summary = {
            "target": str(self.resolved_target),
            "dry_run": self.dry_run,
            "moved_count": len(self.successful_moves),
            "skipped_count": len(self.skipped_files),
            "failure_count": len(self.failures),
        }
        self.logger.info(
            f"Operation complete. Moved: {summary['moved_count']}, "
            f"Skipped: {summary['skipped_count']}, Failures: {summary['failure_count']}."
        )
        return summary


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CodeCraft Automated File Organizer - Sort files into 9 structured categories safely."
    )
    parser.add_argument(
        "--target",
        "-t",
        required=True,
        help="Path to the directory containing files to organize."
    )
    parser.add_argument(
        "--dry-run",
        "-d",
        action="store_true",
        help="Simulate the organization process without altering files or creating folders."
    )
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Prompt for user confirmation before executing actual file moves."
    )
    parser.add_argument(
        "--log-file",
        "-l",
        default=None,
        help="Custom destination path for persistent execution logs."
    )
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    default_log = (
        Path(__file__).resolve().parent / "logs" / f"organizer_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.log"
    )
    log_path = Path(args.log_file) if args.log_file else default_log

    organizer = FileOrganizer(target_dir=Path(args.target), dry_run=args.dry_run, log_file=log_path)

    # Validate target first
    is_safe, msg = organizer.validate_target_safety()
    if not is_safe:
        print(f"\n[Error] {msg}\n")
        sys.exit(1)

    if args.interactive and not args.dry_run:
        confirm = input(f"Confirm moving files inside '{organizer.resolved_target}'? (y/n): ").strip().lower()
        if confirm not in ("y", "yes"):
            print("Operation aborted by user.")
            sys.exit(0)

    organizer.organize()


if __name__ == "__main__":
    main()
