import StringIO
import sys
import time
from board import *
from solve import *


board = '''5
4 . . . .
1 . 2 3 .
. 4 5 . .
. 6 1 5 3
. . 6 3 .
'''

fp = StringIO.StringIO(board)

def readLine():
    return fp.readline();
def readBoard():
    l = int(readLine())
    size = (l, l)
    map = {}
    y = 0
    while (y<l):
        line = readLine()
        x = 0
        i = 0
        while (x<l):
            if (line[i].isdigit()):
                map[(x,y)] = boardPiece(int(line[i]));
                x+=1
            if (line[i] == "."):
                map[(x,y)] = boardPiece(0);
                x+=1
            i+=1

        y+=1
    return (map, size)

b=readBoard()
solve(b)