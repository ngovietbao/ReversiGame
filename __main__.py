from copy import copy

from heuristic import *
from reversi_client import *
from searcher import *

class ReversiClient(PlayReversi):
    map_function = {
        -1: 0,
        2: 1,
        1: -1
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
        heuristic, move = self._searcher.search(current_node, 5, 1)
        print move
        return {'X': move[1], 'Y': move[0]}

    def update_board(self, updated_board):
        print (updated_board.__str__())
        super(ReversiClient, self).update_board(updated_board)


from node_advance import *
if __name__ == "__main__":
    heuristic = DummyHeuristic()
    # heuristic = heuristic()
    begin = BitBoard(None)
    searcher = AlplaBetaSearcher(heuristic)
    searcher.search(begin, 13, 1)
    # handler = ReversiClient(searcher, -1)
    #play(handler)
