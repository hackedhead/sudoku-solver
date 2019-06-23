from sudoku import Cell
import pytest


def test_new_cell_has_all_options_and_no_value():
    cell = Cell()
    assert cell.options == set(range(1, 10))
    assert cell.value is None


def test_assigned_cell_has_no_options():
    cell = Cell(8)
    assert cell.options == set()
    assert cell.value == 8


def test_setting_cell_value_remove_options():
    cell = Cell()
    cell.set_value(7)
    assert cell.value == 7
    assert cell.options == set()


def test_removing_last_cell_option_errors():
    cell = Cell()
    for value in range(1, 9):
        cell.remove_option(value)
    with pytest.raises(AttributeError):
        assert cell.remove_option(9)
