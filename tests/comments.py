import _
import unittest


class TestComments(unittest.TestCase):
    def test_comments(self):
        compiled = _.compile_(
            '''
            value = 42;
            #
            value = 63;
            #
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value'], 42)

    def test_hash_does_not_break_strings(self):
        compiled = _.compile_(
            '''
            value = 'Here is a hash: #.';
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value'], 'Here is a hash: #.')
