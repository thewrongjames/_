import _
import unittest


class TestBooleanExpressions(unittest.TestCase):
    def test_and(self):
        compiled = _.compile_(
            '''
            value_one = true AND true;
            value_two = true AND false;
            value_three = false AND false;
            '''
        )
        memory = compiled.run()
        self.assertTrue(memory['value_one'])
        self.assertFalse(memory['value_two'])
        self.assertFalse(memory['value_three'])

    def test_or(self):
        compiled = _.compile_(
            '''
            value_one = true OR true;
            value_two = true OR false;
            value_three = false OR false;
            '''
        )
        memory = compiled.run()
        self.assertTrue(memory['value_one'])
        self.assertTrue(memory['value_two'])
        self.assertFalse(memory['value_three'])

    def test_not(self):
        compiled = _.compile_(
            '''
            value_one = NOT false;
            value_two = NOT true;
            '''
        )
        memory = compiled.run()
        self.assertTrue(memory['value_one'])
        self.assertFalse(memory['value_two'])

    def test_complex_expressions(self):
        compiled = _.compile_(
            '''
            value = (6 < 3) OR ((-5 < 2) AND ((NOT true) OR (1 == 1)));
            '''
        )
        memory = compiled.run()
        self.assertTrue(memory['value'])


class TestBooleanStatements(unittest.TestCase):
    def test_equality(self):
        compiled = _.compile_(
            '''
            value_one = 5 == 5;
            value_two = 6 == 9;
            '''
        )
        memory = compiled.run()
        self.assertTrue(memory['value_one'])
        self.assertFalse(memory['value_two'])

    def test_smaller_than_or_equal_to(self):
        compiled = _.compile_(
            '''
            value_one = 5 <= 5;
            value_two = -3.2 <= (-85/6);
            value_three = 1 <= 2;
            '''
        )
        memory = compiled.run()
        self.assertTrue(memory['value_one'])
        self.assertFalse(memory['value_two'])
        self.assertTrue(memory['value_three'])

    def test_smaller_than(self):
        compiled = _.compile_(
            '''
            value_one = -0.00000100 < 3.52;
            value_two = 12 < 9;
            '''
        )
        memory = compiled.run()
        self.assertTrue(memory['value_one'])
        self.assertFalse(memory['value_two'])

    def test_greater_than_or_equal_to(self):
        compiled = _.compile_(
            '''
            value_one = 5 >= 5;
            value_two = -6 >= 9.5;
            value_three = -2 >= -5;
            '''
        )
        memory = compiled.run()
        self.assertTrue(memory['value_one'])
        self.assertFalse(memory['value_two'])
        self.assertTrue(memory['value_three'])

    def test_greater_than(self):
        compiled = _.compile_(
            '''
            value_one = 5 > 5;
            value_two = 9 > 6;
            '''
        )
        memory = compiled.run()
        self.assertFalse(memory['value_one'])
        self.assertTrue(memory['value_two'])

    def test_inequality(self):
        compiled = _.compile_(
            '''
            value_one = 5 == 5;
            value_two = 6 == 9;
            '''
        )
        memory = compiled.run()
        self.assertTrue(memory['value_one'])
        self.assertFalse(memory['value_two'])
