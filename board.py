EMPTY_SPACE = 0
X_VALUE = 1
O_VALUE = 2
class Board(object):
    boardArr = None
    def __init__(self, size=3):
        self.boardArr = []
        self.size = size
        self.history = []
        for i in range(size):
            self.boardArr.append([EMPTY_SPACE]*size)
    def getBoard(self): # warning this returns the actual board
        return self.boardArr
    def _put(self, row, col, val):
        self.boardArr[row][col] = val # this is on purpose
        # print("HISTORY")
        # print(self.history)
    def putX(self, row, col):
        self._put(row, col, X_VALUE)
        self.history.append((row, col))
    def putO(self, row, col):
        self._put(row, col, O_VALUE)
        self.history.append((row, col))
    def undo(self):
        position = self.history.pop()
        # print("HISTORY")
        # print(self.history)
        self._put(*position, EMPTY_SPACE)
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
    def whoWon(self):
        if not self.isSolved():
            return None
        else:
            if self._checkWinner(X_VALUE):
                return X_VALUE
            if self._checkWinner(O_VALUE):
                return O_VALUE
    def _checkWinner(self, player):
        t = [*zip(*self.boardArr)] # transpose the board
        for i in self.boardArr:
            if list(i) == [player]*len(self.boardArr):
                return True
        for i in t:
            if list(i) == [player]*len(self.boardArr):
                return True
        diag1 = [self.boardArr[i][i] for i in range(len(self.boardArr))]
        diag2 = [self.boardArr[i][len(self.boardArr)-1-i] for i in range(len(self.boardArr))]
        if diag1 == [player]*len(self.boardArr):
            return True
        if diag2 == [player]*len(self.boardArr):
            return True
        return False
    def isFull(self):
        count = 0
        for c in self.boardArr:
            for r in c:
                if r != EMPTY_SPACE:
                    count += 1
        return count == self.size**2
    def getEmptySquares(self):
        emptySquares = []
        for c in range(len(self.boardArr)):
            for r in range(len(self.boardArr[c])):
                if self.boardArr[c][r] == EMPTY_SPACE:
                    emptySquares.append((c,r))
        return emptySquares