import requests


class OS2DisplayAPI:
    """Functions for the OS2display API.
    """
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.token = None

    def authenticate(self, username, password):
        """Get authentication token."""
        url = f"{self.base_url}/authentication/token"
        params = {"providerId": username, "password": password}
        response = self.session.post(url, json=params)
        response.raise_for_status()

        # Extract token from response
        self.token = response.json().get("token")
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})
        return self.token

    def upload_media(self, file_path, title="", description=""):
        """Upload media file."""
        url = f"{self.base_url}/media"

        with open(file_path, 'rb') as f:
            # binary_data = f.read()
            data = {
                'title': title,
                'description': description,
                'license': "uploaded by script"
            }
            header = {'accept': 'application/ld+json'}
            files = {'file': (f.name, f)}
            response = self.session.post(url, data=data, files=files, headers=header)
            response.raise_for_status()
            return response.json()

    def update_slide(self, slide_id, media_id):
        """Update slide with media."""
        url = f"{self.base_url}/slides/{slide_id}"
        slide = self.session.get(url).json()
        media = slide['media']
        if isinstance(media, list):
            media.append(media_id)
        else:
            media = [media, media_id]
        payload = {'media': media, 'content': {'text': "", 'image': media, 'duration': 5000 * len(media)}}
        headers = {'Content-Type': 'application/ld+json', 'accept': 'application/ld+json'}
        response = self.session.put(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
