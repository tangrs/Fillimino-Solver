from blocksearch import *
from board import *
import time
import math

def shapeBruteforce(board, toCheck):
    map,size = board
    w,h = size
    if (len(toCheck)==0):
        if (boardIsValid(board)):
            printProgress(board, h)
            return 1
        else:
            return 0
    position = toCheck.pop()
    if (shapeCreate(board, position, toCheck, [], blockItemSearch(board, position) )): return 1
    toCheck.append(position)
    return 0

def printProgress(board, h):
    global bruteforceStartTime
    global lastCheckedTime
    lastCheckedTime = time.time()
    printBoard(board)
    sys.stdout.write("[*] Generated {0} shapes at {1:0.1f} shapes/second.\033[{2};A\r".format(bruteforceCount, bruteforceCount / (time.time()-bruteforceStartTime),h))

def shapeCreate(board, position, toCheck, shapesCache, blockItemsCache):
    map,size = board
    w,h = size
    blockItems = blockItemsCache
    id = map[position].id
    if (len(blockItems) > id): return 0
    elif (len(blockItems) == id):
        global bruteforceCount
        bruteforceCount += 1
        if ((time.time()-lastCheckedTime) > 0.5):
            printProgress(board, h)
        if (set(blockItems) in shapesCache): return 0
        shapesCache.append(set(blockItems))
        if (shapeBruteforce(board, toCheck)):
            return 1
    else:
        _,_,_,frees = checkSurrounding(board, position)
        for block in blockItems:
            _,_,_,free = checkSurrounding(board, block)
            if (len(free) > 0): frees = list(set(free) | set(frees))
        if (frees < id-len(blockItems)): return 0
        for pos in frees:
            map[pos].id = id
            selfs,_,_,_ = checkSurrounding(board, pos)
            if (len(selfs) > 1):
                if (shapeCreate(board, pos, toCheck, shapesCache, blockItemSearch(board, pos))): return 1
            else:
                blockItems.append(pos)
                if (shapeCreate(board, pos, toCheck, shapesCache, blockItems)): return 1
                blockItems.remove(pos)
            map[pos].id = 0
    return 0

def runBruteforce(board):
    map,size = board
    w,h = size
    toCheck = {}
    maxn = max(w,h)
    global bruteforceCount
    global bruteforceStartTime
    global lastCheckedTime
    bruteforceCount=0
    bruteforceStartTime = time.time()
    lastCheckedTime = 0
    for key, obj in map.items():
        if (obj.id != 0 and obj.clean == 0):
            toCheck[key] = obj.id
    # Smaller blocks have less combinations so are more likely to be right on the first try
    toCheck = sorted(toCheck, lambda x,y: cmp(map[x].id, map[y].id) )
    return shapeBruteforce(board, toCheck)