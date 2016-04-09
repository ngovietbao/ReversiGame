from copy import copy, deepcopy


class Node(object):
    'This is class declare a state of game Reversi'

    __player1 = 0
    __player2 = 0
    __is_player1_turn = True

    def __init__(self, board, parent=None):
        """ Constructor for node class """
        self.board = deepcopy(board)
        self.parent = parent

    def __eq__(self, other):
        """Implement fast compare two state is equal or not"""
        return self.board == other.board

    def __hash__(self):
        """Hash function"""
        hash = [0] * 8
        hashcode = 0
        for i in xrange(0, 7):
            current = 0
            for j in xrange(0, 7):
                current |= self.board[i][j] << 4 * j
            hash[i] = current
            hashcode |= hash[i] << 4 * i

        return hashcode

    def __str__(self):
        tostring = "\n".join([str(i) for i in self.board])
        return tostring

    def isValidMove(self, player, x, y):
        """Return true if move is valid"""
        # TODO: Implement here
        pass

    def getAllValidMove(self):
        """Return a list of valid move"""
        # TODO: Get all valid move and return it.
        pass

    def getNumberValidMove(self):
        # TODO: Get number valid move
        pass

    def getScore(self, player):
        # TODO: Return current score of @player
        pass

    def getTurn(self):
        if self.__is_player1_turn:
            return 1
        else:
            return 2

    @staticmethod
    def create():
        """Create begin board value
        """
        board = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 2, 0, 0, 0],
            [0, 0, 0, 2, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
        initnode = Node(board)

        return initnode
