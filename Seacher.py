class AbstractSearcher:
    """ Lop truu tuong cu cac lop tim kiem"""
    __heuristic = None

    def __init__(self):
        """Initialize seacher"""
        print "Create searcher"

    def setHeuristic(self, h):
        self.__heuristic = h

    def search(self, node):
        """Find a next best node in a list valid node
            :param: node current state of the game
            :return: next step if there a valid next move
                     Node if there no valid move
        """

        pass


class MinMaxSearcher(AbstractSearcher):
    def search(self, node):
        """Tim theo giai thuat  minmax"""
        # TODO: Minmax
        pass


class AlplaBetaSearcher(AbstractSearcher):
    def search(self, node):
        """Tim theo giai thuat alpha-beta"""
        # TODO: Alpha-beta
        pass


class AlphaBetaWidthIterativeDeepening(AbstractSearcher):
    def search(self, node):
        """Giai thuat alpla-beta cai tien"""
        # TODO: Alpha-beta improve
        pass
