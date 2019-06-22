import pytest
from sudoku import Board


def test_board_has_81_cells():
    board = Board()
    assert board[0][0].options == set(range(1, 10))
    assert board[8][8].options == set(range(1, 10))
    with pytest.raises(KeyError):
        assert board[0][9]
    with pytest.raises(KeyError):
        assert board[9][0]

def test_board_errors_loading_string_too_short():
    with pytest.raises(ValueError):
        assert Board("091823098")

def test_board_errors_loading_string_too_long():
    with pytest.raises(ValueError):
        assert Board(82*"X")

def test_board_errors_loading_string_invalid_character():
    with pytest.raises(ValueError):
        assert Board(80*"1" + "A")

def test_board_errors_loading_string_invalid_numeral():
    with pytest.raises(ValueError):
        assert Board(80*"1" + "0")

def test_valid_string_becomes_board():
    board = Board("123456789" + ("X" * 9) * 8)
    assert board[0][2].value == 3
    assert board[0][8].value == 9
    assert board[1][5].value == None

