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

    def test_container(self):
        with self.assertRaises(_.exceptions.UnderscoreSyntaxError):
            _.compile_underscore('container=7;')


class TestReference(unittest.TestCase):
    def test_basics(self):
        """
        While this currently cannot possibly execute, it is still going to be
        thought of as syntactically valid. For now at least.
        """
        _.compile_underscore('this.that.this.that.this.that;')


class TestTemplates(unittest.TestCase):
    def test_basics(self):
        _.compile_underscore('template {   };')
        _.compile_underscore('    template ( )   {};')

    def test_internal_values(self):
        compiled = _.compile_underscore('value=template(){value=18;}();')
        memory = compiled.run()
        self.assertEqual(memory['value']['value'], 18)

    def test_return(self):
        compiled = _.compile_underscore('value=template(){return(5;);}();')
        memory = compiled.run()
        self.assertEqual(memory['value'], 5)

    def test_container_access(self):
        compiled = _.compile_underscore(
            '''
            value = -2.5;
            template_ = template () {
                value=container.value;
            };
            instance = template_();
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['instance']['value'], -2.5)

    def test_external_access_to_template(self):
        compiled = _.compile_underscore(
            '''
            instance = template(){value='foo';}();
            value = instance.value;
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value'], 'foo')


class TestNames(unittest.TestCase):
    def test_reserved_words(self):
        with self.assertRaises(_.exceptions.UnderscoreCouldNotConsumeError):
            _.compile_underscore('return = 7;')

    def test_name_error(self):
        with self.assertRaises(_.exceptions.UnderscoreNameError):
            compiled = _.compile_underscore('this=that;')
            compiled.run()


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
