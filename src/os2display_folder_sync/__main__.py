import argparse
import sys
import dotenv
import os
from pathlib import Path

from os2display_folder_sync.folder_check import watch_folder
from os2display_folder_sync.process_file import ProcessFile

dotenv.load_dotenv()


def main():
    """Main entry for program."""
    parser = argparse.ArgumentParser(description="Watch folder and upload PNG files to OS2display. By default using .env file for credentials, path and api-url, may be overwritten with arguments.")

    parser.add_argument("-f", "--folder", help="Path to folder to watch for PNG files", default=os.getenv('IMG_PATH'))
    parser.add_argument("-u", "--username", help="API username", default=os.getenv('USERNAME'))
    parser.add_argument("-p", "--password", help="API password", default=os.getenv('PASSWORD'))
    parser.add_argument("-s", "--slide", help="Display slide", default=os.getenv('SLIDE'))
    parser.add_argument("--api-url", help="API base URL", default=os.getenv('BASE_URL'))

    args = parser.parse_args()
    # Validate path
    watch_path = Path(args.folder)
    if not watch_path.exists():
        print(f"Error: Path {watch_path} does not exist")
        sys.exit(1)

    process_file = ProcessFile(args.username, args.password, args.slide, args.api_url)
    process_file.process_all(watch_path)
    watch_folder(watch_path, process_file.process_image_file)


if __name__ == "__main__":
    main()
