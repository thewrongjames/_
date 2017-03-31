import _
import unittest

class TestNames(unittest.TestCase):
    def test_reserved_words(self):
        with self.assertRaises(_.exceptions.UnderscoreCouldNotConsumeError):
            _.compile_underscore('return = 7;')

    def test_name_error(self):
        with self.assertRaises(_.exceptions.UnderscoreNameError):
            compiled = _.compile_underscore('this=that;')
            compiled.run()
