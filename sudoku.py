from __future__ import print_function
import sys
import os
import itertools
from collections import Counter

class Cell:
  def __init__(self, value=None):
    self.value = value
    self.options = set() if value else set(range(1,10))

  def remove_option(self, opt_value):
      self.options.remove(opt_value)
      if len(self.options) == 1:
          self.value = self.options.pop()

  def set_value(self, value):
      self.value = value
      self.options.clear()

  def __str__(self):
    if self.value is not None:
      return str(self.value)
    else:
      return "X"


class Solver:
    def __init__(self):
        self._build_board()

    def _build_board(self):
        self.board = Board()

    def set(self, cell, value):
        x, y = cell
        self.board[x][y].set_value(value)
        # remove option for other cells in the row and column
        for i in range(0,9):
            if i != x:
                self.board[i][y].remove_option(value)
            if i != y:
                self.board[x][i].remove_option(value)


class Board:
    def __init__(self):
        self.data = {k:{j:Cell() for j in range(0,9)} for k in range(0,9)}

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value


