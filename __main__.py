from copy import copy, deepcopy


class Node(object):
    def __init__(self, board, parent=None):
        """ Constructor for node class """
        self.board = deepcopy(board)
        self.parent = parent

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        """"""
        hash = [None] * 8
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

    def _oppose(self, player, x, y):
        return self.board[x][y] != 0 and self.board[x][y] != player

    def validMove(self, player, x, y):
        # Check valid turn
        if player != 1 and player != 2:
            return False
        if x < 0 or x >= 8 or y < 0 or y >= 8 or self.board[x][y] != 0:
            return False

        lleft, lright, lup, ldown = False, False, False, False
        # Check can slip left
        if y > 1 or self._oppose(player, x, y - 1):
            surround = False
            for j in xrange(y - 1, 0, -1):
                if self.board[x][j] == 0:
                    break
                if self.board[x][j] == player:
                    surround = True
                    break
            if surround:
                lleft = True

        # Check can slip right
        if y < 7 or self._oppose(player, x, y + 1):
            surround = False
            for j in xrange(y + 1, 7):
                if self.board[x][j] == 0:
                    break
                if self.board[x][j] == player:
                    surround = True
                    break
            if surround:
                lright = True

        # Check can slip Up
        if x > 1 or self._oppose(player, x - 1, y):
            surround = False
            for j in xrange(x - 1, 0, -1):
                if self.board[j][y] == 0:
                    break
                if self.board[j][y] == player:
                    surround = True
                    break
            if surround:
                lup = True

        # Check can slip down
        if x < 7 or self._oppose(player, x + 1, y):
            surround = False
            for j in xrange(x + 1, 7):
                if self.board[j][y] == 0:
                    break
                if self.board[j][y] == player:
                    surround = True
                    break
            if surround:
                ldown = True

        # Check can slip down
        if x < 7 or self._oppose(player, x + 1, y):
            surround = False
            for j in xrange(x + 1, 7):
                if self.board[j][y] == 0:
                    break
                if self.board[j][y] == player:
                    surround = True
                    break
            if surround:
                ldown = True
        return True


if __name__ == "__main__":
    print "Hello world"
    node = Node.create()

    node2 = Node.create()
    print node == node2
    print node
    print 'hash code = ', node.__hash__()
    print 'hash code 2  = ', node2.__hash__()
