import pprint
import board, strat
b = board.Board()
b.putX(1,1)
b.putO(0,0)
b.putX(2,2)
b.putO(0,2)
b.putX(0,1)
b.putO(2,1)


print("INITIALIZE")
print(b.toString())
s = strat.AlphaBetaStrat()
vs = s.pickNextMove(b)
pprint.pprint(s.pickNextMove(b))