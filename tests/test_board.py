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
