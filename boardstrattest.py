import pprint
import board, strat
b = board.Board()
b.putX(1,1)
b.putO(0,1)
b.putX(2,2)
print("INITIALIZE")
print(b.toString())
s = strat.AlphaBetaStrat()
vs = s.pickNextMove(b)
pprint.pprint(s.pickNextMove(b))