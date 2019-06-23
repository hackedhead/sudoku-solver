from __future__ import print_function
import re


class Cell:
    def __init__(self, value=None):
        self.value = value
        self.options = set() if value else set(range(1, 10))

    def remove_option(self, opt_value):
        self.options.discard(opt_value)
        if len(self.options) == 0 and self.value is None:
            raise AttributeError("Cell has no remaining options")

    def set_value(self, value):
        self.value = value
        self.options.clear()

    def __str__(self):
        if self.value is not None:
            return str(self.value)
        else:
            return "·"


class Solver:
    def __init__(self):
        self._build_board()

    def _build_board(self):
        self.board = Board()


class Board:
    def __init__(self, board_string=None):
        self.data = {k: {j: Cell() for j in range(0, 9)} for k in range(0, 9)}
        if board_string is not None:
            pattern = re.compile("[1-9X]{81}")
            if not pattern.fullmatch(board_string):
                raise ValueError
            else:
                for x in range(0, 9):
                    row_offset = x * 9
                    row_string = board_string[row_offset:row_offset+9]
                    for y, char in enumerate(row_string):
                        if char is not "X":
                            self.set((x, y), int(char))

    def set(self, cell, value):
        x, y = cell
        if value not in self.data[x][y].options:
            raise ValueError("{value} is not a valid option for Cell({x},{y})".format(x=x, y=y, value=value))
        self.data[x][y].set_value(value)
        # remove option for other cells in the row and column
        for i in range(0, 9):
            self.data[i][y].remove_option(value)
            self.data[x][i].remove_option(value)
        # remove option for other cells in square (3x3)
        xbase = x - (x % 3)
        ybase = y - (y % 3)
        for sq_x in range(xbase, xbase+3):
            for sq_y in range(ybase, ybase+3):
                self.data[sq_x][sq_y].remove_option(value)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __str__(self):
        cyan_vertical_pipe = "\x1b[1;36m|\x1b[0m"
        cyan_horizontal_pipe = "\x1b[1;36m-\x1b[0m"
        output_string = ""
        for x in range(0,9):
            for y in range(0,9):
                output_string += str(self.data[x][y]) + " "
                if y in [2,5]:
                    output_string += cyan_vertical_pipe + " "
            output_string += "\n"
            if x in [2,5]:
                output_string += cyan_horizontal_pipe * (9*2+3) + "\n"
        return output_string

class Loader:
    @staticmethod
    def create_board_from_file(filename):
        input_string = ""
        with open(filename, "r") as input_file:
            for line in input_file:
                input_string += line.strip("\r\n")
        return Board(input_string)
