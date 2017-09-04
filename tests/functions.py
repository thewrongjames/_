import _
import unittest
import os


class TestFunctions(unittest.TestCase):
    def test_basic_return(self):
        compiled = _.compile_(
            '''
            value = function(){return(5);}();
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value'], 5)

    def test_not_at_end_return(self):
        compiled = _.compile_file(
            os.path.dirname(__file__) +
            '/file_tests/functions/test_not_at_end_return._'
        )
        memory = compiled.run()
        self.assertEqual(memory['definately_not_eight'], 9)
        self.assertEqual(memory['value_one'], 'this')
        self.assertEqual(memory['value_two'], 'that')

    def test_return_outside_of_function_raises_error(self):
        compiled = _.compile_(
            '''
            return(5);
            '''
        )
        with self.assertRaises(_.exceptions.UnderscoreReturnError):
            compiled.run()

    def test_python_callable(self):
        compiled = _.compile_(
            '''
            instance = function(){return('bar');};
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['instance']({}, []), 'bar')

    def test_method_like_behaviour(self):
        compiled = _.compile_file(
            os.path.dirname(__file__) +
            '/file_tests/functions/test_method_like_behaviour._'
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
        compiled = _.compile_(
            '''
            factorial = function(number) {
                if (number <= 1) {
                    return (1);
                };
                return (number * container.factorial(number-1));
            };
            value = factorial(5);
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value'], 120)

    def test_expressions_resolve_in_correct_scope(self):
        compiled = _.compile_file(
            os.path.dirname(__file__) +
            '/file_tests/functions/test_expressions_resolve_in_correct_scope._'
        )
        memory = compiled.run()
        self.assertEqual(memory['template_instance']['this_plus_one'], 2)
        self.assertEqual(memory['template_instance']['that'], 1)
