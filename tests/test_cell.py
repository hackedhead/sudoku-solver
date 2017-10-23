from sudoku import Cell

def test_new_cell_has_all_options_and_no_value():
    cell = Cell()
    assert cell.options == set(range(1,10))
    assert cell.value == None


def test_assigned_cell_has_no_options():
    cell = Cell(8)
    assert cell.options == set()
    assert cell.value == 8


def test_cell_remove_penultimate_option_sets_value():
    cell = Cell()
    for i in range(1,9):
        cell.remove_option(i)
    assert cell.value == 9

def test_setting_cell_value_remove_options():
    cell = Cell()
    cell.set_value(7)
    assert cell.value == 7
    assert cell.options == set()
