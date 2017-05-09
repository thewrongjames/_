import _
import unittest

class TestReferences(unittest.TestCase):
    def test_properties_compile(self):
        _.compile_('this.that.this.that.this.that;')

    def test_square_brackets(self):
        compiled = _.compile_(
            '''
            instance = template() {
                set(54, 42);
            }();
            six = 6;
            nine = 9;
            value = instance[six*nine];
            '''
        )
        memory = compiled.run()
        self.assertEqual(value, 42)
