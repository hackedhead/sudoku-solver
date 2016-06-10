from __future__ import print_function
import sys
import os
import itertools

class Cell:
  def __init__(self):
    self.value = None
    self.options = set([1,2,3,4,5,6,7,8,9])

  def __str__(self):
    if self.value is not None:
      return str(self.value)
    else:
      return "X"

class Board:

  def load_file(self, puzzle_filename):
    pfile = open(puzzle_filename,'r')
    for row,line in enumerate(pfile):
      if len(line) != 10:
        print("Bad puzzle format line: {lineno}".format(lineno=row))
        sys.exit()
      for col,digit in enumerate(line):
        if col == 9:
          continue
        if digit != 'X':
          if digit.isdigit():
            self.update_cell(row, col, int(digit))
          else:
            print("Bad digit on line: {lineno}".format(lineno=row))
            sys.exit()
    pfile.close()

  @staticmethod
  def get_squares_cells(x,y):
    """ Given a Cell, return all the Cells in the square"""
    # the simplest, dumbest way to do this is just to generate the set of
    # tuples for each square and return the set to which the target tuple 
    # belongs
    squares = [ 
          [ (0,0), (0,1), (0,2),
            (1,0), (1,1), (1,2),
            (2,0), (2,1), (2,2) ],
          [ (3,0), (3,1), (3,2), 
            (4,0), (4,1), (4,2), 
            (5,0), (5,1), (5,2) ],
          [ (6,0), (6,1), (6,2), 
            (7,0), (7,1), (7,2), 
            (8,0), (8,1), (8,2) ],

          [ (0,3), (0,4), (0,5),
            (1,3), (1,4), (1,5),
            (2,3), (2,4), (2,5) ],
          [ (3,3), (3,4), (3,5), 
            (4,3), (4,4), (4,5), 
            (5,3), (5,4), (5,5) ],
          [ (6,3), (6,4), (6,5), 
            (7,3), (7,4), (7,5), 
            (8,3), (8,4), (8,5) ],

          [ (0,6), (0,7), (0,8),
            (1,6), (1,7), (1,8),
            (2,6), (2,7), (2,8) ],
          [ (3,6), (3,7), (3,8), 
            (4,6), (4,7), (4,8), 
            (5,6), (5,7), (5,8) ],
          [ (6,6), (6,7), (6,8), 
            (7,6), (7,7), (7,8), 
            (8,6), (8,7), (8,8) ],
        ]
    for sq in squares:
      if (x,y) in sq:
        return sq
  
  def scan_singles(self):
    """The scan function walks the board checking for single-option cells,
    when one is found we call update_cell, then break the loop immediately,
    since the table state is now "dirty" and previous results may be invalid.

    We call scan repeatedly until it reports it finds no changes to make.
    """
    def scan():
      clean = True
      for row in range(0,9):
        for col in range(0,9):
          if len(self.rows[row][col].options) == 1:
            value = self.rows[row][col].options.pop()
            self.update_cell(row, col, value)
            clean = False
          if not clean:
            break
        if not clean:
          print("Scan chain broken updating {row},{col}, restarting".format(row=row,col=col))
          break
      return clean

    counter = 1
    while True:
      clean = scan()
      if clean:
        break
      counter += 1
    print("Scanned singles {counter} times.".format(counter=counter))
    return counter-1

  def scan_cols(self):
    """Check each column to see if any option values only appear once in the column"""
    def scan():
      clean = True
      for col in range(0,9):
        # store list of rows for each opt_val (any opt_val having only one col is updatable
        opts_seen = { k: set() for k in range(1,10)}
        for row in range(0,9):
          for opt_val in self.rows[row][col].options:
            opts_seen[opt_val].add(row)
        for opt_val in opts_seen.keys():
          if len(opts_seen[opt_val]) == 1: # only one candidate
            urow = opts_seen[opt_val].pop()
            self.update_cell(urow, col, opt_val)
            clean = False
            print("Scan chain broken updating {row},{col}, restarting".format(row=urow,col=col))
            break
        if not clean:
          break
      return clean

    counter = 1
    while True:
      clean = scan()
      if clean:
        break
      counter += 1
    print("Scanned columns {counter} times.".format(counter=counter))
    return counter-1

  def scan_rows(self):
    """Check each row to see if any option values only appear once in the row"""
    def scan():
      clean = True
      for row in range(0,9):
        # store list of cols for each opt_val (any opt_val having only one row is updatable
        opts_seen = { k: set() for k in range(1,10)}
        for col in range(0,9):
          for opt_val in self.rows[row][col].options:
            opts_seen[opt_val].add(col)
        for opt_val in opts_seen.keys():
          if len(opts_seen[opt_val]) == 1: # only one candidate column
            ucol = opts_seen[opt_val].pop()
            self.update_cell(row, ucol, opt_val)
            clean = False
            print("Scan chain broken updating {row},{col}, restarting".format(row=row,col=ucol))
            break
        if not clean:
          break
      return clean

    counter = 1
    while True:
      clean = scan()
      if clean:
        break
      counter += 1
    print("Scanned rows {counter} times.".format(counter=counter))
    return counter-1

  def scan_squares(self):
    """ check for solo opt_vals in each square, call update_cell as appropriate"""
    def scan():
      target_cells = [ (0,0),
                       (3,0),
                       (6,0),
                       (0,3),
                       (3,3),
                       (6,3),
                       (0,6),
                       (3,6),
                       (6,6),
                      ]
      clean = True
      for square in [board.get_squares_cells(*x) for x in target_cells]:
        opts_seen = { k: set() for k in range(1,10)}
        for (row,col) in square:
          for opt_val in self.rows[row][col].options:
            opts_seen[opt_val].add( (row,col) )
        for opt_val in opts_seen.keys():
          if len(opts_seen[opt_val]) == 1:
            (urow,ucol) = opts_seen[opt_val].pop()
            self.update_cell(urow,ucol,opt_val)
            clean = False
            print("Scan chain broken updating {row},{col}, restarting".format(row=row,col=ucol))
            break
        if not clean:
          break
      return clean

    counter = 1
    while True:
      clean = scan()
      if clean:
        break
      counter += 1
    print("Scanned squares {counter} times.".format(counter=counter))
    return counter-1

  def row_tuples(self):
    """check for row tuples and elimate options in non-tuple cells"""
    def scan():
      clean = True
      for row in range(0,9):
        pcols = [col for col in range(0,9) if self.rows[row][col].value is None]
        max_tuple_size = len(pcols)
        for tuple_size in range(2,max_tuple_size):
          #  12, 13, 14, 15, 23, 24, 25, 34, 35, 45  
          # itertools.combinations(iterable,length)
          column_combos = list(itertools.combinations(pcols,tuple_size))
          #print("column combos for row {row}: {combos}".format(row=row,combos=str(column_combos)))
          # union the options from the pcols together and check if size is == tuple_size
          # ... it shouldn't be able to be smaller than tuple-size, i think...
          for combo in column_combos:
            tuple_options = set()
            for ccol in combo:
              tuple_options.update(self.rows[row][ccol].options)
            if len(tuple_options) == tuple_size:
              for ucol in range(0,9):
                if ucol not in combo:
                  for opt_val in tuple_options:
                    try:
                      self.rows[row][ucol].options.remove(opt_val)
                      clean = False
                      print("Found values to remove via tuples search in row {row}, restarting".format(row=row))
                    # couldn't remove a non-extant option
                    except KeyError:
                      pass
      return clean

    counter = 1
    while True:
      clean = scan()
      if clean:
        break
      counter += 1
    print("Scanned row_tuples {counter} times.".format(counter=counter))
    return counter-1

  def col_tuples(self):
    """check for column tuples and elimate options in non-tuple cells"""
    def scan():
      clean = True
      for col in range(0,9):
        prows = [row for row in range(0,9) if self.rows[row][col].value is None]
        max_tuple_size = len(prows)
        for tuple_size in range(2,max_tuple_size):
          #  12, 13, 14, 15, 23, 24, 25, 34, 35, 45  
          # itertools.combinations(iterable,length)
          column_combos = list(itertools.combinations(prows,tuple_size))
          #print("column combos for column {col}: {combos}".format(col=col,combos=str(column_combos)))
          # union the options from the pcols together and check if size is == tuple_size
          # ... it shouldn't be able to be smaller than tuple-size, i think...
          for combo in column_combos:
            tuple_options = set()
            for crow in combo:
              tuple_options.update(self.rows[crow][col].options)
            if len(tuple_options) == tuple_size:
              for urow in range(0,9):
                if urow not in combo:
                  for opt_val in tuple_options:
                    try:
                      self.rows[urow][col].options.remove(opt_val)
                      clean = False
                      print("Found values to remove via tuples search in column {col}, restarting".format(col=col))
                    # couldn't remove a non-extant option
                    except KeyError:
                      pass
      return clean

    counter = 1
    while True:
      clean = scan()
      if clean:
        break
      counter += 1
    print("Scanned col_tuples {counter} times.".format(counter=counter))
    return counter-1

  def square_tuples(self):
    """check for square tuples and eliminate options in non-tuple cells"""
    def scan():
      target_cells = [ (0,0),
                       (3,0),
                       (6,0),
                       (0,3),
                       (3,3),
                       (6,3),
                       (0,6),
                       (3,6),
                       (6,6),
                      ]
      clean = True
      for snum,square in enumerate([board.get_squares_cells(*x) for x in target_cells]):
        pcells = [(row,col) for row,col in square if self.rows[row][col].value is None]
        max_tuple_size = len(pcells)
        for tuple_size in range(2,max_tuple_size):
          cell_combos = list(itertools.combinations(pcells,tuple_size))
          for combo in cell_combos:
            tuple_options = set()
            for crow,ccol in combo:
              tuple_options.update(self.rows[crow][ccol].options)
            if len(tuple_options) == tuple_size:
              for urow,ucol in square:
                if (urow,ucol) not in combo:
                  for opt_val in tuple_options:
                    try:
                      self.rows[urow][ucol].options.remove(opt_val)
                      clean = False
                      print("Found values to remove via square search in square {snum} , restarting".format(snum=snum))
                    # couldn't remove a non-extant option
                    except KeyError:
                      pass
      return clean

    counter = 1
    while True:
      clean = scan()
      if clean:
        break
      counter += 1
    print("Scanned square_tuples {counter} times.".format(counter=counter))
    return counter-1

  def partials(self):
    """Search squares for two or three cells in the same row/col that hold the only options for a single value in the square.
    Other cells in that row/col must discard the value in question."""
    def scan():
      target_cells = [ (0,0),
                       (3,0),
                       (6,0),
                       (0,3),
                       (3,3),
                       (6,3),
                       (0,6),
                       (3,6),
                       (6,6),
                      ]
      clean = True
      for snum,square in enumerate([board.get_squares_cells(*x) for x in target_cells]):
        pcells = [(row,col) for row,col in square if self.rows[row][col].value is None]
        opt_set = set()
        for row,col in square:
          opt_set.update(self.rows[row][col].options)

        allowed_cells = {k: [] for k in opt_set}
        for row,col in square:
          opt_vals = self.rows[row][col].options
          for opt_val in opt_vals:
            allowed_cells[opt_val].append((row,col))
        for opt_val in allowed_cells:
          if len(allowed_cells) < 2:
            break
          row_uniq = True if len(set(row for row,col in allowed_cells[opt_val])) == 1 else False
          col_uniq = True if len(set(col for row,col in allowed_cells[opt_val])) == 1 else False
          #print("option: {}, rowuniq: {} coluniq: {}".format(opt_val,row_uniq,col_uniq))
          if row_uniq:
            print("Found row uniq in square {} for value {}. {}".format(snum,opt_val,allowed_cells[opt_val]))
            # delete the opt_val from all cells in this column that are not in allowed_cells
            urow = allowed_cells[opt_val][0][0]
            for ucol in [col for col in range(0,9) if col not in [c for r,c in allowed_cells[opt_val]]]:
              try:
                self.rows[urow][ucol].options.remove(opt_val)
                clean = False
                print("Removed {} from options in cell {}, {}".format(opt_val,urow,ucol))
              except KeyError:
                pass
          if col_uniq:
            # delete the opt_val from all cells in this column that are not in allowed_cells
            print("Found column uniq in square {} for value {}. {}".format(snum,opt_val,allowed_cells[opt_val]))
            ucol = allowed_cells[opt_val][0][1]
            for urow in [row for row in range(0,9) if row not in [r for r,c in allowed_cells[opt_val]]]:
              try:
                self.rows[urow][ucol].options.remove(opt_val)
                clean = False
                print("Removed {} from options in cell {}, {}".format(opt_val,urow,ucol))
              except KeyError:
                pass
      return clean

    counter = 1
    while True:
      clean = scan()
      if clean:
        break
      counter += 1
    print("Scanned partials {counter} times.".format(counter=counter))
    return counter-1

  def scan(self):
    for row in range(0,9):
      for col in range(0,9):
        if self.rows[row][col].value is None:
          print(self.rows[row][col].options)

  def __init__(self):
    self.rows = {k:{j:Cell() for j in range(0,9)} for k in range(0,9)}

  def display(self):
    for x in range(0,9):
      for y in range(0,9):
        print(self.rows[x][y], end=" ")
        if y in [2,5]:
          print("|", end=" ")
      print()
      if x in [2,5]:
        print("-"*(9*2+3))

  def large_display(self):
    for row in range(0,9): # loop for each row
      for subrow in range(0,3): #subrows for options
        line = ["|"]
        for col in range(0,9):
          for opt in range(1,4):
            if (subrow*3)+opt in self.rows[row][col].options:
              line.append(str(subrow*3+opt))
            # if there are no options in the set, the Cell's value is fixed
            # and we should draw a green value in the center square
            # (where the 5 note would be)
            elif (subrow*3+opt == 5) and not self.rows[row][col].options:
              line.append("\x1b[1;32m"+str(self.rows[row][col].value)+"\x1b[0m")
            else:
              line.append(" ")
          if col in [2,5]:
            line.append('\x1b[1;36m|\x1b[0m')
          else:
            line.append("|")
        print("".join(line))
      if row in [2,5]:
        print("\x1b[1;36m"+"="*39+"\x1b[0m")
      else:
        print("-"*39)
      
  def update_cell(self,x,y,value):
    """ This sets the cell to the given value as long as it is blank or
    matches the existing value and also updates options of the row, column
    and square"""
    print("row: "+str(x)+" col: "+str(y)+" curr_value: "+str(self.rows[x][y].value)+" set value: "+str(value))
    if self.rows[x][y].value == value or self.rows[x][y].value is None:
      print("Updating board from {row},{col} set to {value}".format(row=x,col=y,value=value))
      self.rows[x][y].value = value
      self.rows[x][y].options.clear()
      for uy in range(0,9):
        self.rows[x][uy].options.discard(value)
      for ux in range(0,9):
        self.rows[ux][y].options.discard(value)
      sq_cells = self.get_squares_cells(x,y)
      for ux,uy in sq_cells:
        self.rows[ux][uy].options.discard(value)
  
def usage():
  print("Usage: python sudoku.py <puzzle_file>")

if __name__ == "__main__":
  if len(sys.argv) != 2:
    usage()
    sys.exit()

  puzzle_filename = sys.argv[1]

  board = Board()

  board.load_file(puzzle_filename)

  #board.rows[8][8].options.clear()
  #board.rows[8][8].options.add(9)
  def solve():
    while True:
      counter = 0
      counter += board.scan_singles()
      counter += board.scan_rows()
      counter += board.scan_cols()
      counter += board.scan_squares()
      counter += board.row_tuples()
      counter += board.col_tuples()
      counter += board.square_tuples()
      counter += board.partials()
      if counter == 0:
        print("Completed all scans with no changes, giving up")
        break
  solve()
  #board.rows[6][4].options.discard(6)
  #solve()
  board.display()
  board.large_display()
  board.partials()


  """ Write an "option_remove(option_value,row=None,col=None,exclude=[])" function
  that removes the specified option_value in all cells in the given row XOR column
  exclude those in the exlcude list"""
