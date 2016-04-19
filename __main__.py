from copy import copy

from abstract_heuristic import DummyHeuristic
from node import *
from reversi_client import *
from searcher import *


class ReversiClient(PlayReversi):
    map_function = {
        -1: 0,
        1: 1,
        2: -1
    }

    _searcher = None
    _player = 1

    def __init__(self, searcher, player):
        super(ReversiClient, self).__init__()
        self._searcher = searcher
        self._player = player

    def make_a_move(self, updated_board):
        board = copy(updated_board)
        for i in xrange(8):
            for j in xrange(8):
                temp = board[i][j]
                board[i][j] = self.map_function[temp]
        current_node = Node(board)
        heuristic, move = self._searcher.search(current_node, 4, self._player)
        return {'X': move[1], 'Y': move[0]}

    def update_board(self, updated_board):
        print updated_board.__str__()
        super(ReversiClient, self).update_board(updated_board)


if __name__ == "__main__":
    heuristic = DummyHeuristic()
    begin = Node.create()
    searcher = MinMaxSearcher(heuristic)
    handler = ReversiClient(searcher, -1)
    play(handler)
