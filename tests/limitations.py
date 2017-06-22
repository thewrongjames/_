import _
import unittest
import os
import time


class TestLimitations(unittest.TestCase):
    # def test_time_limit(self):
    #     compiled = _.compile_('while(true){};', time_limit=2)
    #     start_time = time.time()
    #     with self.assertRaises(_.exceptions.UnderscoreOutOfTimeError):
    #         compiled.run()
    #     total_time = time.time() - start_time
    #     # Just getting to here at all means that the time_limit worked.
    #     # Give it a (large) buffer of two seconds for overhead.
    #     self.assertTrue(total_time < 4)

    def test_memory_limit(self):
        compiled = _.smart_compile_file(
            os.path.dirname(__file__) +
                '/file_tests/limitations/test_memory_limit._',
            memory_limit=200
        )
        with self.assertRaises(_.exceptions.UnderscoreOutOfMemoryError):
            compiled.run()
