import _
import unittest


class TestSyntaxErrors(unittest.TestCase):
    def test_closing_strings(self):
        with self.assertRaises(_.exceptions.UnderscoreSyntaxError):
            _.compile_('"')
        with self.assertRaises(_.exceptions.UnderscoreSyntaxError):
            _.compile_("'")
        with self.assertRaises(_.exceptions.UnderscoreSyntaxError):
            _.compile_('"""')
        with self.assertRaises(_.exceptions.UnderscoreSyntaxError):
            _.compile_("'''")

    def test_float(self):
        with self.assertRaises(_.exceptions.UnderscoreSyntaxError):
            _.compile_('3.')
