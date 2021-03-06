import _
import unittest

class TestAssignment(unittest.TestCase):
    def test_integer(self):
        compiled = _.compile_('value=-13;')
        memory = compiled.run()
        self.assertEqual(memory['value'], -13)
        compiled = _.compile_('value=42;')
        memory = compiled.run()
        self.assertEqual(memory['value'], 42)

    def test_float(self):
        compiled = _.compile_('value=   234.234567;')
        memory = compiled.run()
        self.assertEqual(memory['value'], 234.234567)

    def test_boolean(self):
        compiled_true = _.compile_('value = true;')
        compiled_false = _.compile_('value     =false;')
        memory_true = compiled_true.run()
        memory_false = compiled_false.run()
        self.assertEqual(memory_true['value'], True)
        self.assertEqual(memory_false['value'], False)

    def test_string_double_quotes(self):
        compiled = _.compile_('      value="sdfasdfasd";')
        memory = compiled.run()
        self.assertEqual(memory['value'], 'sdfasdfasd')

    def test_string_single_quotes(self):
        compiled = _.compile_("value='smv lddfl sdf lfdg'     ;")
        memory = compiled.run()
        self.assertEqual(memory['value'], 'smv lddfl sdf lfdg')

    def test_string_triple_double_quotes(self):
        compiled = _.compile_(
            'value="""ascv lclv ff4''6557646.n5  dj""";'
        )
        memory = compiled.run()
        self.assertEqual(memory['value'], 'ascv lclv ff46557646.n5  dj')

    def test_string_triple_single_quotes(self):
        compiled = _.compile_(
            """value='''`````dsfs lkf "" ''fgdsakl hd`````''';"""
        )
        memory = compiled.run()
        self.assertEqual(
            memory['value'], '''`````dsfs lkf "" ''fgdsakl hd`````'''
        )

    def test_reference(self):
        compiled = _.compile_(
            '''
            first_variable=5;second_variable=first_variable;
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['second_variable'], 5)

    def test_container(self):
        with self.assertRaises(_.exceptions.UnderscoreSyntaxError):
            _.compile_('container=7;')

    def test_none(self):
        compiled = _.compile_('value=none;')
        memory = compiled.run()
        self.assertTrue(memory['value'] is None)
