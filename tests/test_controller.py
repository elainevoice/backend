import unittest

import sys
sys.path.append(sys.path[0] + '/..')

class TestControllers(unittest.TestCase):
    def test_text_to_tacotron_audio_file(self):
        # Not sure how we can test this
        pass 
        
    def test_get_models(self):
        models = get_taco_models()
        assert len(models) > 0
        
    def test_audio_to_tacotron_audio_file(self):
        # Not sure how we can test this
        pass

if __name__ == '__main__':
    unittest.main()
