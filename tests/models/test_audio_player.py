import unittest

import sys
sys.path.append(sys.path[0] + '/..')

import os, random

from api.models.audio_player import AudioPlayer

class TestAudioPlayer(unittest.TestCase):
    audio_player = None

    def setUp(self):
        self.audio_player = AudioPlayer()

    def tearDown(self):
        del self.audio_player

    def test_play_wav(self):
        basePath = r'./assets/data/sounds_wav/sentences/'
        randomFileName = random.choice(os.listdir(basePath))
        self.audio_player.play_wav(basePath + randomFileName)

if __name__ == '__main__':
    unittest.main()