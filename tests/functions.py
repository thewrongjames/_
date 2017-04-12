import _
import unittest


class TestFunctions(unittest.TestCase):
    def test_return(self):
        compiled = _.compile_underscore(
            '''
            value = function(){return(5);}();
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['value'], 5)

    def test_python_callable(self):
        compiled = _.compile_underscore(
            '''
            instance = function(){return('bar');};
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['instance'](), 'bar')

    def test_method_like_behaviour(self):
        compiled = _.compile_underscore(
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
        return
        compiled = _.compile_underscore(
            '''
            add = function(this, that) {
                return (this + that);
            };
            eight = add(3, 5);
            '''
        )
        memory = compiled.run()
        self.assertEqual(memory['eight'], 8)

    def test_recursion(self):
        return
        # Quite a bit needs to be done before this will work.
        # Perhaps I need to make a return node? Something that when run errors
        # in a way that the function catches? And returns what it needs to.
        compiled = _compile_underscore(
            '''
            factorial = function(number) {
                if (number <= 1) {
                    return (1);
                }
                return (number * factorial(number-1));
            };
            '''
        )
