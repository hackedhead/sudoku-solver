from sudoku import Solver


def test_set_cell_value_clears_option_from_row_cells():
    solver = Solver()
    solver.set((1, 6), 5)
    for cell in [solver.board[1][i] for i in range(0, 9)]:
        if i != 6:
            assert 5 not in cell.options
        else:
            assert cell.value == 6
            assert cell.options == set()
