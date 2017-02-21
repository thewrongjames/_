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
        _.compile_underscore('this.that.this.that.this.that;')


class TestTemplates(unittest.TestCase):
    def test_basics(self):
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

    def test_python_callable(self):
        compiled = _.compile_underscore(
            '''
            instance = template(){return('bar';);};
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['instance'](), 'bar')

    def test_modifying_external_values(self):
        compiled = _.compile_underscore(
            '''
            external_value = false;
            instance = template(){
                internal_value = container.external_value;
            }();
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['instance']['internal_value'], False)

    def test_nested_template_access(self):
        compiled = _.compile_underscore(
            '''
            template_1 = template(){
                value = 7;
                template_2 = template(){
                    container.value = 'bar';
                };
            };
            instance = template_1();
            first_value = instance.value;
            instance.template_2();
            second_value = instance.value;
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['first_value'], 7)
        self.assertEqual(memory['second_value'], 'bar')

    def test_method_like_behaviour(self):
        pass

    def test_container_updates(self):
        compiled = _.compile_underscore(
            '''
            external_value = -15.4;
            template_ = template(){
                internal_value = external_value;
            };
            first_value = template_().internal_value;
            external_value = true;
            second_value = template_().internal_value;
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['first_value'], -15.4)
        self.assertEqual(memory['second_value'], True)


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
