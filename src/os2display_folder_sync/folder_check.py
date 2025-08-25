import time

from watchdog.events import FileCreatedEvent, FileSystemEventHandler
from watchdog.observers import Observer


class FolderCheck(FileSystemEventHandler):
    """Check for changes in a folder given.

    Args:
        FileSystemEventHandler: Event to handle file system changes.
    """
    ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.jfif', '.png', '.webp', '.bmp', '.tiff')

    def __init__(self, callback=None):
        super().__init__()
        self.callback = callback

    def on_created(self, event: FileCreatedEvent):
        """Called when a file is created or changed."""
        if not event.is_directory and event.src_path.lower().endswith(self.ALLOWED_EXTENSIONS):
            print(f"New file: {event.src_path}, adding to OS2display")
            if self.callback:
                self.callback(event.src_path)


def watch_folder(path, callback=None):
    """Call this to start watching the folder path.

    Args:
        path: Path of folder to watch.
        callback: Callback to run when something changes. Defaults to None.
    """
    observer = Observer()
    observer.schedule(FolderCheck(callback), path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:  # This makes sure the program ends gracefully.
        observer.stop()
    observer.join()


if __name__ == "__main__":
    watch_folder(".")
