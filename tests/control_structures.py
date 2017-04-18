import _
import unittest


class TestControlStructures(unittest.TestCase):
    def test_if(self):
        compiled = _.compile_(
        '''
        value_one = 5;
        if (false) {
            value_one = 7;
        };
        if (5 > 2) {
            value_two = value_one - 2.3;
        };
        '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value_one'], 5)
        self.assertEqual(memory['value_two'], 2.7)

    def test_else(self):
        compiled = _.compile_(
            '''
            if (2 <= -0.3) {
                value = none;
            } else {
                value = 'seven';
            };
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value'], 'seven')

    def test_else_if(self):
        compiled = _.compile_(
            '''
            if (2 < 1) {
                value = 'bar';
            } else { if (3) {
                value = 'foo';
            } else {
                value = none;
            };};
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value'], 'foo')

    def test_while(self):
        compiled = _.compile_(
            '''
            iterator = 0;
            value = 2;
            while (iterator < 3) {
                value = value * 2;
                iterator = iterator + 1;
            };
            '''
        )
