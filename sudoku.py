from __future__ import print_function
import copy
import re
import time
import sys
import argparse


class Cell:
    def __init__(self, value=None):
        self.value = value
        self.options = set() if value else set(range(1, 10))
        self.confidence = None

    def remove_option(self, opt_value):
        self.options.discard(opt_value)
        if len(self.options) == 0 and self.value is None:
            raise AttributeError("Cell has no remaining options")

    def set_value(self, value, confidence=None):
        self.value = value
        self.options.clear()
        self.confidence = confidence

    def __str__(self):
        pass


class Solver:
    @staticmethod
    def solve(board, confidence):
        time.sleep(0.08)
        render_board(board)
        sys.stdout.flush()
        best_cell = None
        best_count = None
        for px in range(0, 9):
            for py in range(0, 9):
                opt_count = len(board[px][py].options)
                if opt_count > 0:
                    if best_count is None or opt_count < best_count:
                        best_cell = (px, py)
                        best_count = opt_count
        if best_count is None:
            render_board(board)
            print("Complete!")
            return board
        else:
            px, py = best_cell
            # print("Attempting to assign into {cell}".format(cell=best_cell))
            options = list(board[px][py].options)
            for count, candidate_value in enumerate(options):
                new_confidence = confidence/(len(options)-count)
                try:
                    newboard = copy.deepcopy(board)
                    newboard.set((px, py), candidate_value, new_confidence)
                except AttributeError as err:
                    # print(err)
                    continue
                try:
                    return Solver.solve(newboard, new_confidence)
                except AttributeError as err:
                    # print(err)
                    continue
            raise AttributeError("Ran out of options")


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

    def set(self, cell, value, confidence=None):
        x, y = cell
        if value not in self.data[x][y].options:
            raise ValueError("{value} is not a valid option for Cell({x},{y})".format(x=x, y=y, value=value))
        self.data[x][y].set_value(value, confidence)
        # remove option for other cells in the row and column
        for i in range(0, 9):
            try:
                self.data[i][y].remove_option(value)
            except AttributeError as err:
                message = "Cell ({x},{y}): {err}".format(x=i, y=y, err=err)
                # print(message)
                raise AttributeError(message)
            try:
                self.data[x][i].remove_option(value)
            except AttributeError as err:
                message = "Cell ({x},{y}): {err}".format(x=x, y=i, err=err)
                # print(message)
                raise AttributeError(message)
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

    def emit(self):
        output_string = ""
        for x in range(0, 9):
            for y in range(0, 9):
                output_string += "X" if self.data[x][y].value is None else str(self.data[x][y].value)
        return output_string


class Loader:
    @staticmethod
    def create_board_from_file(filename):
        input_string = ""
        with open(filename, "r") as input_file:
            for line in input_file:
                input_string += line.strip("\r\n")
        return Board(input_string)

def render_board(board):
    def render_cell(cell):
        if cell.value is not None:
            colors = {0: "\x1b[1;97m",  # bright white
                      1: "\x1b[1;96m",  # bright cyan
                      2: "\x1b[1;92m",  # bright green
                      3: "\x1b[1;93m",  # bright yellow
                      4: "\x1b[1;91m",  # bright red
                      5: "\x1b[1;31m",  # red
                      6: "\x1b[1;33m",  # yellow
                      7: "\x1b[1;35m",  # magenta
                      }

            def get_color(confidence):
                """
                Confidence intervals are chosen based on picking
                1 from 2,3,4 and then halving or thirding those numbers.
                1/2 -> 0.5
                1/3 -> 0.33
                1/4 -> 0.25
                1/2 -> 1/2 -> 0.25
                1/2 -> 1/2 -> 1/2 -> 0.125
                1/3 -> 1/3 -> 0.11
                1/3 -> 1/3 -> 1/3 -> 0.05
                1/3 -> 1/2 -> 0.13
                1/3 -> 1/4 -> 0.08
                etc
                """
                if confidence is None:
                    return colors[0]
                if confidence > 0.5:  # known
                    return colors[1]
                elif confidence > 0.33:  # 1/2
                    return colors[2]
                elif confidence > 0.25:  # 1/3
                    return colors[3]
                elif confidence > 0.33/2:  # 1/4
                    return colors[4]
                elif confidence > 0.125:
                    return colors[5]
                elif confidence > 0.08:
                    return colors[6]
                else:
                    return colors[7]

            return ("{color}{value}{reset}"
                    .format(color=get_color(cell.confidence),
                            value=str(cell.value),
                            reset="\x1b[0m"))
        else:
            return "·"

    cyan_vertical_pipe = "\x1b[1;36m|\x1b[0m"
    cyan_horizontal_pipe = "\x1b[1;36m-\x1b[0m"
    output_string = ""
    for x in range(0, 9):
        for y in range(0, 9):
            output_string += render_cell(board[x][y]) + " "
            if y in [2, 5]:
                output_string += cyan_vertical_pipe + " "
        output_string += "\n"
        if x in [2, 5]:
            output_string += cyan_horizontal_pipe * (9*2+3) + "\n"
    print(output_string)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="the filename of the puzzle to solve")
    args = parser.parse_args()
    board = Loader.create_board_from_file(args.filename)
    render_board(board)
    Solver.solve(board, 1)
