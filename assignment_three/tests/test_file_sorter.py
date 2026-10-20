"""Unit tests for Automated File Organizer (Assignment Three)."""

import tempfile
import unittest
from pathlib import Path
from assignment_three.file_sorter import FileOrganizer, CATEGORY_MAPPING


class TestFileOrganizer(unittest.TestCase):
    """Tests file classification, dry-run safety, collisions, and security restrictions."""

    def test_extension_categorization(self):
        cases = [
            (Path("report.pdf"), "Documents"),
            (Path("notes.txt"), "Documents"),
            (Path("vacation.JPG"), "Images"),
            (Path("icon.svg"), "Images"),
            (Path("clip.mp4"), "Videos"),
            (Path("podcast.mp3"), "Audio"),
            (Path("bundle.tar.gz"), "Archives"),
            (Path("backup.zip"), "Archives"),
            (Path("script.py"), "Source Code"),
            (Path("style.css"), "Source Code"),
            (Path("ledger.xlsx"), "Spreadsheets"),
            (Path("data.csv"), "Spreadsheets"),
            (Path("deck.pptx"), "Presentations"),
            (Path("mystery.xyz123"), "Other"),
        ]
        for path_obj, expected_cat in cases:
            self.assertEqual(FileOrganizer.determine_category(path_obj), expected_cat)

    def test_dry_run_leaves_disk_untouched(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir)
            doc_file = target / "test_doc.docx"
            img_file = target / "test_img.png"
            doc_file.write_text("Hello doc", encoding="utf-8")
            img_file.write_text("fake image", encoding="utf-8")

            organizer = FileOrganizer(target, dry_run=True)
            summary = organizer.organize()

            self.assertTrue(summary["dry_run"])
            self.assertEqual(summary["moved_count"], 2)

            # Files MUST remain in their original location during dry-run
            self.assertTrue(doc_file.exists())
            self.assertTrue(img_file.exists())
            # Category subfolders must NOT be created
            self.assertFalse((target / "Documents").exists())
            self.assertFalse((target / "Images").exists())

    def test_active_organization(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir)
            doc_file = target / "resume.pdf"
            code_file = target / "app.py"
            doc_file.write_text("Resume Content", encoding="utf-8")
            code_file.write_text("print('hello')", encoding="utf-8")

            organizer = FileOrganizer(target, dry_run=False)
            summary = organizer.organize()

            self.assertEqual(summary["moved_count"], 2)
            self.assertEqual(summary["failure_count"], 0)

            # Files moved into category folders
            self.assertTrue((target / "Documents" / "resume.pdf").exists())
            self.assertTrue((target / "Source Code" / "app.py").exists())
            self.assertFalse(doc_file.exists())
            self.assertFalse(code_file.exists())

    def test_collision_renaming(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir)
            cat_dir = target / "Documents"
            cat_dir.mkdir()

            # Existing file in destination
            existing = cat_dir / "report.pdf"
            existing.write_text("Existing file", encoding="utf-8")

            # Source file in target root with the same name
            incoming = target / "report.pdf"
            incoming.write_text("New incoming file", encoding="utf-8")

            organizer = FileOrganizer(target, dry_run=False)
            summary = organizer.organize()

            self.assertEqual(summary["moved_count"], 1)
            # Original remains untouched
            self.assertEqual(existing.read_text(encoding="utf-8"), "Existing file")
            # Colliding file safely renamed to report_1.pdf
            renamed = cat_dir / "report_1.pdf"
            self.assertTrue(renamed.exists())
            self.assertEqual(renamed.read_text(encoding="utf-8"), "New incoming file")

    def test_safety_rejects_root_and_nonexistent(self):
        # Non-existent
        fake = Path("C:/non_existent_folder_xyz_123")
        org_fake = FileOrganizer(fake)
        safe, msg = org_fake.validate_target_safety()
        self.assertFalse(safe)
        self.assertIn("does not exist", msg)

        # Drive Root
        root_c = Path("C:/")
        org_root = FileOrganizer(root_c)
        safe_root, msg_root = org_root.validate_target_safety()
        self.assertFalse(safe_root)
        self.assertIn("Safety restriction", msg_root)


if __name__ == "__main__":
    unittest.main()
