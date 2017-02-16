import __init__ as _
import unittest


class TestAssignment(unittest.TestCase):
    def test_integer(self):
        compiled = _.compile_underscore('value=-13;')
        memory = compiled.run()
        self.assertEqual(memory['value'], -13)

    def test_float(self):
        compiled = _.compile_underscore('value=   234.234567;')
        memory = compiled.run()
        self.assertEqual(memory['value'], 234.234567)

    def test_boolean(self):
        compiled_true = _.compile_underscore('value = true;')
        compiled_false = _.compile_underscore('value     =false;')
        memory_true = compiled_true.run()
        memory_false = compiled_false.run()
        self.assertEqual(memory_true['value'], True)
        self.assertEqual(memory_false['value'], False)

    def test_string(self):
        compiled = _.compile_underscore('value="sdfasdfasd"')

class TestSyntaxErrors(unittest.TestCase):
    def test_closing_strings(self):
        with self.assertRaises(_.UnderscoreSyntaxError):
            
            

unittest.main()
