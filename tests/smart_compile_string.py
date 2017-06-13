import _
import unittest

class TestSmartCompileString(unittest.TestCase):
    def test_main(self):
        program_one, pickle_one = _.smart_compile_string('value=5;')
        value_one = program_one.run()['value']
        program_two, pickle_two = _.smart_compile_string(
            program_string='value=5;',
            pickle_bytes_string=pickle_one,
            underscore_last_modified_time=0,
            pickle_last_modified_time=1,
            running_underscore_standard_library=False,
            force_pickle_update=False,
        )
        value_two = program_two.run()['value']
        self.assertTrue(value_one == value_two == 5)
