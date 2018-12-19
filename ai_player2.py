from player import Player
import math as m
from copy import deepcopy
from time import time

class AIPlayer2(Player):
    """This player should implement a heuristic along with a min-max and alpha
    beta search to """

    def __init__(self):
        super().__init__()
        self.name = "FONTAINE Pierre"

    # Heuristique pour la variable x qui représente
    def heuristic(self, board,depth):

        def getAligmentPoints(line):
            points = [0,0,10,100,1000]
            total = 0
            x = 0
            o = 0
            for i in range(len(line)):
                if line[i] == -1:
                    if x == 4:
                        total += 1000
                        x = 0
                    else:
                        x+= 1
                else:
                    total += points[x]
                    x = 0
            total += points[x]
            for i in range(len(line)):
                if line[i] == 1:
                    if o == 4:
                        total -= 1000
                        o = 0
                    else:
                        o += 1
                else:
                    total -= points[o]
                    o = 0

            total -= points[o]
            n = len(line)
            for i in range(n-4):
                t = line[i:i+4]
                if t == [1,1,1,-1] or t == [-1,1,1,1] or t == [1,-1,1,1] or t== [1,1,-1,1]:
                    total += 500
                if [1,-1,1] in t or [1,1,-1] in t or [-1,1,-1] in t:
                    total += 50

            return total-500*depth

        total_points = 0
        for i in range(0,6):
            total_points += getAligmentPoints(board.getRow(i))
        for i in range(0,7):
            total_points += getAligmentPoints(board.getCol(i))
        for i in range(0,7):
            total_points += getAligmentPoints(board.getDiagonal(True,i))
        for i in range(0,7):
            total_points += getAligmentPoints(board.getDiagonal(False,i))

        return total_points

    def winningLine(self, line):
        if [-1, -1, -1, -1] in line: return True
        if [1, 1, 1, 1] in line: return True
        return False

    def winningGame(self, board):
        for i in range(0, 6):
            if self.winningLine(board.getRow(i)): return True
        for i in range(0, 7):
            if self.winningLine(board.getCol(i)): return True
        for i in range(0, 7):
            if self.winningLine(board.getDiagonal(True, i)): return True
        for i in range(0, 7):
            if self.winningLine(board.getDiagonal(False, i)): return True
        return False

    def maxValues(self,board,alpha,beta,player,depth):
        if depth<=0 or self.winningGame(board):
            return self.heuristic(board,depth)
        else:
            v = - m.inf
            for i in board.getPossibleColumns():
                sim = deepcopy(board)
                sim.play(player,i)
                v = max(v, self.minValues(sim,alpha,beta,-1*player,depth-1))
                if v >= beta: return v
                alpha = max(alpha,v)
            return v



    def minValues(self,board,alpha,beta,player,depth):
        if depth<=0 or self.winningGame(board):
            return self.heuristic(board,depth)
        else:
            v = m.inf
            for i in board.getPossibleColumns():
                sim = deepcopy(board)
                sim.play(player,i)
                v = min(v, self.maxValues(sim,alpha,beta,-1*player,depth-1))
                if v <= alpha:
                    return v
                beta = min(beta,v)
            return v

    def AlphaBetaDecision(self,board,player,depth):
        play = 0
        max_val = -m.inf
        for i in board.getPossibleColumns():
            sim = deepcopy(board)
            sim.play(player,i)
            val = self.minValues(sim,-m.inf,m.inf,-1*player,depth-1)
            if val > max_val:
                max_val = val
                play = i
        return(play)



    def getColumn(self, board):
        before_time = time()
        play = self.AlphaBetaDecision(board,self.color,4)
        after_time = time()
        return play

