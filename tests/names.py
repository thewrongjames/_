import _
import unittest


class TestNames(unittest.TestCase):
    def test_reserved_words(self):
        with self.assertRaises(_.exceptions.UnderscoreCouldNotConsumeError):
            _.compile_underscore('return = 7;')

    def test_name_error(self):
        with self.assertRaises(_.exceptions.UnderscoreNameError):
            _.compile_underscore('this=that;').run()

    def test_containers(self):
        compiled = _.compile_underscore(
            '''
            template_ = template () {
                thing = 'this';
            };
            template_instance = template_();
            value_one = template_instance.thing;
            template_instance.thing = 'that';
            value_two = template_instance.thing;
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value_one'], 'this')
        self.assertEqual(memory['value_two'], 'that')
