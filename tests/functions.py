import _
import unittest


class TestFunctions(unittest.TestCase):
    def test_return(self):
        compiled = _.compile_(
            '''
            value = function(){return(5);}();
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value'], 5)

    def test_python_callable(self):
        compiled = _.compile_(
            '''
            instance = function(){return('bar');};
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['instance'](), 'bar')

    def test_method_like_behaviour(self):
        compiled = _.compile_(
            '''
            instance = template(){
                value = 7;
                method = function(){
                    container.value = 'bar';
                };
            }();
            first_value = instance.value;
            instance.method();
            second_value = instance.value;
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['first_value'], 7)
        self.assertEqual(memory['second_value'], 'bar')

    def test_passing_in(self):
        compiled = _.compile_(
            '''
            add = function(this, that) {
                return (this + that);
            };
            eight = add(3, 5);
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['eight'], 8)

    def test_passing_in_more_complex_expressions(self):
        compiled = _.compile_(
            '''
            add = function(this, that) {
                return (this + that);
            };
            two_point_five = 2.5;
            negative_fifty_four = -54;
            value = add(
                (two_point_five * 2) - 1, negative_fifty_four / (1.5 * 4)
            );
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value'], -5)

    def test_name_expression_mismatch(self):
        compiled = _.compile_(
            '''
            function_ = function(this, that) {};
            call = function_(1);
            '''
        )
        with self.assertRaises(_.exceptions.UnderscoreTypeError):
            compiled.run()

    def test_recursion(self):
        # Quite a bit needs to be done before this will work.
        # Perhaps I need to make a return node? Something that when run errors
        # in a way that the function catches? And returns what it needs to.
        compiled = _.compile_(
            '''
            factorial = function(number) {
                if (number <= 1) {
                    return (1);
                };
                return (number * factorial(number-1));
            };
            '''
        )
