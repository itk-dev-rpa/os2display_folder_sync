# tests/test_api.py
import unittest
import os
from unittest.mock import patch, mock_open, MagicMock
import tempfile

from os2display_folder_sync.os2display_api import OS2DisplayAPI


class TestOS2DisplayAPI(unittest.TestCase):

    def setUp(self):
        self.api = OS2DisplayAPI()

    # MOCK TESTS (fast)
    @patch('requests.Session.get')
    def test_authenticate_success(self, mock_get):
        """Unit test for authentication."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"access_token": "test_token_123"}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        token = self.api.authenticate("state123", "code456")

        self.assertEqual(token, "test_token_123")
        self.assertEqual(self.api.token, "test_token_123")
        mock_get.assert_called_once()

    @patch('builtins.open', new_callable=mock_open, read_data=b"fake_png_data")
    @patch('requests.Session.post')
    def test_upload_media_success(self, mock_post, mock_file):
        """Unit test for media upload."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"@id": "/api/media/123", "id": "123"}
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        result = self.api.upload_media("test.png", title="Test Image")

        self.assertEqual(result["id"], "123")
        mock_post.assert_called_once()
        mock_file.assert_called_once_with("test.png", 'rb')

    @patch('requests.Session.put')
    def test_update_slide_success(self, mock_put):
        """Unit test for slide update."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "slide_123"}
        mock_response.raise_for_status = MagicMock()
        mock_put.return_value = mock_response

        result = self.api.update_slide("slide_123", "media_456", title="Updated Slide")

        self.assertEqual(result["id"], "slide_123")
        mock_put.assert_called_once()


class TestOS2DisplayAPIIntegration(unittest.TestCase):
    """Integration tests - requires TEST_API_URL environment variable."""

    def setUp(self):
        self.test_api_url = os.getenv("TEST_API_URL")
        self.test_state = os.getenv("TEST_STATE")  
        self.test_code = os.getenv("TEST_CODE")

    @unittest.skipIf(not os.getenv("RUN_INTEGRATION_TESTS"), "Integration tests disabled")
    def test_real_authentication(self):
        """Test authentication against real API."""
        if not all([self.test_api_url, self.test_state, self.test_code]):
            self.skipTest("Missing test API credentials")

        api = OS2DisplayAPI(self.test_api_url)
        token = api.authenticate(self.test_state, self.test_code)

        self.assertIsNotNone(token)
        self.assertTrue(len(token) > 0)

    @unittest.skipIf(not os.getenv("RUN_INTEGRATION_TESTS"), "Integration tests disabled")
    def test_real_media_upload(self):
        """Test media upload against real API."""
        if not self.test_api_url:
            self.skipTest("Missing TEST_API_URL")

        # Create test PNG file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            # Minimal PNG header
            f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde')
            test_file = f.name

        try:
            api = OS2DisplayAPI(self.test_api_url)
            # Authenticate first (you'll need real credentials)
            # api.authenticate(self.test_state, self.test_code)

            result = api.upload_media(test_file, title="Integration Test Image")

            self.assertIn("id", result)
            self.assertIn("@id", result)

        finally:
            os.unlink(test_file)


if __name__ == "__main__":
    unittest.main()
