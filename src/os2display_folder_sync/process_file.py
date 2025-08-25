"""Constains the class for image processing."""
from os import path
import shutil
from pathlib import Path

from os2display_folder_sync.os2display_api import OS2DisplayAPI


class ProcessFile():
    """Class for processing image files."""
    def __init__(self, username: str, password: str, slide: str):
        self.username = username
        self.password = password
        self.slide = slide

    def process_image_file(self, file_path):
        """Process uploaded image file via API."""
        api = OS2DisplayAPI()
        api.authenticate(self.username, self.password)

        try:
            result = api.upload_media(file_path, title=Path(file_path).name)
            media_id = result.get('@id')
            print(f"Upload successful: {media_id}")
            api.update_slide(self.slide, media_id)

            directory, filename = path.split(file_path)
            shutil.move(file_path, path.join(directory, "processed_images", filename))

        except Exception as e:
            print(f"Error uploading {file_path}: {e}")

    def process_all(self, folder_path):
        """Processes all files in given folder."""
        folder = Path(folder_path)
        for filepath in folder.glob("*"):
            if filepath.suffix.lower() in ['.jpg', '.jpeg', '.jfif', '.png']:
                print(f"Processing {filepath}")
                self.process_image_file(filepath)
