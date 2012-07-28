import StringIO
import sys
import time
from board import *
from solve import *


board = '''8
7 . 8 . . . . 8
. . 1 4 . . . .
1 . . 4 8 5 . 5
7 7 . 3 . 6 3 .
. . . 3 . . 4 .
. 2 . 6 . . 3 3
3 1 5 . . 6 6 .
2 . . 5 6 . . .'''

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