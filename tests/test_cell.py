from sudoku import Cell

def test_new_cell_has_all_options_and_no_value():
    cell = Cell()
    assert cell.options == set(range(1,10))
    assert cell.value == None


def test_assigned_cell_has_no_options():
    cell = Cell(8)
    assert cell.options == set()
    assert cell.value == 8

def test_setting_cell_value_remove_options():
    cell = Cell()
    cell.set_value(7)
    assert cell.value == 7
    assert cell.options == set()
