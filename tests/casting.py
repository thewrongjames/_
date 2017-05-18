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
        compiled = _.copmile_(
            '''
            value = float(function(){});
            '''
        )
        with self.assertRaises(_.exceptions.UnderscoreTypeError):
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
        compiled = _.copmile_(
            '''
            value = integer('18.6');
            '''
        )
        with self.assertRaises(_.exceptions.UnderscoreTypeError):
            compiled.run()

    def test_boolean(self):
        # Everything should be able to be casted to a boolean, so there is no
        # counter case.
        compiled = _.compile_(
            '''
            value_one = boolean(template(){});
            value_two = boolean(0);
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
            value_one = string(function(){});
            value_two = string(-12/5)
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value_one'], 'function')
        self.assertEqual(memory['value_two'], '-2.4')
