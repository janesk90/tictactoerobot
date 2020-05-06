import random
import board

class Strat(object):
    def __init__(self):
        pass
    def pickNextMove(self, b):
        if b.isSolved() or b.isFull():
            return None
        return self._pickNextMove(b)
    def _pickNextMove(self, b):
        raise NotImplementedError("_pickNextMove is abstract, please use a subclass of Strat which implements _pickNextMove(self)")
class RandomStrat(Strat):
    def _pickNextMove(self, b):
        possibleNextMoves = []
        for c in range(len(b.getBoard())):
            for r in range(len(b.getBoard()[c])):
                if b.getBoard()[c][r] == board.EMPTY_SPACE:
                    possibleNextMoves.append((c,r))
        random.shuffle(possibleNextMoves)
        return possibleNextMoves[0]

b = board.Board()
s = RandomStrat()
print(s.pickNextMove(b))