import _
import unittest


class TestSyntaxErrors(unittest.TestCase):
    def test_closing_strings(self):
        with self.assertRaises(_.exceptions.UnderscoreSyntaxError):
            _.compile_underscore('"')
        with self.assertRaises(_.exceptions.UnderscoreSyntaxError):
            _.compile_underscore("'")
        with self.assertRaises(_.exceptions.UnderscoreSyntaxError):
            _.compile_underscore('"""')
        with self.assertRaises(_.exceptions.UnderscoreSyntaxError):
            _.compile_underscore("'''")

    def test_float(self):
        with self.assertRaises(_.exceptions.UnderscoreSyntaxError):
            _.compile_underscore('3.')
