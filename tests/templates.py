import _
import unittest


class TestTemplates(unittest.TestCase):
    def test_basics(self):
        _.compile_('    template ( )   {};')

    def test_internal_values(self):
        compiled = _.compile_('value=template(){value=18;}();')
        memory = compiled.run()
        self.assertEqual(memory['value']['value'], 18)

    def test_container_access(self):
        compiled = _.compile_(
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
        compiled = _.compile_(
            '''
            instance = template(){value='foo';}();
            value = instance.value;
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value'], 'foo')

    def test_modifying_from_external_values(self):
        compiled = _.compile_(
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
        compiled = _.compile_(
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
        compiled = _.smart_compile_file(
            'tests/file_tests/templates/test_nested_template_access._'
        )
        memory = compiled.run()
        self.assertEqual(memory['first_value'], 7)
        self.assertEqual(memory['second_value'], 'bar')

    def test_container_updates(self):
        compiled = _.compile_(
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

    def test_passing_in(self):
        compiled = _.compile_(
            '''
            template_ = template(thing_one, thing_two) {
                this = thing_one;
            };
            instance_one = template_(1, 2);
            instance_two = template_('false', none);
            value_one = instance_one.this;
            value_two = instance_two.thing_two;
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value_one'], 1)
        self.assertEqual(memory['value_two'], None)

    def test_key_value_assignment(self):
        compiled = _.compile_(
            '''
            instance = template() {
                set('this', 'that');
            }();
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['instance']['this'], 'that')

    def test_key_value_read(self):
        compiled = _.compile_(
            '''
            instance = template() {
                set('this', 'that');
            }();
            value = instance.get('this');
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value'], 'that')

    def test_key_value_delete(self):
        compiled = _.compile_(
            '''
            instance = template() {
                value = 'this';
            }();
            instance.delete('value');
            '''
        )
        memory = compiled.run()
        self.assertNotIn('value', memory['instance'])

    def test_key_value_template(self):
        compiled = _.smart_compile_file(
            'tests/file_tests/templates/test_key_value_template._'
        )
        memory = compiled.run()
        self.assertEqual(memory['list_instance'][0], 'zero')
