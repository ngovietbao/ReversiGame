class AbstractSearcher:
    """ Lop truu tuong cu cac lop tim kiem"""
    _heuristic = None

    def __init__(self, heuristic):
        """Initialize seacher"""
        self._heuristic = heuristic

    def set_heuristic(self, h):
        self._heuristic = h

    def get_heuristic_value(self, node):
        """
        :param node: a node you want to get its static value
        :return: a real number value
        """
        return self._heuristic.eval(node)

    def search(self, node, depth, player):
        """Find a next best node in a list valid node
            :param: node current state of the game
            :return: next step if there a valid next move
                     Node if there no valid move
        """
        pass


class MinMaxSearcher(AbstractSearcher):
    def search(self, node, depth, player):
        """
        Implementation min-max algorithm
        :param node: Node
        :param depth: Depth of search
        :param player: Current player
        :return: a pair of best node and value
        """

        if depth <= 0:
            return self.get_heuristic_value(node), None

        # Get all node can be of current node
        valid_moves = node.get_all_valid_moves(player)
        lst = [i for i in valid_moves.values()]

        # Get max value of child node
        max, moving = -165, None
        for mov, new_node in valid_moves.iteritems():
            # print 2 test
            #print mov
            #print(' has child: ')
            # aaa
            result = self.search(new_node, depth - 1, -player)
            value = player * result[0]  # Value of this node
            #print mov
            #print value
            if value >= max:
                max, moving = value, mov
        # Get how to move return this node
        #print(max)
        #print(moving)
        return max * player, moving


class AlplaBetaSearcher(AbstractSearcher):
    def search(self, node, depth, alpha, beta, player):
        """Tim theo giai thuat  minmax"""
        if depth <= 0:
            return self.get_heuristic_value(node), None

        valid_moves = node.get_all_valid_moves(player)

        if len(valid_moves) is 0:
            return self.get_heuristic_value(node), None

        best_value, best_move = -1000, None
        for mov, new_node in valid_moves.iteritems():
            result = self.search(new_node, depth-1, -beta, -alpha, -player)
            value = player * result[0]  # Value of this node
            if value > best_value:
                best_value, best_move = value, mov
            alpha = max (value, alpha)
            if alpha >= beta:
                break

        return best_value * player, best_move


class AlphaBetaWidthIterativeDeepening(AbstractSearcher):
    def search(self, node, depth, player):
        """Giai thuat alpla-beta cai tien"""
        # TODO: Alpha-beta improve
        pass
