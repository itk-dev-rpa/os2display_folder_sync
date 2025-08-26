"""Contains the class for image processing."""
from os import path, makedirs
import shutil
from pathlib import Path

from os2display_folder_sync.os2display_api import OS2DisplayAPI


class ProcessFile():
    """Class for processing image files."""
    def __init__(self, username: str, password: str, slide: str, base_url: str):
        self.username = username
        self.password = password
        self.slide = slide
        self.base_url = base_url

    def process_image_file(self, file_path):
        """Process uploaded image file via API."""
        api = OS2DisplayAPI(self.base_url)
        api.authenticate(self.username, self.password)

        try:
            result = api.upload_media(file_path, title=Path(file_path).name)
            media_id = result.get('@id')
            print(f"Upload successful: {media_id}")
            api.update_slide(self.slide, media_id)

            directory, filename = path.split(file_path)
            processed_folder = path.join(directory, "processed_images")
            if not path.exists(processed_folder):
                makedirs(processed_folder)
            shutil.move(file_path, path.join(processed_folder, filename))

        except Exception as e:
            print(f"Error uploading {file_path}: {e}")

    def process_all(self, folder_path):
        """Processes all files in given folder."""
        folder = Path(folder_path)
        for filepath in folder.glob("*"):
            if filepath.suffix.lower() in ['.jpg', '.jpeg', '.jfif', '.png']:
                print(f"Processing {filepath}")
                self.process_image_file(filepath)
