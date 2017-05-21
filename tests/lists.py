import _
import unittest


class TestLists(unittest.TestCase):
    def test_lists(self):

        compiled = _.compile_(
            '''
            list_instance = List();

            list_instance.append('this');
            list_instance.append(-7.2);

            value_one = list_instance.pop(0);
            value_two = list_instance[0 / 9];
            '''
        )

        memory = compiled.run()

        self.assertEqual(memory['value_one'], 'this')
        self.assertEqual(memory['value_two'], -7.2)
