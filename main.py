"""
This is it, the main control loop for our robot.
"""
import board, strat, GridRead

currentCoordinates = (0,0) # it's an owl
b = board.Board()
s = strat.AlphaBetaStrat()

while not (b.isSolved() or b.isFull()):
    # wait for X input
    xMove = None # this is the X input we're getting from console, it should not be none
    b.putX(*move)
    oMove = s.pickNextMove(b)
    currentCoordinates = GridRead.navigate(GridRead.lineCrossingModule, GridRead.lineFollowingModule, currentCoordinates, oMove)