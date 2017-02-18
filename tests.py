import _
import unittest


class TestAssignment(unittest.TestCase):
    def test_integer(self):
        compiled = _.compile_underscore('value=-13;')
        memory = compiled.run()
        self.assertEqual(memory['value'], -13)
        compiled = _.compile_underscore('value=42;')
        memory = compiled.run()
        self.assertEqual(memory['value'], 42)

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

    def test_string_double_quotes(self):
        compiled = _.compile_underscore('      value="sdfasdfasd";')
        memory = compiled.run()
        self.assertEqual(memory['value'], 'sdfasdfasd')

    def test_string_single_quotes(self):
        compiled = _.compile_underscore("value='smv lddfl sdf lfdg'     ;")
        memory = compiled.run()
        self.assertEqual(memory['value'], 'smv lddfl sdf lfdg')

    def test_string_triple_double_quotes(self):
        compiled = _.compile_underscore(
            'value="""ascv lclv ff4''6557646.n5  dj""";'
        )
        memory = compiled.run()
        self.assertEqual(memory['value'], 'ascv lclv ff46557646.n5  dj')

    def test_string_triple_single_quotes(self):
        compiled = _.compile_underscore(
            """value='''`````dsfs lkf "" ''fgdsakl hd`````''';"""
        )
        memory = compiled.run()
        self.assertEqual(
            memory['value'], '''`````dsfs lkf "" ''fgdsakl hd`````'''
        )

    def test_reference(self):
        compiled = _.compile_underscore(
            '''
            first_variable=5;second_variable=first_variable;
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['second_variable'], 5)

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


unittest.main()
