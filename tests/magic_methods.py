import _
import unittest


class TestMagicMethods(unittest.TestCase):
    # def test_maths(self):
    #     compiled = _.compile_(
    #         '''
    #         instance = template() {
    #             # In some of the methods, an underscore is used as the name of
    #               the is_second_item flag, this is make the function declaration
    #               shorter, and indication what the value will not be accessed. #
    #
    #             __addition = function(other_item, _) {return (other_item * 5);};
    #
    #             __subtraction = function(other_item, _) {
    #                 return (string(other_item + 1));
    #             };
    #
    #             __multiplication = function(other_item, is_second_item) {
    #                 if (is_second_item) {
    #                     return (other_item + 1);
    #                 };
    #                 return (other_item - 1);
    #             };
    #
    #             __division = function(other_item, _) {};
    #
    #             __power = function(other_item, _) {
    #                 return (false);
    #             };
    #         }();
    #
    #         addition_result = 1 + instance;
    #         subtraction_result = instance - 0.2;
    #         reversed_subtraction_result = 0.2 - instance;
    #         multiplication_result = instance * 0;
    #         reversed_multiplication_result = 0 * instance;
    #         double_instance_multiplication_result = instance * instance;
    #         division_result = 2 / instance;
    #         power_result = 0 ^ instance;
    #         '''
    #     )
    #     memory = compiled.run()
    #     self.assertEqual(memory['addition_result'], 5)
    #     self.assertEqual(memory['subtraction_result'], '0.2')
    #     self.assertEqual(memory['reversed_subtraction_result'], '0.2')
    #     self.assertEqual(memory['multiplication_result'], -1)
    #     self.assertEqual(memory['reversed_multiplication_result'], 1)
    #     self.assertEqual(memory['double_instance_multiplication_result'], '2')
    #     self.assertIsNone(memory['division_result'])
    #     self.assertFalse(memory['power_result'])
    #
    # def test_casting(self):
    #     compiled = _.compile_(
    #         '''
    #         instance = template() {
    #             __float = function() {
    #                 return (1.8);
    #             };
    #
    #             __integer = function() {
    #                 return (2);
    #             };
    #
    #             __boolean = function() {
    #                 return (true);
    #             };
    #
    #             __string = function() {
    #                 return ('Six by nine.');
    #             };
    #         }();
    #
    #         float_value = float(instance);
    #         integer_value = integer(instace);
    #         boolean_value = boolean(instance);
    #         string_value = string(instance);
    #         '''
    #     )
    #     memory = compiled.run()
    #     self.assertEqual(memory['float_value'], 1.8)
    #     self.assertEqual(memory['integer_value'], 2)
    #     self.assertEqual(memory['boolean_value'], True)
    #     self.assertEqual(memory['string_value'], 'Six by nine.')

    def test_casting_errors(self):
        compiled = _.compile_(
            '''
            float(
                template() {
                    __float = function() {
                        return ('not a float');
                    };
                }()
            );
            '''
        )
        with self.assertRaises(_.exceptions.UnderscoreTypeError):
            compiled.run()
