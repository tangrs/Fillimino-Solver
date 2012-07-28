from blocksearch import *
import sys
import string

class boardPiece():
    def __init__(self, id):
        self.id = id;
        self.parent = (-1,-1)
        self.clean = 0
    def hasParent(self):
        return not (self.parent == (-1,-1))

def boardIsValid(board):
    map,size = board
    for key, val in map.items():
        if (val.clean): continue
        if (val.id == 0): return 0
        blkSize = blockSizeSearch(board, key)
        if (blkSize != val.id):
            return 0
    return 1

def boardIsSoFarSoGood(board):
    map,size = board
    for key, val in map.items():
        blkSize = blockSizeSearch(board, key)
        if (val.id != 0 and blkSize > val.id):
            print "Invalid block at {0}. Expected {1} got {2}".format(key, val.id, blkSize)
            return 0
    return 1

def emptyBoard(size):
    board = {}
    w,h = size

    while (h>0):
        i = w
        while (i>0):
            board[(i-1,h-1)] = boardPiece(0)
            i-=1
        h-=1
    return (board, size)

def printBoard(board):
    map,size = board
    w,h = size
    y=0
    while (y<h):
        x = 0
        while (x<w):
            if (map[(x,y)].id == 0):
                sys.stdout.write(". ")
            else:
                sys.stdout.write("{0} ".format( map[(x,y)].id ))
            x+=1
        sys.stdout.write("\n");
        y+=1