import unittest
from fastapi.testclient import TestClient

import sys
sys.path.append(sys.path[0] + "/..")

from api.routes import router

class TestRoutes(unittest.TestCase):
    client = None

    def setUp(self):
        self.client = TestClient(router)

    def tearDown(self):
        pass

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200

    # def test_post_recording_disk(self):
    #     response = self.client.post("/recognize_audio_disk")
    #     assert response.status_code == 200

    # def test_post_bad_recording_disk(self):
    #     response = self.client.post("/recognize_audio_disk")
    #     assert response.status_code == 500

    # def test_post_recording_memory(self):
    #     response = self.client.post("/recognize_audio_memory")
    #     assert response.status_code == 200

    # def test_post_bad_recording_memory(self):
    #     response = self.client.post("/recognize_audio_memory")
    #     assert response.status_code == 500

    # def test_create_audio_from_text(self):
    #     response = self.client.post("/create_audio")
    #     assert response.status_code == 200

    # def test_create_audio_from_bad_text(self):
    #     response = self.client.post("/create_audio")
    #     assert response.status_code == 500

    # def test_crack_create_audio_from_text(self):
    #     response = self.client.post("/crack_create_audio")
    #     assert response.status_code == 200

    # def test_crack_create_audio_from_bad_text(self):
    #     response = self.client.post("/crack_create_audio")
    #     assert response.status_code == 500

    # def test_crack_audio_oplossing(self):
    #     response = self.client.get("/crack_audio_oplossing")
    #     assert response.status_code == 200

if __name__ == '__main__':
    unittest.main()