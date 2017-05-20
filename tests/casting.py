import _
import unittest


class TestCasting(unittest.TestCase):
    def test_float_where_possible(self):
        compiled = _.compile_(
            '''
            value = float('-0.289');
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value'], -0.289)

    def test_float_where_not_possible(self):
        compiled = _.compile_(
            '''
            value = float(function(){});
            '''
        )
        with self.assertRaises(_.exceptions.UnderscoreValueError):
            compiled.run()

    def test_integer_where_possible(self):
        compiled = _.compile_(
            '''
            value_one = integer('63');
            value_two = integer(-8.9);
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value_one'], 63)
        self.assertEqual(memory['value_two'], -8)

    def test_integer_where_not_possible(self):
        compiled = _.compile_(
            '''
            value = integer('18.6');
            '''
        )
        with self.assertRaises(_.exceptions.UnderscoreValueError):
            compiled.run()

    def test_boolean(self):
        # Everything should be able to be casted to a boolean, so there is no
        # counter case.
        compiled = _.compile_(
            '''
            value_one = boolean(7);
            value_two = boolean('');
            '''
        )
        memory = compiled.run()
        self.assertTrue(memory['value_one'])
        self.assertFalse(memory['value_two'])

    def test_string(self):
        # Everything should be able to be casted to a string, so there is no
        # counter case.
        compiled = _.compile_(
            '''
            value_one = string(false);
            value_two = string(-12/5);
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value_one'], 'False')
        # Unfortunately because it is the python value being casted, the boolean
        # values and none will have capital letters, but, we will just have to
        # live with that for now.
        self.assertEqual(memory['value_two'], '-2.4')
