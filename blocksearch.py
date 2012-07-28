from board import *

def posToCategory(board, id, position, cats):
    map,size = board
    w,h = size
    x,y = position
    selfs, nonselfs, invalids, frees = cats
    if (x<0 or x>=w):
        invalids.append(position);
        return
    if (y<0 or y>=h):
        invalids.append(position);
        return

    if (map[position].id == 0):
        frees.append(position)
    elif (map[position].id == id):
        selfs.append(position)
    else:
        nonselfs.append(position)
    return

def checkSurrounding(board, position):
    map,size = board
    x,y = position
    selfid = map[position].id
    invalids = []
    selfs = []
    nonselfs = []
    frees = []

    posToCategory(board, selfid, (x-1,y), (selfs, nonselfs, invalids, frees))
    posToCategory(board, selfid, (x,y-1), (selfs, nonselfs, invalids, frees))
    posToCategory(board, selfid, (x+1,y), (selfs, nonselfs, invalids, frees))
    posToCategory(board, selfid, (x,y+1), (selfs, nonselfs, invalids, frees))

    return (selfs, nonselfs, invalids, frees)

def blockEnumerate(board, position, checkedList):
    map,size = board
    x,y = position
    checkedList.append(position)
    selfs,_,_,free = checkSurrounding(board, position)
    if (map[position].id == 0):
        selfs = selfs+free

    for pos in selfs:
        if (pos not in checkedList):
            blockEnumerate(board, pos, checkedList)
    return

def blockSizeSearch(board, position):
    map,size = board
    if (map[position].clean): return map[position].id
    return len(blockItemSearch(board, position))

def blockItemSearch(board, position):
    checkedList = []
    blockEnumerate(board, position, checkedList)
    return checkedList


def blockEnumerateForFrees(board, position, checkedList, freeList):
    checkedList.append(position)
    map,size = board
    x,y = position
    selfs,_,_,frees = checkSurrounding(board, position)
    num = len(frees)
    for pos in selfs:
        if (pos not in checkedList):
            num += blockEnumerateForFrees(board, pos, checkedList)
    return num

def blockFreeSearch(board, position):
    checkedList = []
    freeList = []
    blockEnumerateForFrees(board, position, checkedList, freeList)
    return freeList

def blockSquareSearch(board, position, id):
    map,size = board
    x,y = position
    xr,yr = range(x-id-1, x+id), range(y-id-1, y+id)

    for pos, block in map.items():
        xx,yy = pos
        if (xx in xr and yy in yr and block.id == id):  return 1