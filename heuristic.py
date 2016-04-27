from abstract_heuristic import *


class heuristic(AbstractHeuristic):

    def isSafe(self, node, x, y):
        """
        :param: x,y : position in node board
        :return: False if player at x,y is can be eaten by opponent
                 True if not
        """
        player = node.board[x][y]
        opponent = - player
        # empty position
        if player == 0:
            return True
        # in corner
        if x == 0 and y == 0:
            return True
        if x == 0 and y == 7:
            return True
        if x == 7 and y == 0:
            return True
        if x == 7 and y == 7:
            return True

        # check row
        b_safe = False
        is_opp_in_left = False
        # check left
        for i in range(x - 1, 0, -1):
            if node.board[i][y] != player:
                if node.board[i][y] == opponent: is_opp_in_left = True
                break
            if (i == 0): b_safe = True
        if not b_safe:
            for i in range(x + 1, 7, 1):
                if node.board[i][y] != player:
                    if node.board[i][y] == opponent:
                        if not is_opp_in_left: return False # opponent can eat this if choose in the left
                    if node.board[i][y] == 0:
                        if is_opp_in_left: return False # opponent can eat this if choose in the right
                    break
        # check column
        b_safe = False
        is_opp_in_top = False
        for i in range(y - 1, 0, -1):
            if node.board[x][i] != player:
                if node.board[x][i] == opponent: is_opp_in_top = True
                break
            if i == 0: b_safe = True
        if not b_safe:
            for i in range(y + 1, 7, 1):
                if node.board[x][i] != player:
                    if node.board[x][i] == opponent:
                        if not is_opp_in_top: return False  # opponent can eat this if choose in the left
                    if node.board[x][i] == 0:
                        if is_opp_in_top: return False  # opponent can eat this if choose in the right
                    break
        # check the cross left top 2 right down
        la = 0
        ra = 0
        if x < y:
            la = x
            ra = 7 - y
        else:
            la = y
            ra = 7 - x
        b_safe = False
        is_opp_in_top = False
        for i in range(1, la + 1, 1):
            if node.board[x - i][y - i] != player:
                if node.board[x - i][y - i] == opponent: is_opp_in_top = True
                break
            if i == la:
                b_safe = True
        if not b_safe:
            for i in range(1, ra + 1, 1):
                if node.board[x + i][y + i] != player:
                    if node.board[x + i][y + i] == opponent:
                        if not is_opp_in_top:
                            return False  # opponent can eat this if choose in the left up
                    if node.board[x + i][y + i] == 0:
                        if is_opp_in_top:
                            return False  # opponent can eat this if choose in the right down
                    break
        # check the cross right top 2 left down
        if x < 7 - y:
            la = x
            ra = y
        else:
            la = 7 - y
            ra = 7 - x
        b_safe = False
        is_opp_in_top = False
        for i in range(1, la + 1, 1):
            if node.board[x - i][y + i] != player:
                if node.board[x - i][y + i] == opponent: is_opp_in_top = True
                break
            if i == la:
                b_safe = True
        if not b_safe:
            for i in range(1, ra + 1, 1):
                if node.board[x + i][y - i] != player:
                    if node.board[x + i][y - i] == opponent:
                        if not is_opp_in_top: return False  # opponent can eat this if choose in the left down
                    if node.board[x + i][y - i] == 0:
                        if is_opp_in_top: return False  # opponent can eat this if choose in the right up
                    break
        return True

    def eval_early_game(self, node):
        """ return the score of a node in early game"""
        point_board = [[10, 1, 3, 2, 2, 3, 1, 10],
                       [ 1, 1, 2, 2, 2, 2, 1, 1],
                       [ 3, 2, 4, 2, 2, 4, 2, 3],
                       [ 2, 2, 2, 2, 2, 2, 2, 2],
                       [ 2, 2, 2, 2, 2, 2, 2, 2],
                       [ 3, 2, 4, 2, 2, 4, 2, 3],
                       [ 1, 1, 2, 2, 2, 2, 1, 1],
                       [10, 1, 3, 2, 2, 3, 1, 10]]
        res = 0
        for i in range(8):
            for j in range(8):
                res += point_board[i][j]*node.board[i][j]
        return res

    def eval_mid_game(self, node):
        """ return the score of a node in mid game"""
        my_safe = 0
        my_not_safe = 0
        opp_safe = 0
        opp_not_safe = 0
        player = Node.PLAYER_1
        #opponent = Node.PLAYER_2
        # calculate the num of safe-chess, not safe-chess of mine and opponent's
        for i in range(8):
            for j in range(8):
                if node.board[i][j] != 0:
                    if self.isSafe(node, i, j):
                        if node.board[i][j] == player:
                            my_safe += 1  # = my_safe + 1
                        else:
                            opp_safe += 1  # = opp_safe + 1
                    else:
                        if node.board[i][j] == player:
                            my_not_safe += 1  # = my_not_safe + 1
                        else:
                            opp_not_safe += 1  # = opp_not_safe + 1
        res = 2*my_safe + my_not_safe - 2*opp_safe - opp_not_safe
        return res

    def eval_late_game(self, node):
        """ return the score of a node in late game
        We: Player_1
        Opp: Player-2
        """
        return node.get_score(node.PLAYER_1) - node.get_score(node.PLAYER_2)

    def eval(self, node):
        n = node.get_score(node.PLAYER_1) + node.get_score(node.PLAYER_2)
        if n < 30:
            return self.eval_early_game(node)
        elif n < 55:
            return self.eval_mid_game(node)
        else:
            return self.eval_late_game(node)

class _heuristic():
    def get_checking_path_value(self, node, start_x, start_y, end_x, end_y, roc, player):
        flag = True
        beside = True
        point = 1;
        if start_x < 0 or start_x >= 8 or start_y < 0 or start_y >= 8:
            return 0
        if roc:
            if start_x == end_x:
                j = start_y
                if end_y == 0:
                    while True:
                        if node.board[start_x][j] == 0:
                            break
                        if j - 1 < 0 or node.board[start_x][j] == player:
                            flag = False
                            break
                        point += 1
                        j -= 1
                        beside = False
                elif end_y == 7:
                    while True:
                        if node.board[start_x][j] == 0:
                            break
                        if j + 1 >= 8 or node.board[start_x][j] == player:
                            flag = False
                            break
                        point += 1
                        j += 1
                        beside = False
            elif start_y == end_y:
                i = start_x
                if end_x == 0:
                    while True:
                        if node.board[i][start_y] == 0:
                            break
                        if i - 1 < 0 or node.board[i][start_y] == player:
                            flag = False
                            break
                        point += 1
                        i -= 1
                        beside = False
                elif end_x == 7:
                    while True:
                        if node.board[i][start_y] == 0:
                            break
                        if i + 1 >= 8 or node.board[i][start_y] == player:
                            flag = False
                            break
                        point += 1
                        i += 1
                        beside = False
        else:
            x = 0
            y = 0
            if end_x == 0 and end_y == 0:
                x = -1
                y = -1
            elif end_x == 7 and end_y == 0:
                x = 1
                y = -1
            elif end_x == 7 and end_y == 7:
                x = 1
                y = 1
            elif end_x == 0 and end_y == 7:
                x = -1
                y = 1
            else:
                return 0
            i = start_x
            j = start_y

            while True:
                if node.board[i][j] == 0:
                    break
                if (i - 1 < 0 or i + 1 >= 8) or (j - 1 < 0 or j + 1 >= 8) or node.board[i][j] == player:
                    flag = False
                    break
                point += 1
                i += x
                j += y
                beside = False

        if flag == True and beside == False:
            return point
        else:
            return 0


    def get_value_of_men(self, node, player):
        """Evaluate value of a chessman based on number of opponent's chessman around him [0-8]"""

        point_sum = 0

        for i in xrange(8):
            for j in xrange(8):
                if node.board[i][j] == player:
                    point = 0
                    # Check PLAYER_1's chessman
                    # Check 8 path - left - right - bottom - top and 4 diagonals
                    point += self.get_checking_path_value(node, i, j - 1, i, 0, True, player)
                    point += self.get_checking_path_value(node, i, j + 1, i, 7, True, player)
                    point += self.get_checking_path_value(node, i - 1, j, 0, j, True, player)
                    point += self.get_checking_path_value(node, i + 1, j, 7, j, True, player)
                    point += self.get_checking_path_value(node, i - 1, j - 1, 0, 0, False, player)
                    point += self.get_checking_path_value(node, i - 1, j + 1, 0, 7, False, player)
                    point += self.get_checking_path_value(node, i + 1, j + 1, 7, 7, False, player)
                    point += self.get_checking_path_value(node, i + 1, j - 1, 7, 0, False, player)
                    # Add point into point_sum
                    point_sum += point
        return point_sum
