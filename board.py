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
        self.boardArr[col][row] = val # this is on purpose
    def putX(self, row, col):
        self._put(row, col, X_VALUE)
    def putO(self, row, col):
        self._put(row, col, O_VALUE)
    def toString(self):
        s = ""
        for i in self.boardArr:
            for j in i:
                if j == X_VALUE:
                    s += "X"
                if j == O_VALUE:
                    s += "O"
                if j == EMPTY_SPACE:
                    s += "_"
                s += " "
            s += "\n"
        return s
    def isSolved(self):
        t = [*zip(*self.boardArr)] # transpose the board
        for i in self.boardArr:
            if list(i) == [X_VALUE]*len(self.boardArr) or list(i) == [O_VALUE]*len(self.boardArr):
                return True
        for i in t:
            if list(i) == [X_VALUE]*len(self.boardArr) or list(i) == [O_VALUE]*len(self.boardArr):
                return True
        diag1 = [self.boardArr[i][i] for i in range(len(self.boardArr))]
        diag2 = [self.boardArr[i][len(self.boardArr)-1-i] for i in range(len(self.boardArr))]
        if diag1 == [X_VALUE]*len(self.boardArr) or diag1 == [O_VALUE]*len(self.boardArr):
            return True
        if diag2 == [X_VALUE]*len(self.boardArr) or diag2 == [O_VALUE]*len(self.boardArr):
            return True
        return False
"""
b = Board(3)
b.putX(0,0)
b.putX(1,1)
b.putX(2,2)
b.putO(1,2)
print(b.isSolved())
print(b.toString())
"""