import _
import unittest


class TestTemplates(unittest.TestCase):
    # def test_basics(self):
    #     _.compile_('    template ( )   {};')
    #
    # def test_internal_values(self):
    #     compiled = _.compile_('value=template(){value=18;}();')
    #     memory = compiled.run()
    #     self.assertEqual(memory['value']['value'], 18)
    #
    # def test_container_access(self):
    #     compiled = _.compile_(
    #         '''
    #         value = -2.5;
    #         template_ = template () {
    #             value=container.value;
    #         };
    #         instance = template_();
    #         '''
    #     )
    #     memory = compiled.run()
    #     self.assertEqual(memory['instance']['value'], -2.5)
    #
    # def test_external_access_to_template(self):
    #     compiled = _.compile_(
    #         '''
    #         instance = template(){value='foo';}();
    #         value = instance.value;
    #         '''
    #     )
    #     memory = compiled.run()
    #     self.assertEqual(memory['value'], 'foo')
    #
    # def test_modifying_from_external_values(self):
    #     compiled = _.compile_(
    #         '''
    #         external_value = false;
    #         instance = template(){
    #             internal_value = container.external_value;
    #         }();
    #         '''
    #     )
    #     memory = compiled.run()
    #     self.assertEqual(memory['instance']['internal_value'], False)
    #
    # def test_modifying_external_values(self):
    #     compiled = _.compile_(
    #         '''
    #         external_value = -95.3;
    #         instance = template(){
    #             container.external_value = 8;
    #         }();
    #         '''
    #     )
    #     memory = compiled.run()
    #     self.assertEqual(memory['external_value'], 8)
    #
    # def test_nested_template_access(self):
    #     compiled = _.compile_(
    #         '''
    #         template_1 = template(){
    #             value = 7;
    #             template_2 = template(){
    #                 container.value = 'bar';
    #             };
    #         };
    #         instance = template_1();
    #         first_value = instance.value;
    #         instance.template_2();
    #         second_value = instance.value;
    #         '''
    #     )
    #     memory = compiled.run()
    #     self.assertEqual(memory['first_value'], 7)
    #     self.assertEqual(memory['second_value'], 'bar')
    #
    # def test_container_updates(self):
    #     compiled = _.compile_(
    #         '''
    #         external_value = -15.4;
    #         template_ = template(){
    #             internal_value = container.external_value;
    #         };
    #         first_value = template_().internal_value;
    #         external_value = true;
    #         second_value = template_().internal_value;
    #         '''
    #     )
    #     memory = compiled.run()
    #     self.assertEqual(memory['first_value'], -15.4)
    #     self.assertEqual(memory['second_value'], True)
    #
    # def test_passing_in(self):
    #     compiled = _.compile_(
    #         '''
    #         template_ = template(thing_one, thing_two) {
    #             this = thing_one;
    #         };
    #         instance_one = template_(1, 2);
    #         instance_two = template_('false', none);
    #         value_one = instance_one.this;
    #         value_two = instance_two.thing_two;
    #         '''
    #     )
    #     memory = compiled.run()
    #     self.assertEqual(memory['value_one'], 1)
    #     self.assertEqual(memory['value_two'], None)

    def test_key_value_assignment(self):
        compiled = _.compile_(
            '''
            list = template() {
                length = 0;

                append = function(item) {
                    container.set('length', item);
                    container.length = container.length + 1;
                };

                pop = function(index) {
                    value = container.get(index);
                    while (index < container.length - 1) {
                        container.set(index, container.get(index + 1));
                    };
                    container.delete(container.length - 1);
                    container.length = container.length - 1;
                    return (value);
                };
            };

            list_instance = list();
            '''
        )
        print('Compiled')
        memory = compiled.run()
        print(memory)
        print('Run')
        # self.assertEqual(memory['value'], -7.2)
        # self.assertEqual(memory['list_instance'][1], False)

compiled = (#_.compile_(
    '''
    list = template() {
        length = 0;

        append = function(item) {
            container.set('length', item);
            container.length = container.length + 1;
        };

        pop = function(index) {
            value = container.get(index);
            while (index < container.length - 1) {
                container.set(index, container.get(index + 1));
            };
            container.delete(container.length - 1);
            container.length = container.length - 1;
            return (value);
        };
    };

    list_instance = list();
    list_instance.append('this');
    list_instance.append(-7.2);
    list_instance.append(false);

    value_one = list_instance.pop(1);
    value_two = list_instance[0 / 9];
    '''
)
