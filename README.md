# os2display Folder Sync
This module looks at content in a folder and uploads new files to an OS2display slide.

## Setup

Install the module locally by setting up a virtual environment and installing packages with pip.
### Win
```
python -m venv .venv
.venv/Scripts/activate
pip install -e .
```
### bash
```
python -m venv .venv
.venv/bin/activate
pip install -e .
```
Create a local .env file to run the module without parameters.
```
USERNAME="username@os2display"
PASSWORD="s3cr3t_p455w0rd"
IMG_PATH="/path/to/folder/with/images"
SLIDE="Slide_ID_From_OS2Display_Like_01K38G82ZAQ1T8Q5RGEA473SBK"
BASE_URL="https://os2display.domain.dk/v2"
```
Run the module without parameters, if using a .env, or with parameters if not:
```
python -m os2display_folder_sync
python -m os2display_folder_sync -u "username@os2display" -p "s3cr3t_p455w0rd" -f "/path/to/folder/with/images" -s "Slide_ID_From_OS2Display_Like_01K38G82ZAQ1T8Q5RGEA473SBK" -w "https://os2display.domain.dk/v2"
```

## Usage
The module will check for any files in the designated folder and check for image files added.

Any new images will be uploaded to OS2display and moved to a processed_images folder.