import unittest

import sys
sys.path.append(sys.path[0] + '/..')

from api.controller import stt_recognize_binary_audio_on_disk, stt_recognize_binary_audio_in_memory, tts_create_audio_from_text

class TestControllers(unittest.TestCase):
    #def test_stt_recognize_binary_audio_on_disk(self):
        #path, text = stt_recognize_binary_audio_on_disk('spooled_temp_file')

    #def test_stt_recognize_binary_audio_in_memory(self):
        #text = stt_recognize_binary_audio_in_memory('spooled_temp_file')

    def test_tts_create_audio_from_text(self):
        path = tts_create_audio_from_text('Test')

if __name__ == '__main__':
    unittest.main()