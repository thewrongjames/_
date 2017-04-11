def _peek(self, look_ahead_distance=1):
    if self.position_in_program < len(self.program):
        return self.program[
            self.position_in_program:
            self.position_in_program+look_ahead_distance
        ]
    # If you are at or past the end of the program, this will return none.
