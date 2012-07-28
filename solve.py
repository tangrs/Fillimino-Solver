from board import *
from brute import *
from blocksearch import *
import sys
import time

def solve(board):
    map,size = board
    w,h = size
    startTime = time.time()
    timeLast = time.time()
    sys.stdout.write("[*] Solving all certain blocks... ")
    count = 1
    while (count>0):
        count = 0
        #print
        #printBoard(b)
        for position, obj in map.items():
            if (obj.id == 0):
                # Free
                _,nonselfs,_,frees = checkSurrounding(board, position)
                if (len(frees) == 0):
                    unsolvedId = -1
                    totalBlks = 0
                    for pos in nonselfs:
                        blkSize = blockSizeSearch(board,pos)
                        if (blkSize < map[pos].id):
                            if (unsolvedId < 0 or unsolvedId == map[pos].id):
                                totalBlks += blkSize
                                unsolvedId = map[pos].id
                            else:
                                unsolvedId = -1
                                break

                    if (unsolvedId > 0 and totalBlks < unsolvedId):
                        map[position].id = unsolvedId
                        count += 1

            else:
                # Piece
                selfs, nonselfs, invalids, frees = checkSurrounding(board, position)

                # Solve certain ones
                if (len(frees) == 1 \
                    and ( (obj.hasParent() and obj.parent in selfs) or len(selfs) == 0 ) \
                    and blockSizeSearch(board,position) < obj.id):

                    map[frees[0]].id = obj.id
                    map[frees[0]].parent = position
                    count+=1
    sys.stdout.write("[Done in {0:0.4f}s]\n".format(time.time()-timeLast))
    timeLast = time.time()
    sys.stdout.write("[*] Optimize slightly for bruteforcing... ")
    # Mark confirmed blocks as "clean" so block sizes aren't recomputed; builds list of incomplete blocks
    unfinishedBlocks = []
    for position, obj in map.items():
        if (obj.clean): continue
        blockList = blockItemSearch(board, position)
        if (len(blockList) == obj.id):
            for pos in blockList:
                map[pos].clean = 1
    sys.stdout.write("[Done in {0:0.4f}s]\n".format(time.time()-timeLast))
    timeLast = time.time()
    sys.stdout.write("[*] Sanity check to make sure everything is okay... ")
    if (not boardIsSoFarSoGood(board)):
        sys.stdout.write("[Fail]\n")
        return
    sys.stdout.write("[Done in {0:0.4f}s]\n".format(time.time()-timeLast))
    timeLast = time.time()
    sys.stdout.write("[*] Begin bruteforcing...\n")
    runBruteforce(board)
    printBoard(board)
    sys.stdout.write("\n[Bruteforced in {0:0.4f}s]\n".format(time.time()-timeLast))
    timeLast = time.time()
    sys.stdout.write("[*] Checking if solved board is valid... ")
    if (boardIsValid(board)):
        sys.stdout.write("[Success. Done in {0:0.4f}s]\n".format(time.time()-timeLast))
    else:
        sys.stdout.write("[Fail. Is it unsolvable?]\n")
    sys.stdout.write("[*] Total solving time: {0:0.4f}s\n".format(time.time()-startTime))
    return
