import unittest
import os

import sys
sys.path.append(sys.path[0] + '/..')

from api.helpers import get_taco_models

class TestHelpers(unittest.TestCase):
    def test_get_taco_models(self):
        models = get_taco_models()
        assert len(models) > 0

if __name__ == '__main__':
    unittest.main()