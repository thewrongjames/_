import _
import unittest

class FileTests(unittest.TestCase):
    def test_list(self):
        compiled = _.compile_file('tests/file_tests/list._')
        memory = compiled.run()
        self.assertEqual(memory['value_one'], 'this')
        self.assertEqual(memory['value_two'], -7.2)
