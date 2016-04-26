from time import *

from node import Node

# Declare const
C_PLAYER1, C_PLAYER2 = 1, -1
shift_left_mask = -9187201950435737472
shift_right_mask = 72340172838076673

inv_slm = ~shift_left_mask
inv_srm = ~shift_right_mask


def shift_left(position):
    return (position >> 1) & inv_slm


def shift_right(position):
    return (position << 1) & inv_srm


def shift_down(position):
    return position >> 8


def shift_up(position):
    return position << 8


def shift_left_up(position):
    return ((position >> 1) & inv_slm) << 8


def shift_left_down(position):
    return ((position >> 1) & inv_slm) >> 8


def shift_right_up(position):
    return ((position << 1) & inv_srm) << 8


def shift_right_down(position):
    return ((position << 1) & inv_srm) >> 8


direction = {
    'UPP': shift_up,
    'DOW': shift_down,
    'LEF': shift_left,
    'RIG': shift_right,
    'LUP': shift_left_up,
    'LDO': shift_left_down,
    'RUP': shift_right_up,
    'RDO': shift_right_down
}

inv_direction = {
    'UPP': shift_down,
    'DOW': shift_up,
    'LEF': shift_right,
    'RIG': shift_left,
    'LUP': shift_right_down,
    'LDO': shift_right_up,
    'RUP': shift_left_down,
    'RDO': shift_left_up
}


def dilation(bits, d=None, is_inverted=False):
    if d is not None:
        if is_inverted:
            return inv_direction[d](bits)
        else:
            return direction[d](bits)
    else:
        return bits | shift_up(bits) | shift_down(bits) | \
               shift_left(bits) | shift_right(bits) | \
               shift_left_down(bits) | shift_left_up(bits) | \
               shift_right_up(bits) | shift_right_down(bits)


class BitBoard(Node):
    bitboard = {
        # 0x00\00\00\08\10\00\00\00
        C_PLAYER1: 0x0000000810000000,
        C_PLAYER2: 0x0000001008000000
    }

    def __position(self, row, col):
        return 1 << (row * 8 + col)

    def __set_at(self, pos, player):
        self.bitboard[player] = (self.bitboard[player] & ~pos) | pos

    def __get_at(self, pos, player):
        return self.bitboard[player] & pos

    def __init__(self, board):
        super(BitBoard, self).__init__(board)

    def get_all_valid_moves(self, player):
        moves = {}
        empty = ~(self.bitboard[C_PLAYER1] | self.bitboard[C_PLAYER2])
        for d in direction.keys():
            dmove = 0
            candidates = self.bitboard[-player] & dilation(self.bitboard[player], d)
            while candidates != 0:
                dmove |= empty & dilation(candidates, d)
                candidates = self.bitboard[-player] & dilation(candidates, d)
            moves[d] = dmove
        all_candidate_moves = {}
        for keys, values in moves.iteritems():
            if values != 0:
                # Select a random valid move
                # Try
                bit2xy = self.__to_x_y(values)
                for valid_move in bit2xy:
                    x, y = valid_move[0], valid_move[1]
                    flipped_square = self.__generate_flipped_squares(1 << (x * 8 + y), keys, player)
                    bstr = self.__gererate_new_board(flipped_square, player)
                    new_board = BitBoard(None)
                    new_board.bitboard = bstr
                    all_candidate_moves[(x, y)] = new_board

        return all_candidate_moves

    def __to_x_y(self, board):
        to_x_y = []
        for i in xrange(0, 64, 8):
            temp = board >> i & 0xFF
            if temp != 0:
                for j in xrange(8):
                    valid = temp & 1
                    temp >>= 1
                    if valid != 0:
                        to_x_y.append((i / 8, j))
        return to_x_y

    def __generate_flipped_squares(self, move, dir, player):
        flipped_bit = move
        is_end = 0xFFFFFFFFFFFFFFFF
        while is_end != 0:
            move = dilation(move, dir, True)
            is_end = move & self.bitboard[player]
            flipped_bit |= move
        return flipped_bit

    def __gererate_new_board(self, flipped_squares, player):
        new_board = {C_PLAYER1: self.bitboard[C_PLAYER1], C_PLAYER2: self.bitboard[C_PLAYER2]}

        # Add to player bitboard
        new_board[player] |= flipped_squares
        # Clear opponent
        new_board[-player] &= ~flipped_squares
        return new_board

    def __str__(self):
        tostring = ""
        for i in xrange(8):
            for j in xrange(8):
                pos = self.__position(i, j)
                if self.__get_at(pos, C_PLAYER1) | self.__get_at(pos, C_PLAYER2) != 0:
                    tostring += '1'
                else:
                    tostring += '0'
            tostring += '\n'
        return tostring


def bitboard_tostring(bits):
    seq = '\n'
    tostring = seq.join(["{0:08b}".format(bits >> (i * 8) & 0xFF) for i in range(8)])
    return tostring


save_board = []


def anlysis(node, depth, player):
    if depth <= 0:
        save_board.append(node)
        return
    lst = node.get_all_valid_moves(player)

    for k, v in lst.iteritems():
        # print k
        anlysis(v, depth - 1, -player)


if __name__ == "__main__":
    print "Unit test for bitboard"
    bb = BitBoard(None)
    # print bb
    nb = Node.create()
    start_time = 0
    for i in xrange(10):
        start_time = time()
        if i <= 7:
            anlysis(nb, i, 1)
        end_time = time()
        estimate1 = end_time - start_time
        start_time = time()
        anlysis(bb, i, 1)
        end_time = time()
        estimate2 = end_time - start_time
        print 'Depth = ', i, '\t', estimate1, '---------------------\t', estimate2
    if bb.bitboard[1] == bb.bitboard[1] and \
                    bb.bitboard[-1] == bb.bitboard[-1]:
        print 'OK'
    anlysis(bb, 7, 1)
    """
    dup = 0
    check = {}
    for i in xrange(len(save_board)):
        c = 0
        for j in xrange(i+1, len(save_board)):
            if save_board[i].bitboard[1] == save_board[j].bitboard[1] and \
                save_board[i].bitboard[-1] == save_board[j].bitboard[-1] and not check.has_key(j):
                check[j] = 1
                dup +=1



    print dup
    """
    """
    print 'K'
    fst = bb.get_all_valid_moves(1)
    for k, v in fst.iteritems():
        nn = v.get_all_valid_moves(-1)
        for k1, v1 in nn.iteritems():
            aa = v1.get_all_valid_moves(1)
            #print bitboard_tostring(v1.bitboard[-1])
            print bitboard_tostring(v1.bitboard[1]), '\n'
            print bitboard_tostring(v1.bitboard[-1]), '\n'
            for k2, v2 in aa.iteritems():
                print bitboard_tostring(v2.bitboard[1]), '\n'
                print bitboard_tostring(v2.bitboard[-1]), '\n'
                break
            print '~~~~'
            break

        print 'End'
        break
    """
