import __init__ as _
import unittest


class TestMath(unittest.TestCase):
    def test_single_value(self):
        compiled = _.compile_underscore('value=-13;')
        memory = compiled.run()
        self.assertEqual(memory['value'], -13)


unittest.main()
