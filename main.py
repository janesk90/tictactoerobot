"""
This is it, the main control loop for our robot.
"""
import board, strat, GridRead, symbol

currentCoordinates = (0,0) # it's an owl
b = board.Board()
s = strat.AlphaBetaStrat()

while not (b.isSolved() or b.isFull()):
    # wait for X input
    xMove = [0,0] # this is the X input we're getting from console, it should not be 0,0; it needs to be whatever the X coords are
    b.putX(*xMove)
    oMove = s.pickNextMove(b)
    currentCoordinates = GridRead.navigate(GridRead.lineCrossingModule, GridRead.lineFollowingModule, currentCoordinates, oMove)
    # we need to call the code to write a symbol in our current square, here