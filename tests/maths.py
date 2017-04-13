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
