import _
import unittest


class TestBooleanStatements(unittest.TestCase):
    def test_equality(self):
        compiled = _.compile_underscore(
            '''
            value_one = 5 == 5;
            value_two = 6 == 9;
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value_one'], True)
        self.assertEqual(memory['value_two'], False)

    def test_smaller_than_or_equal_to(self):
        compiled = _.compile_underscore(
            '''
            value_one = 5 <= 5;
            value_two = -3.2 <= -85/6;
            value_three = 1 <= 2;
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value_one'], True)
        self.assertEqual(memory['value_two'], False)
        self.assertEqual(memory['value_three'], True)

    def test_smaller_than(self):
        compiled = _.compile_underscore(
            '''
            value_one = -0.00000100 < 3.52;
            value_two = 12 < 9;
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value_one'], True)
        self.assertEqual(memory['value_two'], False)

    def test_greater_than_or_equal_to(self):
        compiled = _.compile_underscore(
            '''
            value_one = 5 >= 5;
            value_two = -6 >= 9.5;
            value_three = -2 >= -5;
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value_one'], True)
        self.assertEqual(memory['value_two'], False)
        self.assertEqual(memory['value_three'], False)

    def test_greater_than(self):
        compiled = _.compile_underscore(
            '''
            value_one = 5 > 5;
            value_two = 9 > 6;
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value_one'], True)
        self.assertEqual(memory['value_two'], False)

    def test_inequality(self):
        compiled = _.compile_underscore(
            '''
            value_one = 5 == 5;
            value_two = 6 == 9;
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value_one'], True)
        self.assertEqual(memory['value_two'], False)
