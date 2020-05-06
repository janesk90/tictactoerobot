import random, pprint
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
        possibleNextMoves = b.getEmptySquares()
        random.shuffle(possibleNextMoves)
        return possibleNextMoves[0]
class AlphaBetaStrat(Strat):
    def _pickNextMove(self, b):
        possibleNextMoves = b.getEmptySquares()
        evals = []
        for m in possibleNextMoves:
            b.putO(*m)
            v = self.alphaBeta(b, 8, float("-inf"), float("inf"), False) # because the next person will be X, who is min
            b.undo()
            evals.append({"move": m, "val":v})
        return sorted(evals, key=lambda d: -d['val'])[0]['move']
    def eval(self, b):
        if b.whoWon() == board.X_VALUE:
            return -1
        elif b.whoWon() == board.O_VALUE:
            return 1
        else:
            return 0
    def alphaBeta(self, b, depth, alpha, beta, isMax):
        if depth == 0 or b.isSolved() or b.isFull():
            return self.eval(b)
        if isMax:
            value = float("-inf")
            for emptySquare in b.getEmptySquares():
                b.putO(*emptySquare)
                value = max([value, self.alphaBeta(b, depth-1, alpha, beta, False)])
                b.undo()
                alpha = max([alpha, value])
                if alpha >= beta:
                    break
            return value
        else:
            value = float("inf")
            for emptySquare in b.getEmptySquares():
                b.putX(*emptySquare)
                value = min([value, self.alphaBeta(b, depth-1, alpha, beta, True)])
                b.undo()
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value