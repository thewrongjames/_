import _
import unittest

class TestReferences(unittest.TestCase):
    def test_properties_compile(self):
        _.compile_underscore('this.that.this.that.this.that;')
