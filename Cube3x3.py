import random
import twophase.solver as sv


class Cube3x3:

    """
    http://www.rubiksplace.com/move-notations/
    U:Up,    F:Front, R:Right, B:Back, L:Left,   D:Down
    w:white, g:green, r:red,   b:blue, o:orange, y:yellow

            UUU                www
            UUU                www
            UUU                www
        LLL FFF RRR BBB    ooo ggg rrr bbb
        LLL FFF RRR BBB    ooo ggg rrr bbb
        LLL FFF RRR BBB    ooo ggg rrr bbb
            DDD                yyy
            DDD                yyy
            DDD                yyy
    """

    class CornerBlock:

        def __init__(self, colors='', orientation=0):

            """
            A corner block of the cube.\n
            :param colors: 3-character string, colors of this block
            :param orientation: between 0~2, white or yellow relative to up or down
            """

            self.colors = colors
            self.orientation = orientation

        def assign(self, other):
            self.colors = other.colors[0] + other.colors[1] + other.colors[2]
            self.orientation = other.orientation

    class EdgeBlock:

        def __init__(self, colors='', orientation=0):

            """
            An edge block of the cube.\n
            :param colors: 2-character string, colors of this block
            :param orientation: between 0~1
            """

            self.colors = colors
            self.orientation = orientation

        def assign(self, other):
            self.colors = other.colors[0] + other.colors[1]
            self.orientation = other.orientation

    def __init__(self, color_str=''):

        """
        :param color_str: 54-character string (optional)
        """

        self.centers = {'u': 'w', 'l': 'o', 'f': 'g', 'r': 'r', 'b': 'b', 'd': 'y'}

        self.corner_blocks = [self.CornerBlock('wrg', 0),  # up-right-front
                              self.CornerBlock('wgo', 0),  # up-front-left
                              self.CornerBlock('wbr', 0),  # up-back-right
                              self.CornerBlock('wob', 0),  # up-left-back
                              self.CornerBlock('ygr', 0),  # down-front-right
                              self.CornerBlock('yog', 0),  # down-left-front
                              self.CornerBlock('yrb', 0),  # down-right-back
                              self.CornerBlock('ybo', 0)]  # down-back-left

        self.edge_blocks = [self.EdgeBlock('wg', 0),  # up-front
                            self.EdgeBlock('wo', 0),  # up-left
                            self.EdgeBlock('wr', 0),  # up-right
                            self.EdgeBlock('wb', 0),  # up-back
                            self.EdgeBlock('gr', 0),  # front-right
                            self.EdgeBlock('go', 0),  # front-left
                            self.EdgeBlock('br', 0),  # back-right
                            self.EdgeBlock('bo', 0),  # back-left
                            self.EdgeBlock('yg', 0),  # down-front
                            self.EdgeBlock('yo', 0),  # down-left
                            self.EdgeBlock('yr', 0),  # down-right
                            self.EdgeBlock('yb', 0)]  # down-back

        try:
            if len(color_str) == 0:
                pass
            elif len(color_str) == 54:
                self.centers['u'] = color_str[ 4]
                self.centers['l'] = color_str[13]
                self.centers['f'] = color_str[22]
                self.centers['r'] = color_str[31]
                self.centers['b'] = color_str[40]
                self.centers['d'] = color_str[49]
                self.corner_blocks[0].colors = color_str[ 8] + color_str[27] + color_str[20]
                self.corner_blocks[1].colors = color_str[ 6] + color_str[18] + color_str[11]
                self.corner_blocks[2].colors = color_str[ 2] + color_str[36] + color_str[29]
                self.corner_blocks[3].colors = color_str[ 0] + color_str[ 9] + color_str[38]
                self.corner_blocks[4].colors = color_str[47] + color_str[26] + color_str[33]
                self.corner_blocks[5].colors = color_str[45] + color_str[17] + color_str[24]
                self.corner_blocks[6].colors = color_str[53] + color_str[35] + color_str[42]
                self.corner_blocks[7].colors = color_str[51] + color_str[44] + color_str[15]
                self.edge_blocks[  0].colors = color_str[ 7] + color_str[19]
                self.edge_blocks[  1].colors = color_str[ 3] + color_str[10]
                self.edge_blocks[  2].colors = color_str[ 5] + color_str[28]
                self.edge_blocks[  3].colors = color_str[ 1] + color_str[37]
                self.edge_blocks[  4].colors = color_str[23] + color_str[30]
                self.edge_blocks[  5].colors = color_str[21] + color_str[14]
                self.edge_blocks[  6].colors = color_str[39] + color_str[32]
                self.edge_blocks[  7].colors = color_str[41] + color_str[12]
                self.edge_blocks[  8].colors = color_str[46] + color_str[25]
                self.edge_blocks[  9].colors = color_str[48] + color_str[16]
                self.edge_blocks[ 10].colors = color_str[50] + color_str[34]
                self.edge_blocks[ 11].colors = color_str[52] + color_str[43]

                # reset corner blocks' color and orientation
                for block in self.corner_blocks:
                    if block.colors[0] == self.centers['u'] or block.colors[0] == self.centers['d']:
                        continue
                    while block.colors[0] != self.centers['u'] and block.colors[0] != self.centers['d']:
                        block.colors = block.colors[1:] + block.colors[:1]
                        block.orientation = (block.orientation + 2) % 3

                # reset edge blocks' color and orientation
                for block in self.edge_blocks:
                    if block.colors[0] == self.centers['u'] or block.colors[0] == self.centers['d']:
                        continue
                    elif block.colors[0] == self.centers['f'] or block.colors[0] == self.centers['b']:
                        if block.colors[1] == self.centers['u'] or block.colors[1] == self.centers['d']:
                            block.colors = block.colors[1] + block.colors[0]
                            block.orientation = (block.orientation + 1) % 2
                        else:
                            continue
                    else:
                        block.colors = block.colors[1] + block.colors[0]
                        block.orientation = (block.orientation + 1) % 2

            else:
                raise ValueError('Parameter of cube must be nothing or a 54-character string')
        except ValueError as err:
            print('Incorrect input: {}'.format(err))

    def __repr__(self):
        result = '    '
        # up
        result += self.corner_blocks[3].colors[self.corner_blocks[3].orientation]
        result += self.edge_blocks[3].colors[self.edge_blocks[3].orientation]
        result += self.corner_blocks[2].colors[self.corner_blocks[2].orientation] + '\n    '
        result += self.edge_blocks[1].colors[self.edge_blocks[1].orientation]
        result += self.centers['u']
        result += self.edge_blocks[2].colors[self.edge_blocks[2].orientation] + '\n    '
        result += self.corner_blocks[1].colors[self.corner_blocks[1].orientation]
        result += self.edge_blocks[0].colors[self.edge_blocks[0].orientation]
        result += self.corner_blocks[0].colors[self.corner_blocks[0].orientation] + '\n'
        # left -> front -> right -> back
        result += self.corner_blocks[3].colors[(1 + self.corner_blocks[3].orientation) % 3]
        result += self.edge_blocks[1].colors[(1 + self.edge_blocks[1].orientation) % 2]
        result += self.corner_blocks[1].colors[(2 + self.corner_blocks[1].orientation) % 3] + ' '
        result += self.corner_blocks[1].colors[(1 + self.corner_blocks[1].orientation) % 3]
        result += self.edge_blocks[0].colors[(1 + self.edge_blocks[0].orientation) % 2]
        result += self.corner_blocks[0].colors[(2 + self.corner_blocks[0].orientation) % 3] + ' '
        result += self.corner_blocks[0].colors[(1 + self.corner_blocks[0].orientation) % 3]
        result += self.edge_blocks[2].colors[(1 + self.edge_blocks[2].orientation) % 2]
        result += self.corner_blocks[2].colors[(2 + self.corner_blocks[2].orientation) % 3] + ' '
        result += self.corner_blocks[2].colors[(1 + self.corner_blocks[2].orientation) % 3]
        result += self.edge_blocks[3].colors[(1 + self.edge_blocks[3].orientation) % 2]
        result += self.corner_blocks[3].colors[(2 + self.corner_blocks[3].orientation) % 3] + '\n'
        result += self.edge_blocks[7].colors[(1 + self.edge_blocks[7].orientation) % 2]
        result += self.centers['l']
        result += self.edge_blocks[5].colors[(1 + self.edge_blocks[5].orientation) % 2] + ' '
        result += self.edge_blocks[5].colors[self.edge_blocks[5].orientation]
        result += self.centers['f']
        result += self.edge_blocks[4].colors[self.edge_blocks[4].orientation] + ' '
        result += self.edge_blocks[4].colors[(1 + self.edge_blocks[4].orientation) % 2]
        result += self.centers['r']
        result += self.edge_blocks[6].colors[(1 + self.edge_blocks[6].orientation) % 2] + ' '
        result += self.edge_blocks[6].colors[self.edge_blocks[6].orientation]
        result += self.centers['b']
        result += self.edge_blocks[7].colors[self.edge_blocks[7].orientation] + '\n'
        result += self.corner_blocks[7].colors[(2 + self.corner_blocks[7].orientation) % 3]
        result += self.edge_blocks[9].colors[(1 + self.edge_blocks[9].orientation) % 2]
        result += self.corner_blocks[5].colors[(1 + self.corner_blocks[5].orientation) % 3] + ' '
        result += self.corner_blocks[5].colors[(2 + self.corner_blocks[5].orientation) % 3]
        result += self.edge_blocks[8].colors[(1 + self.edge_blocks[8].orientation) % 2]
        result += self.corner_blocks[4].colors[(1 + self.corner_blocks[4].orientation) % 3] + ' '
        result += self.corner_blocks[4].colors[(2 + self.corner_blocks[4].orientation) % 3]
        result += self.edge_blocks[10].colors[(1 + self.edge_blocks[10].orientation) % 2]
        result += self.corner_blocks[6].colors[(1 + self.corner_blocks[6].orientation) % 3] + ' '
        result += self.corner_blocks[6].colors[(2 + self.corner_blocks[6].orientation) % 3]
        result += self.edge_blocks[11].colors[(1 + self.edge_blocks[11].orientation) % 2]
        result += self.corner_blocks[7].colors[(1 + self.corner_blocks[7].orientation) % 3] + '\n    '
        # down
        result += self.corner_blocks[5].colors[self.corner_blocks[5].orientation]
        result += self.edge_blocks[8].colors[self.edge_blocks[8].orientation]
        result += self.corner_blocks[4].colors[self.corner_blocks[4].orientation] + '\n    '
        result += self.edge_blocks[9].colors[self.edge_blocks[9].orientation]
        result += self.centers['d']
        result += self.edge_blocks[10].colors[self.edge_blocks[10].orientation] + '\n    '
        result += self.corner_blocks[7].colors[self.corner_blocks[7].orientation]
        result += self.edge_blocks[11].colors[self.edge_blocks[11].orientation]
        result += self.corner_blocks[6].colors[self.corner_blocks[6].orientation]
        return result

    def move(self, notation):

        """
        :param notation: 2-character string: 'U1', 'U2', 'U3', 'L1', ... , 'D2', 'D3'
        """

        try:
            side = notation[0]
            if side not in ['U', 'L', 'F', 'R', 'B', 'D']:
                raise ValueError('First character of notation should be U, L, F, R, B, or D')
            step = int(notation[1])
        except ValueError as err:
            print('Incorrect input: {}'.format(err))
            return

        temp_corner = self.CornerBlock()
        temp_edge = self.EdgeBlock()

        if side == 'U':
            for _ in range(step):
                # rotate corner blocks
                temp_corner.assign(self.corner_blocks[2])
                self.corner_blocks[2].assign(self.corner_blocks[3])
                self.corner_blocks[3].assign(self.corner_blocks[1])
                self.corner_blocks[1].assign(self.corner_blocks[0])
                self.corner_blocks[0].assign(temp_corner)
                # rotate edge blocks
                temp_edge.assign(self.edge_blocks[2])
                self.edge_blocks[2].assign(self.edge_blocks[3])
                self.edge_blocks[3].assign(self.edge_blocks[1])
                self.edge_blocks[1].assign(self.edge_blocks[0])
                self.edge_blocks[0].assign(temp_edge)
        elif side == 'F':
            for _ in range(step):
                # rotate corner blocks
                temp_corner.assign(self.corner_blocks[1])
                self.corner_blocks[1].assign(self.corner_blocks[5])
                self.corner_blocks[5].assign(self.corner_blocks[4])
                self.corner_blocks[4].assign(self.corner_blocks[0])
                self.corner_blocks[0].assign(temp_corner)
                # reset orientation
                self.corner_blocks[1].orientation = (self.corner_blocks[1].orientation + 1) % 3
                self.corner_blocks[5].orientation = (self.corner_blocks[5].orientation + 2) % 3
                self.corner_blocks[4].orientation = (self.corner_blocks[4].orientation + 1) % 3
                self.corner_blocks[0].orientation = (self.corner_blocks[0].orientation + 2) % 3
                # rotate edge blocks
                temp_edge.assign(self.edge_blocks[5])
                self.edge_blocks[5].assign(self.edge_blocks[8])
                self.edge_blocks[8].assign(self.edge_blocks[4])
                self.edge_blocks[4].assign(self.edge_blocks[0])
                self.edge_blocks[0].assign(temp_edge)
                # reset orientation
                self.edge_blocks[5].orientation = (self.edge_blocks[5].orientation + 1) % 2
                self.edge_blocks[8].orientation = (self.edge_blocks[8].orientation + 1) % 2
                self.edge_blocks[4].orientation = (self.edge_blocks[4].orientation + 1) % 2
                self.edge_blocks[0].orientation = (self.edge_blocks[0].orientation + 1) % 2
        elif side == 'R':
            for _ in range(step):
                # rotate corner blocks
                temp_corner.assign(self.corner_blocks[4])
                self.corner_blocks[4].assign(self.corner_blocks[6])
                self.corner_blocks[6].assign(self.corner_blocks[2])
                self.corner_blocks[2].assign(self.corner_blocks[0])
                self.corner_blocks[0].assign(temp_corner)
                # reset orientation
                self.corner_blocks[4].orientation = (self.corner_blocks[4].orientation + 2) % 3
                self.corner_blocks[6].orientation = (self.corner_blocks[6].orientation + 1) % 3
                self.corner_blocks[2].orientation = (self.corner_blocks[2].orientation + 2) % 3
                self.corner_blocks[0].orientation = (self.corner_blocks[0].orientation + 1) % 3
                # rotate edge blocks
                temp_edge.assign(self.edge_blocks[4])
                self.edge_blocks[ 4].assign(self.edge_blocks[10])
                self.edge_blocks[10].assign(self.edge_blocks[ 6])
                self.edge_blocks[ 6].assign(self.edge_blocks[ 2])
                self.edge_blocks[ 2].assign(temp_edge)
        elif side == 'B':
            for _ in range(step):
                # rotate corner blocks
                temp_corner.assign(self.corner_blocks[3])
                self.corner_blocks[3].assign(self.corner_blocks[2])
                self.corner_blocks[2].assign(self.corner_blocks[6])
                self.corner_blocks[6].assign(self.corner_blocks[7])
                self.corner_blocks[7].assign(temp_corner)
                # reset orientation
                self.corner_blocks[3].orientation = (self.corner_blocks[3].orientation + 2) % 3
                self.corner_blocks[2].orientation = (self.corner_blocks[2].orientation + 1) % 3
                self.corner_blocks[6].orientation = (self.corner_blocks[6].orientation + 2) % 3
                self.corner_blocks[7].orientation = (self.corner_blocks[7].orientation + 1) % 3
                # rotate edge blocks
                temp_edge.assign(self.edge_blocks[7])
                self.edge_blocks[7].assign(self.edge_blocks[3])
                self.edge_blocks[3].assign(self.edge_blocks[6])
                self.edge_blocks[6].assign(self.edge_blocks[11])
                self.edge_blocks[11].assign(temp_edge)
                # reset orientation
                self.edge_blocks[ 7].orientation = (self.edge_blocks[ 7].orientation + 1) % 2
                self.edge_blocks[ 3].orientation = (self.edge_blocks[ 3].orientation + 1) % 2
                self.edge_blocks[ 6].orientation = (self.edge_blocks[ 6].orientation + 1) % 2
                self.edge_blocks[11].orientation = (self.edge_blocks[11].orientation + 1) % 2
        elif side == 'L':
            for _ in range(step):
                # rotate corner blocks
                temp_corner.assign(self.corner_blocks[5])
                self.corner_blocks[5].assign(self.corner_blocks[1])
                self.corner_blocks[1].assign(self.corner_blocks[3])
                self.corner_blocks[3].assign(self.corner_blocks[7])
                self.corner_blocks[7].assign(temp_corner)
                # reset orientation
                self.corner_blocks[5].orientation = (self.corner_blocks[5].orientation + 1) % 3
                self.corner_blocks[1].orientation = (self.corner_blocks[1].orientation + 2) % 3
                self.corner_blocks[3].orientation = (self.corner_blocks[3].orientation + 1) % 3
                self.corner_blocks[7].orientation = (self.corner_blocks[7].orientation + 2) % 3
                # rotate edge blocks
                temp_edge.assign(self.edge_blocks[5])
                self.edge_blocks[5].assign(self.edge_blocks[1])
                self.edge_blocks[1].assign(self.edge_blocks[7])
                self.edge_blocks[7].assign(self.edge_blocks[9])
                self.edge_blocks[9].assign(temp_edge)
        elif side == 'D':
            for _ in range(step):
                # rotate corner blocks
                temp_corner.assign(self.corner_blocks[6])
                self.corner_blocks[6].assign(self.corner_blocks[4])
                self.corner_blocks[4].assign(self.corner_blocks[5])
                self.corner_blocks[5].assign(self.corner_blocks[7])
                self.corner_blocks[7].assign(temp_corner)
                # rotate edge blocks
                temp_edge.assign(self.edge_blocks[10])
                self.edge_blocks[10].assign(self.edge_blocks[ 8])
                self.edge_blocks[ 8].assign(self.edge_blocks[ 9])
                self.edge_blocks[ 9].assign(self.edge_blocks[11])
                self.edge_blocks[11].assign(temp_edge)

    def movements(self, move_str=''):
        try:
            for n in move_str.strip().split(' '):
                self.move(n)
        except IndexError as err:
            print('Incorrect input: {}'.format(err))

    def scramble(self):
        m = ['U', 'L', 'F', 'R', 'B', 'D']
        s = ['1', '2', '3']
        for _ in range(24):
            self.move(m[random.randint(0, 5)] + s[random.randint(0, 2)])
        print('scrambled')

    def solve(self):
        solution = ''

        """ The Cross """
        # down-back
        for i in range(0, 12):
            block = self.edge_blocks[i]
            if block.colors == self.centers['d'] + self.centers['b']:
                if i == 0:
                    if block.orientation == 0:
                        self.movements('U2 B2')
                        solution += ' U2 B2'
                        break
                    elif block.orientation == 1:
                        self.movements('U2 B1 D1 L3 D3')
                        solution += ' U2 B1 D1 L3 D3'
                        break
                elif i == 1:
                    if block.orientation == 0:
                        self.movements('U1 B2')
                        solution += ' U1 B2'
                        break
                    elif block.orientation == 1:
                        self.movements('U1 B1 D1 L3 D3')
                        solution += ' U1 B1 D1 L3 D3'
                        break
                elif i == 2:
                    if block.orientation == 0:
                        self.movements('U3 B2')
                        solution += ' U3 B2'
                        break
                    elif block.orientation == 1:
                        self.movements('U3 B1 D1 L3 D3')
                        solution += ' U3 B1 D1 L3 D3'
                        break
                elif i == 3:
                    if block.orientation == 0:
                        self.movements('B2')
                        solution += ' B2'
                        break
                    elif block.orientation == 1:
                        self.movements('B1 D1 L3 D3')
                        solution += ' B1 D1 L3 D3'
                        break
                elif i == 4:
                    if block.orientation == 0:
                        self.movements('R1 U3 R3 B2')
                        solution += ' R1 U3 R3 B2'
                        break
                    elif block.orientation == 1:
                        self.movements('F3 U2 F1 B2')
                        solution += ' F3 U2 F1 B2'
                        break
                elif i == 5:
                    if block.orientation == 0:
                        self.movements('L3 U1 L1 B2')
                        solution += ' L3 U1 L1 B2'
                        break
                    elif block.orientation == 1:
                        self.movements('F1 U2 F3 B2')
                        solution += ' F1 U2 F3 B2'
                        break
                elif i == 6:
                    if block.orientation == 0:
                        self.movements('D3 R1 D1')
                        solution += ' D3 R1 D1'
                        break
                    elif block.orientation == 1:
                        self.movements('B3')
                        solution += ' B3'
                        break
                elif i == 7:
                    if block.orientation == 0:
                        self.movements('D1 L3 D3')
                        solution += ' D1 L3 D3'
                        break
                    elif block.orientation == 1:
                        self.movements('B1')
                        solution += ' B1'
                        break
                elif i == 8:
                    if block.orientation == 0:
                        self.movements('F2 U2 B2')
                        solution += ' F2 U2 B2'
                        break
                    elif block.orientation == 1:
                        self.movements('F2 U2 B1 D1 L3 D3')
                        solution += ' F2 U2 B1 D1 L3 D3'
                        break
                elif i == 9:
                    if block.orientation == 0:
                        self.movements('L2 U1 B2')
                        solution += ' L2 U1 B2'
                        break
                    elif block.orientation == 1:
                        self.movements('L2 U1 B1 D1 L3 D3')
                        solution += ' L2 U1 B1 D1 L3 D3'
                        break
                elif i == 10:
                    if block.orientation == 0:
                        self.movements('R2 U3 B2')
                        solution += ' R2 U3 B2'
                        break
                    elif block.orientation == 1:
                        self.movements('R2 U3 B1 D1 L3 D3')
                        solution += ' R2 U3 B1 D1 L3 D3'
                        break
                elif i == 11:
                    if block.orientation == 0:
                        # correct
                        break
                    elif block.orientation == 1:
                        self.movements('B3 D1 L3 D3')
                        solution += ' B3 D1 L3 D3'
                        break
        # down-right
        for i in range(0, 11):
            block = self.edge_blocks[i]
            if block.colors == self.centers['d'] + self.centers['r']:
                if i == 0:
                    if block.orientation == 0:
                        self.movements('U3 R2')
                        solution += ' U3 R2'
                        break
                    elif block.orientation == 1:
                        self.movements('U3 R1 D1 B3 D3')
                        solution += ' U3 R1 D1 B3 D3'
                        break
                elif i == 1:
                    if block.orientation == 0:
                        self.movements('U2 R2')
                        solution += ' U2 R2'
                        break
                    elif block.orientation == 1:
                        self.movements('U2 R1 D1 B3 D3')
                        solution += ' U2 R1 D1 B3 D3'
                        break
                elif i == 2:
                    if block.orientation == 0:
                        self.movements('R2')
                        solution += ' R2'
                        break
                    elif block.orientation == 1:
                        self.movements('R1 D1 B3 D3')
                        solution += ' R1 D1 B3 D3'
                        break
                elif i == 3:
                    if block.orientation == 0:
                        self.movements('U1 R2')
                        solution += ' U1 R2'
                        break
                    elif block.orientation == 1:
                        self.movements('U1 R1 D1 B3 D3')
                        solution += ' U1 R1 D1 B3 D3'
                        break
                elif i == 4:
                    if block.orientation == 0:
                        self.movements('R3')
                        solution += ' R3'
                        break
                    elif block.orientation == 1:
                        self.movements('D3 F1 D1')
                        solution += ' D3 F1 D1'
                        break
                elif i == 5:
                    if block.orientation == 0:
                        self.movements('L3 U2 L1 R2')
                        solution += ' L3 U2 L1 R2'
                        break
                    elif block.orientation == 1:
                        self.movements('F1 U3 F3 R2')
                        solution += ' F1 U3 F3 R2'
                        break
                elif i == 6:
                    if block.orientation == 0:
                        self.movements('R1')
                        solution += ' R1'
                        break
                    elif block.orientation == 1:
                        self.movements('D1 B3 D3')
                        solution += ' D1 B3 D3'
                        break
                elif i == 7:
                    if block.orientation == 0:
                        self.movements('L1 U2 L3 R2')
                        solution += ' L1 U2 L3 R2'
                        break
                    elif block.orientation == 1:
                        self.movements('B3 U1 F1 R2 B1')
                        solution += ' B3 U1 F1 R2 B1'
                        break
                elif i == 8:
                    if block.orientation == 0:
                        self.movements('F2 U3 R2')
                        solution += ' F2 U3 R2'
                        break
                    elif block.orientation == 1:
                        self.movements('F2 U3 R1 D1 B3 D3')
                        solution += ' F2 U3 R1 D1 B3 D3'
                        break
                elif i == 9:
                    if block.orientation == 0:
                        self.movements('L2 U2 R2')
                        solution += ' L2 U2 R2'
                        break
                    elif block.orientation == 1:
                        self.movements('L2 U2 R1 D1 B3 D3')
                        solution += ' L2 U2 R1 D1 B3 D3'
                        break
                elif i == 10:
                    if block.orientation == 0:
                        # correct
                        break
                    elif block.orientation == 1:
                        self.movements('R3 D1 B3 D3')
                        solution += ' B3 D1 L3 D3'
                        break
        # down-left
        for i in range(0, 10):
            block = self.edge_blocks[i]
            if block.colors == self.centers['d'] + self.centers['l']:
                if i == 0:
                    if block.orientation == 0:
                        self.movements('U1 L2')
                        solution += ' U1 L2'
                        break
                    elif block.orientation == 1:
                        self.movements('U1 L1 D1 F3 D3')
                        solution += ' U1 L1 D1 F3 D3'
                        break
                elif i == 1:
                    if block.orientation == 0:
                        self.movements('L2')
                        solution += ' L2'
                        break
                    elif block.orientation == 1:
                        self.movements('L1 D1 F3 D3')
                        solution += ' L1 D1 F3 D3'
                        break
                elif i == 2:
                    if block.orientation == 0:
                        self.movements('U2 L2')
                        solution += ' U2 L2'
                        break
                    elif block.orientation == 1:
                        self.movements('U2 L1 D1 F3 D3')
                        solution += ' U2 L1 D1 F3 D3'
                        break
                elif i == 3:
                    if block.orientation == 0:
                        self.movements('U3 L2')
                        solution += ' U3 L2'
                        break
                    elif block.orientation == 1:
                        self.movements('U3 L1 D1 F3 D3')
                        solution += ' U3 L1 D1 F3 D3'
                        break
                elif i == 4:
                    if block.orientation == 0:
                        self.movements('R1 U2 R3 L2')
                        solution += ' R1 U2 R3 L2'
                        break
                    elif block.orientation == 1:
                        self.movements('F3 U1 F1 L2')
                        solution += ' F3 U1 F1 L2'
                        break
                elif i == 5:
                    if block.orientation == 0:
                        self.movements('L1')
                        solution += ' L1'
                        break
                    elif block.orientation == 1:
                        self.movements('D1 F3 D3')
                        solution += ' D1 F3 D3'
                        break
                elif i == 6:
                    if block.orientation == 0:
                        self.movements('R3 U2 R1 L2')
                        solution += ' R3 U2 R1 L2'
                        break
                    elif block.orientation == 1:
                        self.movements('B1 U3 B3 L2')
                        solution += ' B1 U3 B3 L2'
                        break
                elif i == 7:
                    if block.orientation == 0:
                        self.movements('L3')
                        solution += ' L3'
                        break
                    elif block.orientation == 1:
                        self.movements('D3 B1 D1')
                        solution += ' D3 B1 D1'
                        break
                elif i == 8:
                    if block.orientation == 0:
                        self.movements('F2 U1 L2')
                        solution += ' F2 U1 L2'
                        break
                    elif block.orientation == 1:
                        self.movements('F2 U1 L1 D1 F3 D3')
                        solution += ' F2 U1 L1 D1 F3 D3'
                        break
                elif i == 9:
                    if block.orientation == 0:
                        # correct
                        break
                    elif block.orientation == 1:
                        self.movements('L3 D1 F3 D3')
                        solution += ' L3 D1 F3 D3'
                        break
        # down-front
        for i in range(0, 9):
            block = self.edge_blocks[i]
            if block.colors == self.centers['d'] + self.centers['f']:
                if i == 0:
                    if block.orientation == 0:
                        self.movements('F2')
                        solution += ' F2'
                        break
                    elif block.orientation == 1:
                        self.movements('F1 D1 R3 D3')
                        solution += ' F1 D1 R3 D3'
                        break
                elif i == 1:
                    if block.orientation == 0:
                        self.movements('U3 F2')
                        solution += ' U3 F2'
                        break
                    elif block.orientation == 1:
                        self.movements('U3 F1 D1 R3 D3')
                        solution += ' U3 F1 D1 R3 D3'
                        break
                elif i == 2:
                    if block.orientation == 0:
                        self.movements('U1 F2')
                        solution += ' U1 F2'
                        break
                    elif block.orientation == 1:
                        self.movements('U1 F1 D1 R3 D3')
                        solution += ' U1 F1 D1 R3 D3'
                        break
                elif i == 3:
                    if block.orientation == 0:
                        self.movements('U2 F2')
                        solution += ' U2 F2'
                        break
                    elif block.orientation == 1:
                        self.movements('U2 F1 D1 R3 D3')
                        solution += ' U2 F1 D1 R3 D3'
                        break
                elif i == 4:
                    if block.orientation == 0:
                        self.movements('D1 R3 D3')
                        solution += ' D1 R3 D3'
                        break
                    elif block.orientation == 1:
                        self.movements('F1')
                        solution += ' F1'
                        break
                elif i == 5:
                    if block.orientation == 0:
                        self.movements('D3 L1 D1')
                        solution += ' D3 L1 D1'
                        break
                    elif block.orientation == 1:
                        self.movements('F3')
                        solution += ' F3'
                        break
                elif i == 6:
                    if block.orientation == 0:
                        self.movements('R3 U1 R1 F2')
                        solution += ' R3 U1 R1 F2'
                        break
                    elif block.orientation == 1:
                        self.movements('B1 U2 B3 F2')
                        solution += ' B1 U2 B3 F2'
                        break
                elif i == 7:
                    if block.orientation == 0:
                        self.movements('L1 U3 L3 F2')
                        solution += ' L1 U3 L3 F2'
                        break
                    elif block.orientation == 1:
                        self.movements('B3 U2 B1 F2')
                        solution += ' B3 U2 B1 F2'
                        break
                elif i == 8:
                    if block.orientation == 0:
                        # correct
                        break
                    elif block.orientation == 1:
                        self.movements('F3 D1 R3 D3')
                        solution += ' F3 D1 R3 D3'
                        break

        """ F2L (First 2 Layers) """
        # down-back-left pair
        for i in range(0, 8):
            # reposition corner block
            c_block = self.corner_blocks[i]
            if c_block.colors == self.centers['d'] + self.centers['b'] + self.centers['l']:
                if i == 0:
                    self.movements('U2')
                    solution += ' U2'
                elif i == 1:
                    self.movements('U1')
                    solution += ' U1'
                elif i == 2:
                    self.movements('U3')
                    solution += ' U3'
                elif i == 3:
                    pass
                elif i == 4:
                    self.movements('R1 U2 R3')
                    solution += ' R1 U2 R3'
                elif i == 5:
                    self.movements('F1 U1 F3')
                    solution += ' F1 U1 F3'
                elif i == 6:
                    self.movements('R3 U3 R1')
                    solution += ' R3 U3 R1'
                elif i == 7:
                    if c_block.orientation == 0:
                        if self.edge_blocks[7].colors == self.centers['b'] + self.centers['l']:
                            if self.edge_blocks[7].orientation == 0:
                                # correct
                                break
                    self.movements('L1 U3 L3')
                    solution += ' L1 U3 L3'
                for j in range(4, 8):
                    # reposition edge block
                    e_block = self.edge_blocks[j]
                    if e_block.colors == self.centers['b'] + self.centers['l']:
                        if j == 4:
                            self.movements('R1 U3 R3 U1')
                            solution += ' R1 U3 R3 U1'
                            break
                        elif j == 5:
                            self.movements('L3 U1 L1')
                            solution += ' L3 U1 L1'
                            break
                        elif j == 6:
                            self.movements('B1 U3 B3')
                            solution += ' B1 U3 B3'
                            break
                        elif j == 7:
                            break
                # 30 cases
                c_block = self.corner_blocks[3]
                for j in [0, 1, 2, 3, 7]:
                    # find edge block
                    e_block = self.edge_blocks[j]
                    if e_block.colors == self.centers['b'] + self.centers['l']:
                        if j == 0:
                            if c_block.orientation == 0:
                                if e_block.orientation == 0:
                                    self.movements('U1 L1 U2 L3 U1 L1 U3 L3')
                                    solution += ' U1 L1 U2 L3 U1 L1 U3 L3'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('B3 U1 B1 U2 B3 U3 B1')
                                    solution += ' B3 U1 B1 U2 B3 U3 B1'
                                    break
                            elif c_block.orientation == 1:
                                if e_block.orientation == 0:
                                    self.movements('U3 L1 U1 L3 U2 L1 U3 L3')
                                    solution += ' U3 L1 U1 L3 U2 L1 U3 L3'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U1 B3 U3 B1 U3 B3 U3 B1')
                                    solution += ' U1 B3 U3 B1 U3 B3 U3 B1'
                                    break
                            elif c_block.orientation == 2:
                                if e_block.orientation == 0:
                                    self.movements('L1 U1 L3')
                                    solution += ' L1 U1 L3'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U1 B3 U2 B1 U2 B3 U1 B1')
                                    solution += ' U1 B3 U2 B1 U2 B3 U1 B1'
                                    break
                        elif j == 1:
                            if c_block.orientation == 0:
                                if e_block.orientation == 0:
                                    self.movements('L1 U2 L3 U3 L1 U1 L3')
                                    solution += ' L1 U2 L3 U3 L1 U1 L3'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U2 B2 U2 B1 U1 B3 U1 B2')
                                    solution += ' U2 B2 U2 B1 U1 B3 U1 B2'
                                    break
                            elif c_block.orientation == 1:
                                if e_block.orientation == 0:
                                    self.movements('U1 L1 U3 L3')
                                    solution += ' U1 L1 U3 L3'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('B3 U1 B1 U3 B3 U1 B1 U2 B3 U1 B1')
                                    solution += ' B3 U1 B1 U3 B3 U1 B1 U2 B3 U1 B1'
                                    break
                            elif c_block.orientation == 2:
                                if e_block.orientation == 0:
                                    self.movements('U3 L1 U3 L3 U1 L1 U1 L3')
                                    solution += ' U3 L1 U3 L3 U1 L1 U1 L3'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('L1 U3 L3 U2 B3 U3 B1')
                                    solution += ' L1 U3 L3 U2 B3 U3 B1'
                                    break
                        elif j == 2:
                            if c_block.orientation == 0:
                                if e_block.orientation == 0:
                                    self.movements('L1 U3 L3 U2 L1 U1 L3')
                                    solution += ' L1 U3 L3 U2 L1 U1 L3'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U3 B3 U2 B1 U3 B3 U1 B1')
                                    solution += ' U3 B3 U2 B1 U3 B3 U1 B1'
                                    break
                            elif c_block.orientation == 1:
                                if e_block.orientation == 0:
                                    self.movements('U3 L1 U2 L3 U2 L1 U3 L3')
                                    solution += ' U3 L1 U2 L3 U2 L1 U3 L3'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('B3 U3 B1')
                                    solution += ' B3 U3 B1'
                                    break
                            elif c_block.orientation == 2:
                                if e_block.orientation == 0:
                                    self.movements('U3 L1 U1 L3 U1 L1 U1 L3')
                                    solution += ' U3 L1 U1 L3 U1 L1 U1 L3'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U1 B3 U3 B1 U2 B3 U1 B1')
                                    solution += ' U1 B3 U3 B1 U2 B3 U1 B1'
                                    break
                        elif j == 3:
                            if c_block.orientation == 0:
                                if e_block.orientation == 0:
                                    self.movements('U2 L2 U2 L3 U3 L1 U3 L2')
                                    solution += ' U2 L2 U2 L3 U3 L1 U3 L2'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('B3 U2 B1 U1 B3 U3 B1')
                                    solution += ' B3 U2 B1 U1 B3 U3 B1'
                                    break
                            elif c_block.orientation == 1:
                                if e_block.orientation == 0:
                                    self.movements('B3 U1 B1 U2 L1 U1 L3')
                                    solution += ' B3 U1 B1 U2 L1 U1 L3'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U1 B3 U1 B1 U3 B3 U3 B1')
                                    solution += ' U1 B3 U1 B1 U3 B3 U3 B1'
                                    break
                            elif c_block.orientation == 2:
                                if e_block.orientation == 0:
                                    self.movements('L1 U3 L3 U1 L1 U3 L3 U2 L1 U3 L3')
                                    solution += ' L1 U3 L3 U1 L1 U3 L3 U2 L1 U3 L3'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U3 B3 U1 B1')
                                    solution += ' U3 B3 U1 B1'
                                    break
                        elif j == 7:
                            if c_block.orientation == 0:
                                if e_block.orientation == 0:
                                    self.movements('L1 U1 L3 U3 L1 U1 L3 U3 L1 U1 L3')
                                    solution += ' L1 U1 L3 U3 L1 U1 L3 U3 L1 U1 L3'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('L1 U3 L3 B3 U2 B1')
                                    solution += ' L1 U3 L3 B3 U2 B1'
                                    break
                            elif c_block.orientation == 1:
                                if e_block.orientation == 0:
                                    self.movements('U3 L1 U3 L3 U2 L1 U3 L3')
                                    solution += ' U3 L1 U3 L3 U2 L1 U3 L3'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U3 L1 U1 L3 U1 B3 U3 B1')
                                    solution += ' U3 L1 U1 L3 U1 B3 U3 B1'
                                    break
                            elif c_block.orientation == 2:
                                if e_block.orientation == 0:
                                    self.movements('U1 B3 U1 B1 U2 B3 U1 B1')
                                    solution += ' U1 B3 U1 B1 U2 B3 U1 B1'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U1 B3 U3 B1 U3 L1 U1 L3')
                                    solution += ' U1 B3 U3 B1 U3 L1 U1 L3'
                                    break
                break
        # down-right-back pair
        for i in range(0, 7):
            # reposition corner block
            c_block = self.corner_blocks[i]
            if c_block.colors == self.centers['d'] + self.centers['r'] + self.centers['b']:
                if i == 0:
                    self.movements('U3')
                    solution += ' U3'
                elif i == 1:
                    self.movements('U2')
                    solution += ' U2'
                elif i == 2:
                    pass
                elif i == 3:
                    self.movements('U1')
                    solution += ' U1'
                elif i == 4:
                    self.movements('F3 U3 F1')
                    solution += ' F3 U3 F1'
                elif i == 5:
                    self.movements('F1 U2 F3')
                    solution += ' F1 U2 F3'
                elif i == 6:
                    if c_block.orientation == 0:
                        if self.edge_blocks[6].colors == self.centers['b'] + self.centers['r']:
                            if self.edge_blocks[6].orientation == 0:
                                # correct
                                break
                    self.movements('B1 U3 B3')
                    solution += ' B1 U3 B3'
                for j in range(4, 7):
                    # reposition edge block
                    e_block = self.edge_blocks[j]
                    if e_block.colors == self.centers['b'] + self.centers['r']:
                        if j == 4:
                            self.movements('R1 U3 R3')
                            solution += ' R1 U3 R3'
                            break
                        elif j == 5:
                            self.movements('F1 U3 F3 U1')
                            solution += ' F1 U3 F3 U1'
                            break
                        elif j == 6:
                            break
                # 30 cases
                c_block = self.corner_blocks[2]
                for j in [0, 1, 2, 3, 6]:
                    # find edge block
                    e_block = self.edge_blocks[j]
                    if e_block.colors == self.centers['b'] + self.centers['r']:
                        if j == 0:
                            if c_block.orientation == 0:
                                if e_block.orientation == 0:
                                    self.movements('U3 R3 U2 R1 U3 R3 U1 R1')
                                    solution += ' U3 R3 U2 R1 U3 R3 U1 R1'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('B1 U3 B3 U2 B1 U1 B3')
                                    solution += ' B1 U3 B3 U2 B1 U1 B3'
                                    break
                            elif c_block.orientation == 1:
                                if e_block.orientation == 0:
                                    self.movements('R3 U3 R1')
                                    solution += ' R3 U3 R1'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U3 B1 U2 B3 U2 B1 U3 B3')
                                    solution += ' U3 B1 U2 B3 U2 B1 U3 B3'
                                    break
                            elif c_block.orientation == 2:
                                if e_block.orientation == 0:
                                    self.movements('U1 R3 U3 R1 U2 R3 U1 R1')
                                    solution += ' U1 R3 U3 R1 U2 R3 U1 R1'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U3 B1 U1 B3 U1 B1 U1 B3')
                                    solution += ' U3 B1 U1 B3 U1 B1 U1 B3'
                                    break
                        elif j == 1:
                            if c_block.orientation == 0:
                                if e_block.orientation == 0:
                                    self.movements('R3 U1 R1 U2 R3 U3 R1')
                                    solution += ' R3 U1 R1 U2 R3 U3 R1'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U1 B1 U2 B3 U1 B1 U3 B3')
                                    solution += ' U1 B1 U2 B3 U1 B1 U3 B3'
                                    break
                            elif c_block.orientation == 1:
                                if e_block.orientation == 0:
                                    self.movements('U1 R3 U3 R1 U3 R3 U3 R1')
                                    solution += ' U1 R3 U3 R1 U3 R3 U3 R1'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U3 B1 U1 B3 U2 B1 U3 B3')
                                    solution += ' U3 B1 U1 B3 U2 B1 U3 B3'
                                    break
                            elif c_block.orientation == 2:
                                if e_block.orientation == 0:
                                    self.movements('U1 R3 U2 R1 U2 R3 U1 R1')
                                    solution += ' U1 R3 U2 R1 U2 R3 U1 R1'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('B1 U1 B3')
                                    solution += ' B1 U1 B3'
                                    break
                        elif j == 2:
                            if c_block.orientation == 0:
                                if e_block.orientation == 0:
                                    self.movements('R3 U2 R1 U1 R3 U3 R1')
                                    solution += ' R3 U2 R1 U1 R3 U3 R1'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U2 B2 U2 B3 U3 B1 U3 B2')
                                    solution += ' U2 B2 U2 B3 U3 B1 U3 B2'
                                    break
                            elif c_block.orientation == 1:
                                if e_block.orientation == 0:
                                    self.movements('U1 R3 U1 R1 U3 R3 U3 R1')
                                    solution += ' U1 R3 U1 R1 U3 R3 U3 R1'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('R3 U1 R1 U2 B1 U1 B3')
                                    solution += ' R3 U1 R1 U2 B1 U1 B3'
                                    break
                            elif c_block.orientation == 2:
                                if e_block.orientation == 0:
                                    self.movements('U3 R3 U1 R1')
                                    solution += ' U3 R3 U1 R1'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('B1 U3 B3 U1 B1 U3 B3 U2 B1 U3 B3')
                                    solution += ' B1 U3 B3 U1 B1 U3 B3 U2 B1 U3 B3'
                                    break
                        elif j == 3:
                            if c_block.orientation == 0:
                                if e_block.orientation == 0:
                                    self.movements('U2 R2 U2 R1 U1 R3 U1 R2')
                                    solution += ' U2 R2 U2 R1 U1 R3 U1 R2'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('B1 U2 B3 U3 B1 U1 B3')
                                    solution += ' B1 U2 B3 U3 B1 U1 B3'
                                    break
                            elif c_block.orientation == 1:
                                if e_block.orientation == 0:
                                    self.movements('R3 U1 R1 U3 R3 U1 R1 U2 R3 U1 R1')
                                    solution += ' R3 U1 R1 U3 R3 U1 R1 U2 R3 U1 R1'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U1 B1 U3 B3')
                                    solution += ' U1 B1 U3 B3'
                                    break
                            elif c_block.orientation == 2:
                                if e_block.orientation == 0:
                                    self.movements('B1 U3 B3 U2 R3 U3 R1')
                                    solution += ' B1 U3 B3 U2 R3 U3 R1'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U3 B1 U3 B3 U1 B1 U1 B3')
                                    solution += ' U3 B1 U3 B3 U1 B1 U1 B3'
                                    break
                        elif j == 6:
                            if c_block.orientation == 0:
                                if e_block.orientation == 0:
                                    self.movements('B1 U1 B3 U3 B1 U1 B3 U3 B1 U1 B3')
                                    solution += ' B1 U1 B3 U3 B1 U1 B3 U3 B1 U1 B3'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('B1 U3 B3 R3 U2 R1')
                                    solution += ' B1 U3 B3 R3 U2 R1'
                                    break
                            elif c_block.orientation == 1:
                                if e_block.orientation == 0:
                                    self.movements('U3 B1 U3 B3 U2 B1 U3 B3')
                                    solution += ' U3 B1 U3 B3 U2 B1 U3 B3'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U3 B1 U1 B3 U1 R3 U3 R1')
                                    solution += ' U3 B1 U1 B3 U1 R3 U3 R1'
                                    break
                            elif c_block.orientation == 2:
                                if e_block.orientation == 0:
                                    self.movements('U1 R3 U1 R1 U2 R3 U1 R1')
                                    solution += ' U1 R3 U1 R1 U2 R3 U1 R1'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U1 R3 U3 R1 U3 B1 U1 B3')
                                    solution += ' U1 R3 U3 R1 U3 B1 U1 B3'
                                    break
                break
        # down-left-front pair
        for i in range(0, 6):
            # reposition corner block
            c_block = self.corner_blocks[i]
            if c_block.colors == self.centers['d'] + self.centers['l'] + self.centers['f']:
                if i == 0:
                    self.movements('U1')
                    solution += ' U1'
                elif i == 1:
                    pass
                elif i == 2:
                    self.movements('U2')
                    solution += ' U2'
                elif i == 3:
                    self.movements('U3')
                    solution += ' U3'
                elif i == 4:
                    self.movements('R1 U1 R3')
                    solution += ' R1 U1 R3'
                elif i == 5:
                    if c_block.orientation == 0:
                        if self.edge_blocks[5].colors == self.centers['f'] + self.centers['l']:
                            if self.edge_blocks[5].orientation == 0:
                                # correct
                                break
                    self.movements('F1 U3 F3')
                    solution += ' F1 U3 F3'
                for j in range(4, 6):
                    # reposition edge block
                    e_block = self.edge_blocks[j]
                    if e_block.colors == self.centers['f'] + self.centers['l']:
                        if j == 4:
                            self.movements('R1 U1 R3 U3')
                            solution += ' R1 U1 R3 U3'
                            break
                        elif j == 5:
                            break
                # 30 cases
                c_block = self.corner_blocks[1]
                for j in [0, 1, 2, 3, 5]:
                    # find edge block
                    e_block = self.edge_blocks[j]
                    if e_block.colors == self.centers['f'] + self.centers['l']:
                        if j == 0:
                            if c_block.orientation == 0:
                                if e_block.orientation == 0:
                                    self.movements('U2 L2 U2 L1 U1 L3 U1 L2')
                                    solution += ' U2 L2 U2 L1 U1 L3 U1 L2'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('F1 U2 F3 U3 F1 U1 F3')
                                    solution += ' F1 U2 F3 U3 F1 U1 F3'
                                    break
                            elif c_block.orientation == 1:
                                if e_block.orientation == 0:
                                    self.movements('L3 U1 L1 U3 L3 U1 L1 U2 L3 U1 L1')
                                    solution += ' L3 U1 L1 U3 L3 U1 L1 U2 L3 U1 L1'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U1 F1 U3 F3')
                                    solution += ' U1 F1 U3 F3'
                                    break
                            elif c_block.orientation == 2:
                                if e_block.orientation == 0:
                                    self.movements('F1 U3 F3 U2 L3 U3 L1')
                                    solution += ' F1 U3 F3 U2 L3 U3 L1'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U3 F1 U3 F3 U1 F1 U1 F3')
                                    solution += ' U3 F1 U3 F3 U1 F1 U1 F3'
                                    break
                        elif j == 1:
                            if c_block.orientation == 0:
                                if e_block.orientation == 0:
                                    self.movements('L3 U2 L1 U1 L3 U3 L1')
                                    solution += ' L3 U2 L1 U1 L3 U3 L1'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U2 F2 U2 F3 U3 F1 U3 F2')
                                    solution += ' U2 F2 U2 F3 U3 F1 U3 F2'
                                    break
                            elif c_block.orientation == 1:
                                if e_block.orientation == 0:
                                    self.movements('U1 L3 U1 L1 U3 L3 U3 L1')
                                    solution += ' U1 L3 U1 L1 U3 L3 U3 L1'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('L3 U1 L1 U2 F1 U1 F3')
                                    solution += ' L3 U1 L1 U2 F1 U1 F3'
                                    break
                            elif c_block.orientation == 2:
                                if e_block.orientation == 0:
                                    self.movements('U3 L3 U1 L1')
                                    solution += ' U3 L3 U1 L1'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('F1 U3 F3 U1 F1 U3 F3 U2 F1 U3 F3')
                                    solution += ' F1 U3 F3 U1 F1 U3 F3 U2 F1 U3 F3'
                                    break
                        elif j == 2:
                            if c_block.orientation == 0:
                                if e_block.orientation == 0:
                                    self.movements('L3 U1 L1 U2 L3 U3 L1')
                                    solution += ' L3 U1 L1 U2 L3 U3 L1'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U1 F1 U2 F3 U1 F1 U3 F3')
                                    solution += ' U1 F1 U2 F3 U1 F1 U3 F3'
                                    break
                            elif c_block.orientation == 1:
                                if e_block.orientation == 0:
                                    self.movements('U1 L3 U3 L1 U3 L3 U3 L1')
                                    solution += ' U1 L3 U3 L1 U3 L3 U3 L1'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U3 F1 U1 F3 U2 F1 U3 F3')
                                    solution += ' U3 F1 U1 F3 U2 F1 U3 F3'
                                    break
                            elif c_block.orientation == 2:
                                if e_block.orientation == 0:
                                    self.movements('U1 L3 U2 L1 U2 L3 U1 L1')
                                    solution += ' U1 L3 U2 L1 U2 L3 U1 L1'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('F1 U1 F3')
                                    solution += ' F1 U1 F3'
                                    break
                        elif j == 3:
                            if c_block.orientation == 0:
                                if e_block.orientation == 0:
                                    self.movements('U3 L3 U2 L1 U3 L3 U1 L1')
                                    solution += ' U3 L3 U2 L1 U3 L3 U1 L1'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('F1 U3 F3 U2 F1 U1 F3')
                                    solution += ' F1 U3 F3 U2 F1 U1 F3'
                                    break
                            elif c_block.orientation == 1:
                                if e_block.orientation == 0:
                                    self.movements('L3 U3 L1')
                                    solution += ' L3 U3 L1'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U3 F1 U2 F3 U2 F1 U3 F3')
                                    solution += ' U3 F1 U2 F3 U2 F1 U3 F3'
                                    break
                            elif c_block.orientation == 2:
                                if e_block.orientation == 0:
                                    self.movements('U1 L3 U3 L1 U2 L3 U1 L1')
                                    solution += ' U1 L3 U3 L1 U2 L3 U1 L1'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U3 F1 U1 F3 U1 F1 U1 F3')
                                    solution += ' U3 F1 U1 F3 U1 F1 U1 F3'
                                    break
                        elif j == 5:
                            if c_block.orientation == 0:
                                if e_block.orientation == 0:
                                    self.movements('F1 U1 F3 U3 F1 U1 F3 U3 F1 U1 F3')
                                    solution += ' F1 U1 F3 U3 F1 U1 F3 U3 F1 U1 F3'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('F1 U3 F3 L3 U2 L1')
                                    solution += ' F1 U3 F3 L3 U2 L1'
                                    break
                            elif c_block.orientation == 1:
                                if e_block.orientation == 0:
                                    self.movements('U3 F1 U3 F3 U2 F1 U3 F3')
                                    solution += ' U3 F1 U3 F3 U2 F1 U3 F3'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U3 F1 U1 F3 U1 L3 U3 L1')
                                    solution += ' U3 F1 U1 F3 U1 L3 U3 L1'
                                    break
                            elif c_block.orientation == 2:
                                if e_block.orientation == 0:
                                    self.movements('U1 L3 U1 L1 U2 L3 U1 L1')
                                    solution += ' U1 L3 U1 L1 U2 L3 U1 L1'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U1 L3 U3 L1 U3 F1 U1 F3')
                                    solution += ' U1 L3 U3 L1 U3 F1 U1 F3'
                                    break
                break
        # down-front-right pair
        for i in range(0, 5):
            # reposition corner block
            c_block = self.corner_blocks[i]
            if c_block.colors == self.centers['d'] + self.centers['f'] + self.centers['r']:
                if i == 0:
                    pass
                elif i == 1:
                    self.movements('U3')
                    solution += ' U3'
                elif i == 2:
                    self.movements('U1')
                    solution += ' U1'
                elif i == 3:
                    self.movements('U2')
                    solution += ' U2'
                elif i == 4:
                    if c_block.orientation == 0:
                        if self.edge_blocks[4].colors == self.centers['f'] + self.centers['r']:
                            if self.edge_blocks[4].orientation == 0:
                                # correct
                                break
                    self.movements('R1 U3 R3')
                    solution += ' R1 U3 R3'
                for j in range(4, 5):
                    # reposition edge block
                    e_block = self.edge_blocks[j]
                    if e_block.colors == self.centers['f'] + self.centers['r']:
                        if j == 4:
                            break
                # 30 cases
                c_block = self.corner_blocks[0]
                for j in [0, 1, 2, 3, 4]:
                    # find edge block
                    e_block = self.edge_blocks[j]
                    if e_block.colors == self.centers['f'] + self.centers['r']:
                        if j == 0:
                            if c_block.orientation == 0:
                                if e_block.orientation == 0:
                                    self.movements('U2 R2 U2 R3 U3 R1 U3 R2')
                                    solution += ' U2 R2 U2 R3 U3 R1 U3 R2'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('F3 U2 F1 U1 F3 U3 F1')
                                    solution += ' F3 U2 F1 U1 F3 U3 F1'
                                    break
                            elif c_block.orientation == 1:
                                if e_block.orientation == 0:
                                    self.movements('F3 U1 F1 U2 R1 U1 R3')
                                    solution += ' F3 U1 F1 U2 R1 U1 R3'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U1 F3 U1 F1 U3 F3 U3 F1')
                                    solution += ' U1 F3 U1 F1 U3 F3 U3 F1'
                                    break
                            elif c_block.orientation == 2:
                                if e_block.orientation == 0:
                                    self.movements('R1 U3 R3 U1 R1 U3 R3 U2 R1 U3 R3')
                                    solution += ' R1 U3 R3 U1 R1 U3 R3 U2 R1 U3 R3'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U3 F3 U1 F1')
                                    solution += ' U3 F3 U1 F1'
                                    break
                        elif j == 1:
                            if c_block.orientation == 0:
                                if e_block.orientation == 0:
                                    self.movements('R1 U3 R3 U2 R1 U1 R3')
                                    solution += ' R1 U3 R3 U2 R1 U1 R3'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U3 F3 U2 F1 U3 F3 U1 F1')
                                    solution += ' U3 F3 U2 F1 U3 F3 U1 F1'
                                    break
                            elif c_block.orientation == 1:
                                if e_block.orientation == 0:
                                    self.movements('U3 R1 U2 R3 U2 R1 U3 R3')
                                    solution += ' U3 R1 U2 R3 U2 R1 U3 R3'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('F3 U3 F1')
                                    solution += ' F3 U3 F1'
                                    break
                            elif c_block.orientation == 2:
                                if e_block.orientation == 0:
                                    self.movements('U3 R1 U1 R3 U1 R1 U1 R3')
                                    solution += ' U3 R1 U1 R3 U1 R1 U1 R3'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U1 F3 U3 F1 U2 F3 U1 F1')
                                    solution += ' U1 F3 U3 F1 U2 F3 U1 F1'
                                    break
                        elif j == 2:
                            if c_block.orientation == 0:
                                if e_block.orientation == 0:
                                    self.movements('R1 U2 R3 U3 R1 U1 R3')
                                    solution += ' R1 U2 R3 U3 R1 U1 R3'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U2 F2 U2 F1 U1 F3 U1 F2')
                                    solution += ' U2 F2 U2 F1 U1 F3 U1 F2'
                                    break
                            elif c_block.orientation == 1:
                                if e_block.orientation == 0:
                                    self.movements('U1 R1 U3 R3')
                                    solution += ' U1 R1 U3 R3'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('F3 U1 F1 U3 F3 U1 F1 U2 F3 U1 F1')
                                    solution += ' F3 U1 F1 U3 F3 U1 F1 U2 F3 U1 F1'
                                    break
                            elif c_block.orientation == 2:
                                if e_block.orientation == 0:
                                    self.movements('U3 R1 U3 R3 U1 R1 U1 R3')
                                    solution += ' U3 R1 U3 R3 U1 R1 U1 R3'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('R1 U3 R3 U2 F3 U3 F1')
                                    solution += ' R1 U3 R3 U2 F3 U3 F1'
                                    break
                        elif j == 3:
                            if c_block.orientation == 0:
                                if e_block.orientation == 0:
                                    self.movements('U1 R1 U2 R3 U1 R1 U3 R3')
                                    solution += ' U1 R1 U2 R3 U1 R1 U3 R3'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('F3 U1 F1 U2 F3 U3 F1')
                                    solution += ' F3 U1 F1 U2 F3 U3 F1'
                                    break
                            elif c_block.orientation == 1:
                                if e_block.orientation == 0:
                                    self.movements('U3 R1 U1 R3 U2 R1 U3 R3')
                                    solution += ' U3 R1 U1 R3 U2 R1 U3 R3'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U1 F3 U3 F1 U3 F3 U3 F1')
                                    solution += ' U1 F3 U3 F1 U3 F3 U3 F1'
                                    break
                            elif c_block.orientation == 2:
                                if e_block.orientation == 0:
                                    self.movements('R1 U1 R3')
                                    solution += ' R1 U1 R3'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U1 F3 U2 F1 U2 F3 U1 F1')
                                    solution += ' U1 F3 U2 F1 U2 F3 U1 F1'
                                    break
                        elif j == 4:
                            if c_block.orientation == 0:
                                if e_block.orientation == 0:
                                    self.movements('R1 U1 R3 U3 R1 U1 R3 U3 R1 U1 R3')
                                    solution += ' R1 U1 R3 U3 R1 U1 R3 U3 R1 U1 R3'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('R1 U3 R3 F3 U2 F1')
                                    solution += ' R1 U3 R3 F3 U2 F1'
                                    break
                            elif c_block.orientation == 1:
                                if e_block.orientation == 0:
                                    self.movements('U3 R1 U3 R3 U2 R1 U3 R3')
                                    solution += ' U3 R1 U3 R3 U2 R1 U3 R3'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U3 R1 U1 R3 U1 F3 U3 F1')
                                    solution += ' U3 R1 U1 R3 U1 F3 U3 F1'
                                    break
                            elif c_block.orientation == 2:
                                if e_block.orientation == 0:
                                    self.movements('U1 F3 U1 F1 U2 F3 U1 F1')
                                    solution += ' U1 F3 U1 F1 U2 F3 U1 F1'
                                    break
                                elif e_block.orientation == 1:
                                    self.movements('U1 F3 U3 F1 U3 R1 U1 R3')
                                    solution += ' U1 F3 U3 F1 U3 R1 U1 R3'
                                    break
                break

        """ OOL (Orientation of the Last Layer) """
        temp = [self.edge_blocks[0].orientation,
                self.edge_blocks[1].orientation,
                self.edge_blocks[2].orientation,
                self.edge_blocks[3].orientation]
        # all edges oriented
        if temp == [0, 0, 0, 0]:
            pass
        # 2 adjacent edges oriented
        elif temp == [0, 0, 1, 1]:
            self.movements('B3 U3 R3 U1 R1 B1')
            solution += ' B3 U3 R3 U1 R1 B1'
        elif temp == [0, 1, 0, 1]:
            self.movements('L3 U3 B3 U1 B1 L1')
            solution += ' L3 U3 B3 U1 B1 L1'
        elif temp == [1, 0, 1, 0]:
            self.movements('R3 U3 F3 U1 F1 R1')
            solution += ' R3 U3 F3 U1 F1 R1'
        elif temp == [1, 1, 0, 0]:
            self.movements('F3 U3 L3 U1 L1 F1')
            solution += ' F3 U3 L3 U1 L1 F1'
        # 2 opposite edges oriented
        elif temp == [0, 1, 1, 0]:
            self.movements('L1 F1 U1 F3 U3 L3')
            solution += ' L1 F1 U1 F3 U3 L3'
        elif temp == [1, 0, 0, 1]:
            self.movements('F1 R1 U1 R3 U3 F3')
            solution += ' F1 R1 U1 R3 U3 F3'
        # no edges oriented
        elif temp == [1, 1, 1, 1]:
            self.movements('F1 R1 U1 R3 U3 F3 B1 U1 L1 U3 L3 B3')
            solution += ' F1 R1 U1 R3 U3 F3 B1 U1 L1 U3 L3 B3'

        temp = [self.corner_blocks[0].orientation,
                self.corner_blocks[1].orientation,
                self.corner_blocks[2].orientation,
                self.corner_blocks[3].orientation]
        # all corners oriented
        if temp == [0, 0, 0, 0]:
            pass
        # Sune
        elif temp == [0, 1, 1, 1]:
            self.movements('B1 U1 B3 U1 B1 U2 B3')
            solution += ' B1 U1 B3 U1 B1 U2 B3'
        elif temp == [1, 0, 1, 1]:
            self.movements('R1 U1 R3 U1 R1 U2 R3')
            solution += ' R1 U1 R3 U1 R1 U2 R3'
        elif temp == [1, 1, 0, 1]:
            self.movements('L1 U1 L3 U1 L1 U2 L3')
            solution += ' L1 U1 L3 U1 L1 U2 L3'
        elif temp == [1, 1, 1, 0]:
            self.movements('F1 U1 F3 U1 F1 U2 F3')
            solution += ' F1 U1 F3 U1 F1 U2 F3'
        elif temp == [0, 2, 2, 2]:
            self.movements('L3 U3 L1 U3 L3 U2 L1')
            solution += ' L3 U3 L1 U3 L3 U2 L1'
        elif temp == [2, 0, 2, 2]:
            self.movements('B3 U3 B1 U3 B3 U2 B1')
            solution += ' B3 U3 B1 U3 B3 U2 B1'
        elif temp == [2, 2, 0, 2]:
            self.movements('F3 U3 F1 U3 F3 U2 F1')
            solution += ' F3 U3 F1 U3 F3 U2 F1'
        elif temp == [2, 2, 2, 0]:
            self.movements('R3 U3 R1 U3 R3 U2 R1')
            solution += ' R3 U3 R1 U3 R3 U2 R1'
        #
        elif temp == [1, 2, 2, 1]:
            self.movements('R1 U2 R3 U3 R1 U1 R3 U3 R1 U3 R3')
            solution += ' R1 U2 R3 U3 R1 U1 R3 U3 R1 U3 R3'
        elif temp == [2, 1, 1, 2]:
            self.movements('F1 U2 F3 U3 F1 U1 F3 U3 F1 U3 F3')
            solution += ' F1 U2 F3 U3 F1 U1 F3 U3 F1 U3 F3'
        # Car
        elif temp == [1, 1, 2, 2]:
            self.movements('R1 U2 R2 U3 R2 U3 R2 U2 R1')
            solution += ' R1 U2 R2 U3 R2 U3 R2 U2 R1'
        elif temp == [1, 2, 1, 2]:
            self.movements('B1 U2 B2 U3 B2 U3 B2 U2 B1')
            solution += ' B1 U2 B2 U3 B2 U3 B2 U2 B1'
        elif temp == [2, 1, 2, 1]:
            self.movements('F1 U2 F2 U3 F2 U3 F2 U2 F1')
            solution += ' F1 U2 F2 U3 F2 U3 F2 U2 F1'
        elif temp == [2, 2, 1, 1]:
            self.movements('L1 U2 L2 U3 L2 U3 L2 U2 L1')
            solution += ' L1 U2 L2 U3 L2 U3 L2 U2 L1'
        # Superman
        elif temp == [0, 0, 2, 1]:
            self.movements('L2 D1 L3 U2 L1 D3 L3 U2 L3')
            solution += ' L2 D1 L3 U2 L1 D3 L3 U2 L3'
        elif temp == [0, 1, 0, 2]:
            self.movements('F2 D1 F3 U2 F1 D3 F3 U2 F3')
            solution += ' F2 D1 F3 U2 F1 D3 F3 U2 F3'
        elif temp == [1, 2, 0, 0]:
            self.movements('R2 D1 R3 U2 R1 D3 R3 U2 R3')
            solution += ' R2 D1 R3 U2 R1 D3 R3 U2 R3'
        elif temp == [2, 0, 1, 0]:
            self.movements('B2 D1 B3 U2 B1 D3 B3 U2 B3')
            solution += ' B2 D1 B3 U2 B1 D3 B3 U2 B3'
        # Superman 2
        elif temp == [0, 0, 1, 2]:
            self.movements('B3 R3 F1 R1 B1 R3 F3 R1')
            solution += ' B3 R3 F1 R1 B1 R3 F3 R1'
        elif temp == [0, 2, 0, 1]:
            self.movements('L3 B3 R1 B1 L1 B3 R3 B1')
            solution += ' L3 B3 R1 B1 L1 B3 R3 B1'
        elif temp == [1, 0, 2, 0]:
            self.movements('R3 F3 L1 F1 R1 F3 L3 F1')
            solution += ' R3 F3 L1 F1 R1 F3 L3 F1'
        elif temp == [2, 1, 0, 0]:
            self.movements('F3 L3 B1 L1 F1 L3 B3 L1')
            solution += ' F3 L3 B1 L1 F1 L3 B3 L1'
        #
        elif temp == [0, 1, 2, 0]:
            self.movements('L3 B1 L1 F3 L3 B3 L1 F1')
            solution += ' L3 B1 L1 F3 L3 B3 L1 F1'
        elif temp == [0, 2, 1, 0]:
            self.movements('R3 F1 R1 B3 R3 F3 R1 B1')
            solution += ' R3 F1 R1 B3 R3 F3 R1 B1'
        elif temp == [1, 0, 0, 2]:
            self.movements('F3 L1 F1 R3 F3 L3 F1 R1')
            solution += ' F3 L1 F1 R3 F3 L3 F1 R1'
        elif temp == [2, 0, 0, 1]:
            self.movements('B3 R1 B1 L3 B3 R3 B1 L1')
            solution += ' B3 R1 B1 L3 B3 R3 B1 L1'

        """ PLL (Permutation of the Last Layer) """
        # corners
        if self.corner_blocks[0].colors[2] == self.corner_blocks[1].colors[1]:
            if self.corner_blocks[1].colors[2] == self.corner_blocks[3].colors[1]:
                # correct
                pass
            else:
                self.movements('L3 B1 L3 F2 L1 B3 L3 F2 L2')
                solution += ' L3 B1 L3 F2 L1 B3 L3 F2 L2'
        elif self.corner_blocks[1].colors[2] == self.corner_blocks[3].colors[1]:
            self.movements('B3 R1 B3 L2 B1 R3 B3 L2 B2')
            solution += ' B3 R1 B3 L2 B1 R3 B3 L2 B2'
        elif self.corner_blocks[3].colors[2] == self.corner_blocks[2].colors[1]:
            self.movements('R3 F1 R3 B2 R1 F3 R3 B2 R2')
            solution += ' R3 F1 R3 B2 R1 F3 R3 B2 R2'
        elif self.corner_blocks[2].colors[2] == self.corner_blocks[0].colors[1]:
            self.movements('F3 L1 F3 R2 F1 L3 F3 R2 F2')
            solution += ' F3 L1 F3 R2 F1 L3 F3 R2 F2'
        else:
            self.movements('R1 B3 R3 F1 R1 B1 R3 F3 R1 B1 R3 F1 R1 B3 R3 F3')
            solution += ' R1 B3 R3 F1 R1 B1 R3 F3 R1 B1 R3 F1 R1 B3 R3 F3'
        # edges
        if self.edge_blocks[0].colors[1] == self.corner_blocks[0].colors[2]:
            if self.edge_blocks[1].colors[1] == self.corner_blocks[1].colors[2]:
                # correct
                pass
            elif self.edge_blocks[1].colors[1] == self.corner_blocks[2].colors[2]:
                # Ua Perm
                self.movements('L1 U3 L1 U1 L1 U1 L1 U3 L3 U3 L2')
                solution += ' L1 U3 L1 U1 L1 U1 L1 U3 L3 U3 L2'
            elif self.edge_blocks[1].colors[1] == self.corner_blocks[3].colors[2]:
                # Ub Perm
                self.movements('R3 U1 R3 U3 R3 U3 R3 U1 R1 U1 R2')
                solution += ' R3 U1 R3 U3 R3 U3 R3 U1 R1 U1 R2'
        elif self.edge_blocks[1].colors[1] == self.corner_blocks[1].colors[2]:
            if self.edge_blocks[2].colors[1] == self.corner_blocks[3].colors[2]:
                # Ua Perm
                self.movements('B1 U3 B1 U1 B1 U1 B1 U3 B3 U3 B2')
                solution += ' B1 U3 B1 U1 B1 U1 B1 U3 B3 U3 B2'
            elif self.edge_blocks[2].colors[1] == self.corner_blocks[0].colors[2]:
                # Ub Perm
                self.movements('F3 U1 F3 U3 F3 U3 F3 U1 F1 U1 F2')
                solution += ' F3 U1 F3 U3 F3 U3 F3 U1 F1 U1 F2'
        elif self.edge_blocks[2].colors[1] == self.corner_blocks[2].colors[2]:
            if self.edge_blocks[3].colors[1] == self.corner_blocks[1].colors[2]:
                # Ua Perm
                self.movements('F1 U3 F1 U1 F1 U1 F1 U3 F3 U3 F2')
                solution += ' F1 U3 F1 U1 F1 U1 F1 U3 F3 U3 F2'
            elif self.edge_blocks[3].colors[1] == self.corner_blocks[0].colors[2]:
                # Ub Perm
                self.movements('B3 U1 B3 U3 B3 U3 B3 U1 B1 U1 B2')
                solution += ' B3 U1 B3 U3 B3 U3 B3 U1 B1 U1 B2'
        elif self.edge_blocks[3].colors[1] == self.corner_blocks[3].colors[2]:
            if self.edge_blocks[0].colors[1] == self.corner_blocks[2].colors[2]:
                # Ua Perm
                self.movements('R1 U3 R1 U1 R1 U1 R1 U3 R3 U3 R2')
                solution += ' R1 U3 R1 U1 R1 U1 R1 U3 R3 U3 R2'
            elif self.edge_blocks[0].colors[1] == self.corner_blocks[1].colors[2]:
                # Ub Perm
                self.movements('L3 U1 L3 U3 L3 U3 L3 U1 L1 U1 L2')
                solution += ' L3 U1 L3 U3 L3 U3 L3 U1 L1 U1 L2'
        elif self.edge_blocks[0].colors[1] == self.corner_blocks[1].colors[2]:
            # Z Perm
            self.movements('L2 R2 D3 L2 R2 U3 L1 R3 F2 L2 R2 B2 L1 R3 U2')
            solution += ' L2 R2 D3 L2 R2 U3 L1 R3 F2 L2 R2 B2 L1 R3 U2'
        elif self.edge_blocks[0].colors[1] == self.corner_blocks[2].colors[2]:
            # Z Perm
            self.movements('L2 R2 D1 L2 R2 U1 L1 R3 F2 L2 R2 B2 L1 R3 U2')
            solution += ' L2 R2 D1 L2 R2 U1 L1 R3 F2 L2 R2 B2 L1 R3 U2'
        elif self.edge_blocks[0].colors[1] == self.corner_blocks[3].colors[2]:
            # H Perm
            self.movements('L2 R2 D1 L2 R2 U2 L2 R2 D1 L2 R2')
            solution += ' L2 R2 D1 L2 R2 U2 L2 R2 D1 L2 R2'
        # final step
        if self.edge_blocks[0].colors[1] == self.centers['f']:
            pass
        elif self.edge_blocks[1].colors[1] == self.centers['f']:
            self.movements('U3')
            solution += ' U3'
        elif self.edge_blocks[2].colors[1] == self.centers['f']:
            self.movements('U1')
            solution += ' U1'
        elif self.edge_blocks[3].colors[1] == self.centers['f']:
            self.movements('U2')
            solution += ' U2'

        """ simplify unnecessary steps """
        simplified = ''
        solution_list = solution.strip().split(' ')
        if len(solution_list) > 1:
            i = 0
            while i < len(solution_list) - 1:
                if solution_list[i][0] == solution_list[i + 1][0]:
                    if (solution_list[i][1] == '1' and solution_list[i + 1][1] == '1') or \
                            (solution_list[i][1] == '3' and solution_list[i + 1][1] == '3'):
                        simplified += ' ' + solution_list[i][0] + '2'
                    elif (solution_list[i][1] == '1' and solution_list[i + 1][1] == '2') or \
                            (solution_list[i][1] == '2' and solution_list[i + 1][1] == '1'):
                        simplified += ' ' + solution_list[i][0] + '3'
                    elif (solution_list[i][1] == '2' and solution_list[i + 1][1] == '3') or \
                            (solution_list[i][1] == '3' and solution_list[i + 1][1] == '2'):
                        simplified += ' ' + solution_list[i][0] + '1'
                    i += 1
                else:
                    simplified += ' ' + solution_list[i]
                i += 1
            try:
                simplified += ' ' + solution_list[i]
            except IndexError:
                pass
            return simplified
        else:
            return solution


def string_covert(color_str):
    result = ''
    color_dict = {color_str[ 4]: 'U',
                  color_str[31]: 'R',
                  color_str[22]: 'F',
                  color_str[49]: 'D',
                  color_str[13]: 'L',
                  color_str[40]: 'B'}
    for i in range(0, 9):
        result += color_dict[color_str[i]]
    for i in range(27, 36):
        result += color_dict[color_str[i]]
    for i in range(18, 27):
        result += color_dict[color_str[i]]
    for i in range(45, 54):
        result += color_dict[color_str[i]]
    for i in range(9, 18):
        result += color_dict[color_str[i]]
    for i in range(36, 45):
        result += color_dict[color_str[i]]
    return result


def six_to_five(solution_six: str):
    solution_five = ''
    sol = solution_six.split(' ')
    print(sol)
    for step in sol:
        if step == 'U1':
            solution_five += 'D3 R2 D3 F2 L2 R2 B2 D3 R2 F2 D2 L2 D2 B2 D2 F2 D2 L2 F2 '
        elif step == 'U2':
            solution_five += 'D1 F2 D1 R2 B2 F2 L2 D1 F2 R2 D2 B2 D2 L2 D2 R2 D2 B2 R2 D1 F2 D1 R2 B2 F2 L2 D1 F2 R2 D2 B2 D2 L2 D2 R2 D2 B2 R2 '
        elif step == 'U3':
            solution_five += 'D1 F2 D1 R2 B2 F2 L2 D1 F2 R2 D2 B2 D2 L2 D2 R2 D2 B2 R2 '
        else:
            solution_five += step + ' '
    print(solution_five)
    pass


if __name__ == '__main__':

    cube1 = Cube3x3()
    print('cube1 = Cube3x3()')
    print(cube1)

    while True:
        cube1.movements(input('Input any movements to scramble(e.g. \'U1 L3 D1 F3 D1 B2 R1 U2 L3\'): '))
        print(cube1)
        print(cube1.solve())
        print(cube1)
