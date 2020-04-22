EMPTY_SPACE = 0
X_VALUE = 1
O_VALUE = 2
class Board(object):
    boardArr = None
    def __init__(self, size=3):
        self.boardArr = []
        for i in range(size):
            self.boardArr.append([0]*size)
    def _put(self, row, col, val):
        self.boardArr[col][row] = val
    def putX(self, row, col):
        self._put(row, col, X_VALUE)
    def putO(self, row, col):
        self._put(row, col, O_VALUE)
    def toString(self):
        s = ""
        return str(self.boardArr)
b = Board(3)
b.putX(0,0)
b.putO(0,1)