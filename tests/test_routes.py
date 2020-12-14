import unittest

from fastapi import HTTPException
from fastapi.testclient import TestClient

import sys
sys.path.append(sys.path[0] + '/..')

import os, random, string

from api.routes import router, MAX_CHARACTERS

class TestRoutes(unittest.TestCase):
    client = None

    def setUp(self):
        self.client = TestClient(router)

    def tearDown(self):
        del self.client

    def test_home(self):
        response = self.client.get('/')
        assert response.status_code == 200

    def test_text_to_tacotron_audio_file(self):
        text = ''.join(random.choice(string.ascii_lowercase) for i in range(50))

        try:
            response = self.client.post(
                '/taco',
                json={
                    'text': text
                }
            )
            assert response.status_code == 200
        except HTTPException as e:
            pass

    def test_text_to_tacotron_audio_file_too_many_characters(self):
        text_with_too_many_characters = ''.join(random.choice(string.ascii_lowercase) for i in range(MAX_CHARACTERS + 1))

        try:
            response = self.client.post(
                '/taco',
                json={
                    'text': text_with_too_many_characters
                }
            )
            assert response.status_code == 500
        except HTTPException as e:
            pass

    def test_audio_to_tacotron_audio_file(self):
        try:
            basePath = './tests/data/'
            fileName = 'dit_is_een_test.wav'
            sound = open(basePath + fileName, 'rb')

            response = self.client.post(
                '/taco_audio',
                files={
                    "file": (
                        "filename", sound, "multipart/form-data"
                    )
                }
            )
            assert response.status_code == 200
        except HTTPException as e:
            pass

    def test_audio_to_tacotron_audio_file_too_many_bytes(self):
        try:
            basePath = './tests/data/'
            fileName = 'song.wav'
            sound = open(basePath + fileName, 'rb')

            response = self.client.post(
                '/taco_audio',
                files={
                    "file": (
                        "filename", sound, "multipart/form-data"
                    )
                }
            )
            assert response.status_code == 500
        except HTTPException as e:
            pass

    def test_get_models(self):
        try:
            response = self.client.get('/get_models')
            assert response.status_code == 200
        except HTTPException as e:
            pass

if __name__ == '__main__':
    unittest.main()
    