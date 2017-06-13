import _
import unittest


class TestMagicMethods(unittest.TestCase):
    def test_maths(self):
        compiled = _.smart_compile_file(
            'tests/file_tests/magic_methods/test_maths._'
        )
        memory = compiled.run()
        self.assertEqual(memory['addition_result'], 5)
        self.assertEqual(memory['subtraction_result'], '1.2')
        self.assertEqual(memory['reversed_subtraction_result'], '1.2')
        self.assertEqual(memory['multiplication_result'], -1)
        self.assertEqual(memory['reversed_multiplication_result'], 1)
        self.assertEqual(memory['double_instance_multiplication_result'], '2')
        self.assertIsNone(memory['division_result'])
        self.assertFalse(memory['power_result'])

    def test_casting(self):
        return
        compiled = _.smart_compile_file(
            'tests/file_tests/magic_methods/test_casting._'
        )
        memory = compiled.run()
        self.assertEqual(memory['float_value'], 1.8)
        self.assertEqual(memory['integer_value'], 2)
        self.assertEqual(memory['boolean_value'], True)
        self.assertEqual(memory['string_value'], 'Six by nine.')

    def test_casting_errors(self):
        return
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
