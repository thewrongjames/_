import _
import unittest


class TestTemplates(unittest.TestCase):
    def test_basics(self):
        _.compile_underscore('    template ( )   {};')

    def test_internal_values(self):
        compiled = _.compile_underscore('value=template(){value=18;}();')
        memory = compiled.run()
        self.assertEqual(memory['value']['value'], 18)

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

    def test_modifying_from_external_values(self):
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

    def test_modifying_external_values(self):
        compiled = _.compile_underscore(
            '''
            external_value = -95.3;
            instance = template(){
                container.external_value = 8;
            }();
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['external_value'], 8)

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

    def test_container_updates(self):
        compiled = _.compile_underscore(
            '''
            external_value = -15.4;
            template_ = template(){
                internal_value = container.external_value;
            };
            first_value = template_().internal_value;
            external_value = true;
            second_value = template_().internal_value;
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['first_value'], -15.4)
        self.assertEqual(memory['second_value'], True)
