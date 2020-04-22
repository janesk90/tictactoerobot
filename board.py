EMPTY_SPACE = 0
X_VALUE = 1
O_VALUE = 2
class Board(object):
    boardArr = None
    def __init__(self, size=3):
        self.boardArr = [[EMPTY_SPACE]*size]*size
    def putX(self, row, col):
        self.boardArr[row][col] = X_VALUE
    def putO(self, row, col):
        self.boardArr[row][col] = O_VALUE
    def toString(self):
        s = ""
        return str(self.boardArr)
b = Board(3)
b.putX(0,0)
b.putO(0,1)
print(b.toString())