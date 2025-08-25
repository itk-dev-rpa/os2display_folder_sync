import unittest
from unittest.mock import patch, MagicMock

from os2display_folder_sync.folder_check import FolderCheck 


class TestFolderCheck(unittest.TestCase):
    def test_accepts_png_files(self):
        """Test that handler processes PNG files."""
        handler = FolderCheck()

        mock_event = MagicMock()
        mock_event.is_directory = False
        mock_event.src_path = "/test/path/image.png"

        with patch('builtins.print') as mock_print:
            handler.on_created(mock_event)
            mock_print.assert_called_once_with("New file: /test/path/image.png")

    def test_ignores_non_png_files(self):
        """Test that handler ignores non-PNG files."""
        handler = FolderCheck()

        mock_event = MagicMock()
        mock_event.is_directory = False
        mock_event.src_path = "/test/path/document.txt"

        with patch('builtins.print') as mock_print:
            handler.on_created(mock_event)
            mock_print.assert_not_called()
