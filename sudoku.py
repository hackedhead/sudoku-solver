from __future__ import print_function
import sys
import os

class Cell:
  def __init__(self):
    self.value = None
    self.options = [1,2,3,4,5,6,7,8,9]

  def __str__(self):
    if self.value is not None:
      return self.value
    else:
      return "X"

class Board:
  def __init__(self):
    self.rows = {k:{j:Cell() for j in range(0,9)} for k in range(0,9)}

  def print(self):
    for x in range(0,9):
      for y in range(0,9):
        print(self.rows[x][y], end=" ")
        if y in [2,5]:
          print("|", end=" ")
      print()
      if x in [2,5]:
        print("-"*(9*2+3))
  
def usage():
  print("Usage: python sudoku.py <puzzle_file>")

if len(sys.argv) != 2:
  usage()
  sys.exit()

puzzle_filename = sys.argv[1]

board = Board()

pfile = open(puzzle_filename,'r')
for lineno,line in enumerate(pfile):
  if len(line) != 10:
    print("Bad puzzle format line: {lineno}".format(lineno=lineno))
    sys.exit()
  for col,digit in enumerate(line):
    if col == 9:
      continue
    if digit != 'X':
      if digit.isdigit():
        board.rows[lineno][col] = digit
      else:
        print("Bad digit on line: {lineno}".format(lineno=lineno))
        sys.exit()
board.print()
