import _
import unittest
import sys
import time


class TestLimitations(unittest.TestCase):
    def test_time_limit(self):
        compiled = _.compile_('while(true){};', time_limit=2)
        start_time = time.time()
        with self.assertRaises(_.exceptions.UnderscoreOutOfTimeError):
            compiled.run()
        total_time = time.time() - start_time
        # Just getting to here at all means that the time_limit worked.
        # Give it a (large) buffer of two seconds for overhead.
        self.assertTrue(total_time < 4)

    def test_memory_limit(self):
        compiled = _.compile_(
            '''
            template_instance = template() {
                index = 0;
                while(true){
                    set(index, 'This should be fifty-six bytes.');
                    index = index + 1;
                };
            }();
            ''',
            memory_limit=221
        )
        with self.assertRaises(_.exceptions.UnderscoreOutOfMemoryError):
            compiled.run()
