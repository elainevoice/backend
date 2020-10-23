import unittest
import os

import sys
sys.path.append(sys.path[0] + '/..')

from api.helpers import find_last_modified_recording, find_last_modified_result

class TestHelpers(unittest.TestCase):
    def test_find_last_modified_recording(self):
        path = r'./assets/data/recordings/'
        last_modified_recording = find_last_modified_recording()

        test_last_modified = { 'file': None, 'last_modified': None}
        for file in os.listdir(path):
            if file.endswith('.wav'):
                full_path = os.path.join(path, file)
                last_modified = os.path.getmtime(full_path)

                if test_last_modified['file'] is None or last_modified > test_last_modified['last_modified']:
                    test_last_modified = {
                        'file': full_path,
                        'last_modified': last_modified
                    }

        self.assertEqual(test_last_modified['file'], last_modified_recording)

    def test_find_last_modified_result(self):
        path = r'./assets/data/results/'
        last_modified_result = find_last_modified_result()

        test_last_modified = { 'file': None, 'last_modified': None}
        for file in os.listdir(path):
            if file.endswith('.wav'):
                full_path = os.path.join(path, file)
                last_modified = os.path.getmtime(full_path)

                if test_last_modified['file'] is None or last_modified > test_last_modified['last_modified']:
                    test_last_modified = {
                        'file': full_path,
                        'last_modified': last_modified
                    }

        self.assertEqual(test_last_modified['file'], last_modified_result)

if __name__ == '__main__':
    unittest.main()