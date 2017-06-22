import _
import unittest


class TestMaths(unittest.TestCase):
    def test_addition(self):
        compiled = _.compile_(
            '''
            value_one = 3 + 4;
            value_two = 12.5 + - 18;
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value_one'], 7)
        self.assertEqual(memory['value_two'], -5.5)

    def test_subtraction(self):
        compiled = _.compile_(
            '''
            value_one = 12.1 - 6;
            value_two = -3 - -5;
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value_one'], 6.1)
        self.assertEqual(memory['value_two'], 2)

    def test_multiplication(self):
        compiled = _.compile_(
            '''
            value = 6 * 9;
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value'], 54)

    def test_division(self):
        compiled = _.compile_(
            '''
            value = -6 / 0.2;
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value'], -30)

    def test_power(self):
        compiled = _.compile_(
            '''
            value = (3 + 1) ^ (-1 / 2);
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value'], 0.5)

    def test_brackets(self):
        compiled = _.compile_(
            '''
            value = 6 * (9 - 2);
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value'], 42)

    def test_reference(self):
        compiled = _.compile_(
            '''
            value_one = -1/2;
            value_two = 3 * value_one;
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value_two'], -1.5)

    def test_type_error(self):
        compiled = _.compile_(
            '''
            function () {} - 5;
            '''
        )
        with self.assertRaises(_.exceptions.UnderscoreTypeError):
            compiled.run()

    def test_addition_subtraction_order(self):
        """
        This test and the test below it were created due to a mistake in the
        parser design that meant that addition and multiplication could be
        parsed after subtraction and division respectively.
        """
        compiled = _.compile_(
            '''
            number_value = 0-1+2;
            boolean_value = 0-1+2 == -1+2;
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['number_value'], 1)
        self.assertTrue(memory['boolean_value'])

    def test_multiplication_and_division_order(self):
        compiled = _.compile_(
            '''
            value = 1/2*2;
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value'], 1)

    def test_chaining_maths(self):
        compiled = _.compile_(
            '''
            value_one = 6+34-34;
            value_two = 3-8/2+5;
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value_one'], 6)
        # Float comparison should be okay because both were done in python.
        self.assertEqual(memory['value_two'], 4)
