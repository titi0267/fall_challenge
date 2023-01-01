import sys
import math
from enum import IntEnum, Enum
from random import choice, randint
import operator

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

width, height = [int(i) for i in input().split()]

class Dir(IntEnum):
    UP= -1
    DOWN= 1
    RIGHT= 1
    LEFT= -1

class Action(Enum):
    MOVE = 1
    SPAWN = 2
    BUILD = 3

class Field:
    scrap = 0,
    own= 0,
    units= 0,
    recycler= 0,
    build= 0,
    spawn= 0,
    in_range= 0

    def __init__(self, scrap, own, units, recycler, build, spawn, in_range) -> None:
        self.scrap = scrap
        self.own = own
        self.units = units
        self.recycler = recycler
        self.build = build
        self.spawn = spawn
        self.in_range = in_range

def getParams(params: list):
    my_matter, opp_matter = [int(i) for i in input().split()]
    my_tiles, opp_tiles = 0,0
    for i in range(height):
        params.append([])
        for j in range(width):
            scrap, own, units, recycler, build, spawn, in_range = [int(k) for k in input().split()]
            params[i].append(Field(scrap, own, units, recycler, build, spawn, in_range))
            if own == 1:
                my_tiles += 1
            elif own == 0:
                opp_tiles += 1
    return (params, [my_matter, my_tiles], (opp_matter, opp_tiles))

def freeParams(params: list) -> None:
    for i in range(len(params)):
        for h in range(len(params[i])):
            del params[i][0]

def mapNextTurn(params: tuple[list[list[Field]], list[int], tuple[int, int]]):
    tiles = params[0]
    for i in range(len(tiles)):
        for h in range(len(tiles[i])):
            if (tiles[i][h].in_range == 1):
                tiles[i][h].scrap -= 1
    return tiles

def tilesToExclude(tileLeft: Field or None, tileRight: Field or None, tileUp: Field or None, tileDown: Field or None, already: list[int]) -> list:
    exclude = already
    if tileUp != None:
        if (tileUp.scrap == 0 or tileUp.recycler == 1):
            exclude.append(1)
    if tileRight != None:
        if (tileRight.scrap == 0 or tileRight.recycler == 1):
            exclude.append(2)
    if tileDown != None:
        if (tileDown.scrap == 0 or tileDown.recycler == 1):
            exclude.append(3)
    if tileLeft != None:
        if (tileLeft.scrap == 0 or tileLeft.recycler == 1):
            exclude.append(4)
    return exclude

def selectTiles(tileLeft: Field or None, tileRight: Field or None, tileUp: Field or None, tileDown: Field or None, tileType: int):
    tileTypeArray = []
    if tileUp != None and tileUp.own == tileType and tileUp.recycler == 0:
        tileTypeArray.append(1)
    if tileRight != None and tileRight.own == tileType and tileRight.recycler == 0:
        tileTypeArray.append(2)
    if tileDown != None and tileDown.own == tileType and tileDown.recycler == 0:
        tileTypeArray.append(3)
    if tileLeft != None and tileLeft.own == tileType and tileLeft.recycler == 0:
        tileTypeArray.append(4)
    return tileTypeArray

def nearestOppCell(tiles: list[list[Field]], i: int, j: int):
    minLen = 1000
    newMinLen = 1000
    tileToGo = [-1, -1]
    for a in range(0, len(tiles)):
        for b in range(0, len(tiles[a])):
            if tiles[a][b].own == 0 and tiles[a][b].recycler == 0:
                newMinLen = math.sqrt(math.pow((a - i), 2) + math.pow((b - j), 2))
                if newMinLen < minLen:
                    minLen = newMinLen
                    tileToGo[0] = b
                    tileToGo[1] = a
    if tileToGo[0] != -1:
        return tileToGo
    return [0,0]


def priorityMovment(tileLeft: Field or None, tileRight: Field or None, tileUp: Field or None, tileDown: Field or None, exclude: list):
    opponentTile = []
    myTiles = []
    freeTiles = []
    opponentTile = selectTiles(tileLeft, tileRight, tileUp, tileDown, 0)
    myTiles = selectTiles(tileLeft, tileRight, tileUp, tileDown, 1)
    freeTiles = selectTiles(tileLeft, tileRight, tileUp, tileDown, -1)
    for i in exclude:
        if i in opponentTile:
            opponentTile.remove(i)
        if i in freeTiles:
            freeTiles.remove(i)
        if i in myTiles:
            myTiles.remove(i)
    if len(exclude) == 4: #No possible movment
        return 0
    elif (len(opponentTile) != 0): #Possible movment on opponent tile
        totalUnits = oppBotsAround(tileLeft, tileRight, tileUp, tileDown, opponentTile)
        if totalUnits[1] != 0:
            return totalUnits
        return(choice(opponentTile))
    elif (len(freeTiles) != 0): #Possible movment on free tile
        return(choice(freeTiles))
    elif (len(myTiles) != 0): #Only possible movment on my tile
        return (-1)

def oppBotsAround(tileLeft: Field or None, tileRight: Field or None, tileUp: Field or None, tileDown: Field or None, oppTiles: list):
    totalUnitsAround = 0
    whereAreThey = 0
    for i in range(0, len(oppTiles)):
        if oppTiles[i] == 1: #Check Bots up
            if (tileUp.units > 0):
                whereAreThey = 1
            totalUnitsAround += tileUp.units
        if oppTiles[i] == 2: #Check Bots right
            if whereAreThey == 0 or (whereAreThey == 1 and tileUp.units >= tileRight.units):
                whereAreThey = 2
            totalUnitsAround += tileRight.units
        if oppTiles[i] == 3: #Check Bots down
            if whereAreThey == 0 or ((whereAreThey == 1 and tileUp.units >= tileDown.units) or (whereAreThey == 2 and tileRight.units >= tileDown.units)):
                whereAreThey = 3
            totalUnitsAround += tileDown.units
        if oppTiles[i] == 4: #Check Bots left
            if whereAreThey == 0 or ((whereAreThey == 1 and tileUp.units >= tileLeft.units) or (whereAreThey == 2 and tileRight.units >= tileLeft.units) or (whereAreThey == 3 and tileDown.units >= tileLeft.units)):
                whereAreThey = 4
            totalUnitsAround += tileLeft.units
    return [-1, totalUnitsAround, whereAreThey]

def prioritySpawn(tileLeft: Field or None, tileRight: Field or None, tileUp: Field or None, tileDown: Field or None, exclude: list, loopedNumber: int):
    opponentTile = []
    myTiles = []
    freeTiles = []
    opponentTile = selectTiles(tileLeft, tileRight, tileUp, tileDown, 0)
    myTiles = selectTiles(tileLeft, tileRight, tileUp, tileDown, 1)
    freeTiles = selectTiles(tileLeft, tileRight, tileUp, tileDown, -1)
    for i in exclude:
        if i in opponentTile:
            opponentTile.remove(i)
        if i in freeTiles:
            freeTiles.remove(i)
        if i in myTiles:
            myTiles.remove(i)
    if len(exclude) == 4:
        return False
    elif (len(opponentTile) != 0 and loopedNumber == 0): #Spawn near to opponent tile with bots on it
        totalUnits = oppBotsAround(tileLeft, tileRight, tileUp, tileDown, opponentTile)
        if totalUnits[1] != 0:
            return [True, totalUnits]
    elif (len(opponentTile) != 0 and loopedNumber == 1): #Spawn near to opponent tile
        return True
    elif (len(freeTiles) != 0 and loopedNumber == 2): #Spawn near to free tile
        return True
    elif (len(myTiles) != 0 and loopedNumber == 3): #Spawn near to my tile
        return True
    return False

def priorityBuild(tileLeft: Field or None, tileRight: Field or None, tileUp: Field or None, tileDown: Field or None, matter: int):
    opponentTile = []
    opponentTile = selectTiles(tileLeft, tileRight, tileUp, tileDown, 0)
    if (len(opponentTile) != 0): #Opponent tile near to my tile
        totalUnits = oppBotsAround(tileLeft, tileRight, tileUp, tileDown, opponentTile)
        if totalUnits[1] != 0 and totalUnits[1] >= int(matter/10): #Build to block opponent units
            return True
    return False

def checkAround(tiles: list[list[Field]], i: int, j: int, actionType: Action, loopedNumber: int, matter: int): #UP 1 | RIGHT 2 | DOWN 3 | LEFT 4
    try:
        if (i == 0 or j == 0 or i == len(tiles)-1 or j == len(tiles[i])-1):
            raise IndexError
        exclude = tilesToExclude(tiles[i][j+int(Dir.LEFT)], tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], tiles[i+int(Dir.DOWN)][j], [])
        if (actionType == Action["SPAWN"]):
            ableToSpawn = prioritySpawn(tiles[i][j+int(Dir.LEFT)], tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], tiles[i+int(Dir.DOWN)][j], exclude, loopedNumber)
            return ableToSpawn
        elif (actionType == Action["MOVE"]):
            bestMove = priorityMovment(tiles[i][j+int(Dir.LEFT)], tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], tiles[i+int(Dir.DOWN)][j], exclude)
            if bestMove == -1:
                goToOppTile = nearestOppCell(tiles, i, j)
                return goToOppTile
            return (bestMove)
        elif (actionType == Action["BUILD"]):
            needRecycler = priorityBuild(tiles[i][j+int(Dir.LEFT)], tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], tiles[i+int(Dir.DOWN)][j], matter)
            return needRecycler
    except IndexError:
        if i == 0:
            if j == 0:#UP LEFT
                exclude = tilesToExclude(None, tiles[i][j+int(Dir.RIGHT)], None, tiles[i+int(Dir.DOWN)][j], [1, 4])
                if (actionType == Action["MOVE"]):
                    bestMove = priorityMovment(None, tiles[i][j+int(Dir.RIGHT)], None, tiles[i+int(Dir.DOWN)][j], exclude)
                    if bestMove == -1:
                        goToOppTile = nearestOppCell(tiles, i, j)
                        return goToOppTile
                    return bestMove
                elif (actionType == Action["SPAWN"]):
                    ableToSpawn = prioritySpawn(None, tiles[i][j+int(Dir.RIGHT)], None, tiles[i+int(Dir.DOWN)][j], exclude, loopedNumber)
                    return ableToSpawn
                elif (actionType == Action["BUILD"]):
                    needRecycler = priorityBuild(None, tiles[i][j+int(Dir.RIGHT)], None, tiles[i+int(Dir.DOWN)][j], matter)
                    return needRecycler
            elif j == len(tiles[i])-1:#UP RIGHT
                exclude = tilesToExclude(tiles[i][j+int(Dir.LEFT)], None, None, tiles[i+int(Dir.DOWN)][j], [1, 2])
                if (actionType == Action["MOVE"]):
                    bestMove = priorityMovment(tiles[i][j+int(Dir.LEFT)], None, None, tiles[i+int(Dir.DOWN)][j], exclude)
                    if bestMove == -1:
                        goToOppTile = nearestOppCell(tiles, i, j)
                        return goToOppTile
                    return(bestMove)
                elif (actionType == Action["SPAWN"]):
                    ableToSpawn = prioritySpawn(tiles[i][j+int(Dir.LEFT)], None, None, tiles[i+int(Dir.DOWN)][j], exclude, loopedNumber)
                    return(ableToSpawn)
                elif (actionType == Action["BUILD"]):
                    needRecycler = priorityBuild(tiles[i][j+int(Dir.LEFT)], None, None, tiles[i+int(Dir.DOWN)][j], matter)
                    return needRecycler
            else:#UP
                exclude = tilesToExclude(tiles[i][j+int(Dir.LEFT)], tiles[i][j+int(Dir.RIGHT)], None, tiles[i+int(Dir.DOWN)][j], [1])
                if (actionType == Action["MOVE"]):
                    bestMove = priorityMovment(tiles[i][j+int(Dir.LEFT)], tiles[i][j+int(Dir.RIGHT)], None, tiles[i+int(Dir.DOWN)][j], exclude)
                    if bestMove == -1:
                        goToOppTile = nearestOppCell(tiles, i, j)
                        return goToOppTile
                    return(bestMove)
                elif (actionType == Action["SPAWN"]):
                    ableToSpawn = prioritySpawn(tiles[i][j+int(Dir.LEFT)], tiles[i][j+int(Dir.RIGHT)], None, tiles[i+int(Dir.DOWN)][j], exclude, loopedNumber)
                    return(ableToSpawn)
                elif (actionType == Action["BUILD"]):
                    needRecycler = priorityBuild(tiles[i][j+int(Dir.LEFT)], tiles[i][j+int(Dir.RIGHT)], None, tiles[i+int(Dir.DOWN)][j], matter)
                    return needRecycler
        if i == len(tiles)-1:
            if j == 0:#DOWN LEFT
                exclude = tilesToExclude(None, tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], None, [3, 4])
                if (actionType == Action["MOVE"]):
                    bestMove = priorityMovment(None, tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], None, exclude)
                    if bestMove == -1:
                        goToOppTile = nearestOppCell(tiles, i, j)
                        return goToOppTile
                    return(bestMove)
                elif (actionType == Action["SPAWN"]):
                    ableToSpawn = prioritySpawn(None, tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], None, exclude, loopedNumber)
                    return(ableToSpawn)
                elif (actionType == Action["BUILD"]):
                    needRecycler = priorityBuild(None, tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], None, matter)
                    return needRecycler
            elif j == len(tiles[i])-1:#DOWN RIGHT
                exclude = tilesToExclude(tiles[i][j+int(Dir.LEFT)], None, tiles[i+int(Dir.UP)][j], None, [2, 3])
                if (actionType == Action["MOVE"]):
                    bestMove = priorityMovment(tiles[i][j+int(Dir.LEFT)], None, tiles[i+int(Dir.UP)][j], None, exclude)
                    if bestMove == -1:
                        goToOppTile = nearestOppCell(tiles, i, j)
                        return goToOppTile
                    return(bestMove)
                elif (actionType == Action["SPAWN"]):
                    ableToSpawn = prioritySpawn(tiles[i][j+int(Dir.LEFT)], None, tiles[i+int(Dir.UP)][j], None, exclude, loopedNumber)
                    return(ableToSpawn)
                elif (actionType == Action["BUILD"]):
                    needRecycler = priorityBuild(tiles[i][j+int(Dir.LEFT)], None, tiles[i+int(Dir.UP)][j], None, matter)
                    return needRecycler
            else:#DOWN
                exclude = tilesToExclude(tiles[i][j+int(Dir.LEFT)], tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], None, [3])
                if (actionType == Action["MOVE"]):
                    bestMove = priorityMovment(tiles[i][j+int(Dir.LEFT)], tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], None, exclude)
                    if bestMove == -1:
                        goToOppTile = nearestOppCell(tiles, i, j)
                        return goToOppTile
                    return(bestMove)
                elif (actionType == Action["SPAWN"]):
                    ableToSpawn = prioritySpawn(tiles[i][j+int(Dir.LEFT)], tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], None, exclude, loopedNumber)
                    return(ableToSpawn)
                elif (actionType == Action["BUILD"]):
                    needRecycler = priorityBuild(tiles[i][j+int(Dir.LEFT)], tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], None, matter)
                    return needRecycler
        elif j == 0:#LEFT
            exclude = tilesToExclude(None, tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], tiles[i+int(Dir.DOWN)][j], [4])
            if (actionType == Action["MOVE"]):
                bestMove = priorityMovment(None, tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], tiles[i+int(Dir.DOWN)][j], exclude)
                if bestMove == -1:
                    goToOppTile = nearestOppCell(tiles, i, j)
                    return goToOppTile
                return(bestMove)
            elif (actionType == Action["SPAWN"]):
                ableToSpawn = prioritySpawn(None, tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], tiles[i+int(Dir.DOWN)][j], exclude, loopedNumber)
                return(ableToSpawn)
            elif (actionType == Action["BUILD"]):
                needRecycler = priorityBuild(None, tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], tiles[i+int(Dir.DOWN)][j], matter)
                return needRecycler
        else:#RIGHT
            exclude = tilesToExclude(tiles[i][j+int(Dir.LEFT)], None, tiles[i+int(Dir.UP)][j], tiles[i+int(Dir.DOWN)][j], [2])
            if (actionType == Action["MOVE"]):
                bestMove = priorityMovment(tiles[i][j+int(Dir.LEFT)], None, tiles[i+int(Dir.UP)][j], tiles[i+int(Dir.DOWN)][j], exclude)
                if bestMove == -1:
                    goToOppTile = nearestOppCell(tiles, i, j)
                    return goToOppTile
                return(bestMove)
            elif (actionType == Action["SPAWN"]):
                ableToSpawn = prioritySpawn(tiles[i][j+int(Dir.LEFT)], None, tiles[i+int(Dir.UP)][j], tiles[i+int(Dir.DOWN)][j], exclude, loopedNumber)
                return(ableToSpawn)
            elif (actionType == Action["BUILD"]):
                needRecycler = priorityBuild(tiles[i][j+int(Dir.LEFT)], None, tiles[i+int(Dir.UP)][j], tiles[i+int(Dir.DOWN)][j], matter)
                return needRecycler

def move(params: tuple[list[list[Field]], list[int], tuple[int, int]]):
    tiles = params[0]
    for i in range(len(tiles)):
        for j in range(len(tiles[i])):
            if tiles[i][j].own == 1 and tiles[i][j].units > 0:
                moveTo = checkAround(tiles, i, j, Action["MOVE"], 0, params[1][0])
                if (type(moveTo) == list and moveTo[0] != -1):
                    print("MOVE", str(tiles[i][j].units), str(j), str(i), str(moveTo[0]), str(moveTo[1]) +";", end="")
                elif (type(moveTo) == list and moveTo[0] == -1):
                    if moveTo[2] == 1:
                        print("MOVE", str(tiles[i][j].units), str(j), str(i), str(j), str(i-1) +";", end="")
                    if moveTo[2] == 2:
                        print("MOVE", str(tiles[i][j].units), str(j), str(i), str(j+1), str(i)+";", end="")
                    if moveTo[2] == 3:
                        print("MOVE", str(tiles[i][j].units), str(j), str(i), str(j), str(i+1)+";", end="")
                    if moveTo[2] == 4:
                        print("MOVE", str(tiles[i][j].units), str(j), str(i), str(j-1), str(i)+";", end="")
                else:
                    if moveTo == 1: #Move Up
                        print("MOVE", str(tiles[i][j].units), str(j), str(i), str(j), str(i-1) +";", end="")
                    if moveTo == 2: #Move Right
                        print("MOVE", str(tiles[i][j].units), str(j), str(i), str(j+1), str(i)+";", end="")
                    if moveTo == 3: #Move Down
                        print("MOVE", str(tiles[i][j].units), str(j), str(i), str(j), str(i+1)+";", end="")
                    if moveTo == 4: #Move Left
                        print("MOVE", str(tiles[i][j].units), str(j), str(i), str(j-1), str(i)+";", end="")

def spawn(params: tuple[list[list[Field]], list[int], tuple[int, int]]):
    tiles = params[0]
    tempMatter = [{'pos': [-1, -1], 'cost': -1}]
    totalMatter = params[1][0]
    for loopedNumber in range(0, 4):
        for i in range(len(tiles)):
            for j in range(len(tiles[i])):
                if tiles[i][j].own == 1:
                    spawnHere = checkAround(tiles, i, j, Action["SPAWN"], loopedNumber, params[1][0])
                    if type(spawnHere) == list:
                        tempMatter.append({'pos': [j, i], 'cost': 10*spawnHere[1][1]})
    tempMatter.sort(key=operator.itemgetter('cost'))
    tempMatter.pop(0)
    potentialCost = 0
    for g in range(len(tempMatter)):
        potentialCost += tempMatter[g]['cost']
    recyclerCost = (len(tempMatter)-1)*10
    for d in range(0, len(tempMatter)):
        if (recyclerCost >= totalMatter): #Not or just enough matter to block opponent everywhere
            return (totalMatter, tempMatter, d)
        if (totalMatter < int(tempMatter[d]['cost']/10)):
            return (totalMatter, tempMatter, d)
        print("SPAWN", str(int(tempMatter[d]['cost']/10)), str(tempMatter[d]['pos'][0]), str(tempMatter[d]['pos'][1])+";", end="")
        totalMatter -= tempMatter[d]['cost']
        recyclerCost -= tempMatter[d]['cost']
    return (totalMatter, tempMatter, -1)
        #elif spawnHere == True:
        #    print("SPAWN", str(math.floor(params[1][0]/10)), str(j), str(i)+";", end="")
        #    params[1][0] -= (10*math.floor(params[1][0]/10))
        #    if params[1][0] < 10:
        #        return params

def build(params: tuple[list[list[Field]], list[int], tuple[int, int]], matterNeeded: list[dict[str, int]]):
    tiles = params[0]
    for i in range(len(matterNeeded)):
        if params[1][0] < 10:
            return params
        print("BUILD", str(matterNeeded[i]['pos'][0]), str(matterNeeded[i]['pos'][1])+";", end="")
        params[1][0] -= 10
    #for i in range(len(tiles)):
    #    for j in range(len(tiles[i])):
    #        if tiles[i][j].own == 1 and tiles[i][j].build == 1:
    #            buildHere = checkAround(tiles, i, j, Action["BUILD"], 0, params[1][0])
    #            if buildHere == True:
    #                print("BUILD", str(j), str(i)+";", end="")
    #                params[1][0] -= 10
    #                params[0][i][j].recycler = 1
    #                if params[1][0] < 10:
    #                    return params
    return params

# game loop
def main():
    turns = 0
    while True:
        params = ([], [0, 0], (0, 0))
        params = getParams(params[0])
        (totalMatter, matterNeeded, index) = spawn(params)
        params[1][0] = totalMatter
        if index != -1:
            params = build(params, matterNeeded[index:])
        # if (turns == 0):
        #     for i in range(len(params[0])):
        #         for j in range(len(params[0][i])):
        #             if (params[0][i][j].build == 1):
        #                 print("BUILD", str(j), str(i)+";", end="")
        #                 params[1][0] -= 10
        # turns+=1
        move(params)
        freeParams(params[0])
        print("WAIT")

main()

#######################################################


import sys
import math
from enum import IntEnum, Enum
from random import choice, randint
import operator

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

width, height = [int(i) for i in input().split()]

class Dir(IntEnum):
    UP= -1
    DOWN= 1
    RIGHT= 1
    LEFT= -1

class Action(Enum):
    MOVE = 1
    SPAWN = 2
    BUILD = 3

class Field:
    scrap = 0,
    own= 0,
    units= 0,
    recycler= 0,
    build= 0,
    spawn= 0,
    in_range= 0

    def __init__(self, scrap, own, units, recycler, build, spawn, in_range) -> None:
        self.scrap = scrap
        self.own = own
        self.units = units
        self.recycler = recycler
        self.build = build
        self.spawn = spawn
        self.in_range = in_range

def getParams(params: list):
    my_matter, opp_matter = [int(i) for i in input().split()]
    my_tiles, opp_tiles = 0,0
    for i in range(height):
        params.append([])
        for j in range(width):
            scrap, own, units, recycler, build, spawn, in_range = [int(k) for k in input().split()]
            params[i].append(Field(scrap, own, units, recycler, build, spawn, in_range))
            if own == 1:
                my_tiles += 1
            elif own == 0:
                opp_tiles += 1
    return (params, [my_matter, my_tiles], (opp_matter, opp_tiles))

def freeParams(params: list) -> None:
    for i in range(len(params)):
        for h in range(len(params[i])):
            del params[i][0]

def mapNextTurn(params: tuple[list[list[Field]], list[int], tuple[int, int]]):
    tiles = params[0]
    for i in range(len(tiles)):
        for h in range(len(tiles[i])):
            if (tiles[i][h].in_range == 1):
                tiles[i][h].scrap -= 1
    return tiles

def tilesToExclude(tileLeft: Field or None, tileRight: Field or None, tileUp: Field or None, tileDown: Field or None, already: list[int]) -> list:
    exclude = already
    if tileUp != None:
        if (tileUp.scrap == 0 or tileUp.recycler == 1):
            exclude.append(1)
    if tileRight != None:
        if (tileRight.scrap == 0 or tileRight.recycler == 1):
            exclude.append(2)
    if tileDown != None:
        if (tileDown.scrap == 0 or tileDown.recycler == 1):
            exclude.append(3)
    if tileLeft != None:
        if (tileLeft.scrap == 0 or tileLeft.recycler == 1):
            exclude.append(4)
    return exclude

def selectTiles(tileLeft: Field or None, tileRight: Field or None, tileUp: Field or None, tileDown: Field or None, tileType: int):
    tileTypeArray = []
    if tileUp != None and tileUp.own == tileType and tileUp.recycler == 0:
        tileTypeArray.append(1)
    if tileRight != None and tileRight.own == tileType and tileRight.recycler == 0:
        tileTypeArray.append(2)
    if tileDown != None and tileDown.own == tileType and tileDown.recycler == 0:
        tileTypeArray.append(3)
    if tileLeft != None and tileLeft.own == tileType and tileLeft.recycler == 0:
        tileTypeArray.append(4)
    return tileTypeArray

def nearestOppCell(tiles: list[list[Field]], i: int, j: int):
    minLen = 1000
    newMinLen = 1000
    tileToGo = [-1, -1]
    for a in range(0, len(tiles)):
        for b in range(0, len(tiles[a])):
            if tiles[a][b].own == 0 and tiles[a][b].recycler == 0:
                newMinLen = math.sqrt(math.pow((a - i), 2) + math.pow((b - j), 2))
                if newMinLen < minLen:
                    minLen = newMinLen
                    tileToGo[0] = b
                    tileToGo[1] = a
    if tileToGo[0] != -1:
        return tileToGo
    return [0,0]


def priorityMovment(tileLeft: Field or None, tileRight: Field or None, tileUp: Field or None, tileDown: Field or None, exclude: list):
    opponentTile = []
    myTiles = []
    freeTiles = []
    opponentTile = selectTiles(tileLeft, tileRight, tileUp, tileDown, 0)
    myTiles = selectTiles(tileLeft, tileRight, tileUp, tileDown, 1)
    freeTiles = selectTiles(tileLeft, tileRight, tileUp, tileDown, -1)
    for i in exclude:
        if i in opponentTile:
            opponentTile.remove(i)
        if i in freeTiles:
            freeTiles.remove(i)
        if i in myTiles:
            myTiles.remove(i)
    if len(exclude) == 4: #No possible movment
        return 0
    elif (len(opponentTile) != 0): #Possible movment on opponent tile
        totalUnits = oppBotsAround(tileLeft, tileRight, tileUp, tileDown, opponentTile)
        if totalUnits[1] != 0:
            return totalUnits
        return(choice(opponentTile))
    elif (len(freeTiles) != 0): #Possible movment on free tile
        return(choice(freeTiles))
    elif (len(myTiles) != 0): #Only possible movment on my tile
        return (-1)

def oppBotsAround(tileLeft: Field or None, tileRight: Field or None, tileUp: Field or None, tileDown: Field or None, oppTiles: list):
    totalUnitsAround = 0
    whereAreThey = 0
    for i in range(0, len(oppTiles)):
        if oppTiles[i] == 1: #Check Bots up
            if (tileUp.units > 0):
                whereAreThey = 1
            totalUnitsAround += tileUp.units
        if oppTiles[i] == 2: #Check Bots right
            if whereAreThey == 0 or (whereAreThey == 1 and tileUp.units >= tileRight.units):
                whereAreThey = 2
            totalUnitsAround += tileRight.units
        if oppTiles[i] == 3: #Check Bots down
            if whereAreThey == 0 or ((whereAreThey == 1 and tileUp.units >= tileDown.units) or (whereAreThey == 2 and tileRight.units >= tileDown.units)):
                whereAreThey = 3
            totalUnitsAround += tileDown.units
        if oppTiles[i] == 4: #Check Bots left
            if whereAreThey == 0 or ((whereAreThey == 1 and tileUp.units >= tileLeft.units) or (whereAreThey == 2 and tileRight.units >= tileLeft.units) or (whereAreThey == 3 and tileDown.units >= tileLeft.units)):
                whereAreThey = 4
            totalUnitsAround += tileLeft.units
    return [-1, totalUnitsAround, whereAreThey]

def prioritySpawn(tileLeft: Field or None, tileRight: Field or None, tileUp: Field or None, tileDown: Field or None, exclude: list, loopedNumber: int):
    opponentTile = []
    myTiles = []
    freeTiles = []
    opponentTile = selectTiles(tileLeft, tileRight, tileUp, tileDown, 0)
    myTiles = selectTiles(tileLeft, tileRight, tileUp, tileDown, 1)
    freeTiles = selectTiles(tileLeft, tileRight, tileUp, tileDown, -1)
    for i in exclude:
        if i in opponentTile:
            opponentTile.remove(i)
        if i in freeTiles:
            freeTiles.remove(i)
        if i in myTiles:
            myTiles.remove(i)
    if len(exclude) == 4:
        return False
    elif (len(opponentTile) != 0 and loopedNumber == 0): #Spawn near to opponent tile with bots on it
        totalUnits = oppBotsAround(tileLeft, tileRight, tileUp, tileDown, opponentTile)
        if totalUnits[1] != 0:
            return [True, totalUnits]
    elif (len(opponentTile) != 0 and loopedNumber == 1): #Spawn near to opponent tile
        return True
    elif (len(freeTiles) != 0 and loopedNumber == 2): #Spawn near to free tile
        return True
    elif (len(myTiles) != 0 and loopedNumber == 3): #Spawn near to my tile
        return True
    return False

def priorityBuild(tileLeft: Field or None, tileRight: Field or None, tileUp: Field or None, tileDown: Field or None, matter: int):
    opponentTile = []
    opponentTile = selectTiles(tileLeft, tileRight, tileUp, tileDown, 0)
    if (len(opponentTile) != 0): #Opponent tile near to my tile
        totalUnits = oppBotsAround(tileLeft, tileRight, tileUp, tileDown, opponentTile)
        if totalUnits[1] != 0 and totalUnits[1] >= int(matter/10): #Build to block opponent units
            return True
    return False

def checkAround(tiles: list[list[Field]], i: int, j: int, actionType: Action, loopedNumber: int, matter: int): #UP 1 | RIGHT 2 | DOWN 3 | LEFT 4
    try:
        if (i == 0 or j == 0 or i == len(tiles)-1 or j == len(tiles[i])-1):
            raise IndexError
        exclude = tilesToExclude(tiles[i][j+int(Dir.LEFT)], tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], tiles[i+int(Dir.DOWN)][j], [])
        if (actionType == Action["SPAWN"]):
            ableToSpawn = prioritySpawn(tiles[i][j+int(Dir.LEFT)], tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], tiles[i+int(Dir.DOWN)][j], exclude, loopedNumber)
            return ableToSpawn
        elif (actionType == Action["MOVE"]):
            bestMove = priorityMovment(tiles[i][j+int(Dir.LEFT)], tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], tiles[i+int(Dir.DOWN)][j], exclude)
            if bestMove == -1:
                goToOppTile = nearestOppCell(tiles, i, j)
                return goToOppTile
            return (bestMove)
        elif (actionType == Action["BUILD"]):
            needRecycler = priorityBuild(tiles[i][j+int(Dir.LEFT)], tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], tiles[i+int(Dir.DOWN)][j], matter)
            return needRecycler
    except IndexError:
        if i == 0:
            if j == 0:#UP LEFT
                exclude = tilesToExclude(None, tiles[i][j+int(Dir.RIGHT)], None, tiles[i+int(Dir.DOWN)][j], [1, 4])
                if (actionType == Action["MOVE"]):
                    bestMove = priorityMovment(None, tiles[i][j+int(Dir.RIGHT)], None, tiles[i+int(Dir.DOWN)][j], exclude)
                    if bestMove == -1:
                        goToOppTile = nearestOppCell(tiles, i, j)
                        return goToOppTile
                    return bestMove
                elif (actionType == Action["SPAWN"]):
                    ableToSpawn = prioritySpawn(None, tiles[i][j+int(Dir.RIGHT)], None, tiles[i+int(Dir.DOWN)][j], exclude, loopedNumber)
                    return ableToSpawn
                elif (actionType == Action["BUILD"]):
                    needRecycler = priorityBuild(None, tiles[i][j+int(Dir.RIGHT)], None, tiles[i+int(Dir.DOWN)][j], matter)
                    return needRecycler
            elif j == len(tiles[i])-1:#UP RIGHT
                exclude = tilesToExclude(tiles[i][j+int(Dir.LEFT)], None, None, tiles[i+int(Dir.DOWN)][j], [1, 2])
                if (actionType == Action["MOVE"]):
                    bestMove = priorityMovment(tiles[i][j+int(Dir.LEFT)], None, None, tiles[i+int(Dir.DOWN)][j], exclude)
                    if bestMove == -1:
                        goToOppTile = nearestOppCell(tiles, i, j)
                        return goToOppTile
                    return(bestMove)
                elif (actionType == Action["SPAWN"]):
                    ableToSpawn = prioritySpawn(tiles[i][j+int(Dir.LEFT)], None, None, tiles[i+int(Dir.DOWN)][j], exclude, loopedNumber)
                    return(ableToSpawn)
                elif (actionType == Action["BUILD"]):
                    needRecycler = priorityBuild(tiles[i][j+int(Dir.LEFT)], None, None, tiles[i+int(Dir.DOWN)][j], matter)
                    return needRecycler
            else:#UP
                exclude = tilesToExclude(tiles[i][j+int(Dir.LEFT)], tiles[i][j+int(Dir.RIGHT)], None, tiles[i+int(Dir.DOWN)][j], [1])
                if (actionType == Action["MOVE"]):
                    bestMove = priorityMovment(tiles[i][j+int(Dir.LEFT)], tiles[i][j+int(Dir.RIGHT)], None, tiles[i+int(Dir.DOWN)][j], exclude)
                    if bestMove == -1:
                        goToOppTile = nearestOppCell(tiles, i, j)
                        return goToOppTile
                    return(bestMove)
                elif (actionType == Action["SPAWN"]):
                    ableToSpawn = prioritySpawn(tiles[i][j+int(Dir.LEFT)], tiles[i][j+int(Dir.RIGHT)], None, tiles[i+int(Dir.DOWN)][j], exclude, loopedNumber)
                    return(ableToSpawn)
                elif (actionType == Action["BUILD"]):
                    needRecycler = priorityBuild(tiles[i][j+int(Dir.LEFT)], tiles[i][j+int(Dir.RIGHT)], None, tiles[i+int(Dir.DOWN)][j], matter)
                    return needRecycler
        if i == len(tiles)-1:
            if j == 0:#DOWN LEFT
                exclude = tilesToExclude(None, tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], None, [3, 4])
                if (actionType == Action["MOVE"]):
                    bestMove = priorityMovment(None, tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], None, exclude)
                    if bestMove == -1:
                        goToOppTile = nearestOppCell(tiles, i, j)
                        return goToOppTile
                    return(bestMove)
                elif (actionType == Action["SPAWN"]):
                    ableToSpawn = prioritySpawn(None, tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], None, exclude, loopedNumber)
                    return(ableToSpawn)
                elif (actionType == Action["BUILD"]):
                    needRecycler = priorityBuild(None, tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], None, matter)
                    return needRecycler
            elif j == len(tiles[i])-1:#DOWN RIGHT
                exclude = tilesToExclude(tiles[i][j+int(Dir.LEFT)], None, tiles[i+int(Dir.UP)][j], None, [2, 3])
                if (actionType == Action["MOVE"]):
                    bestMove = priorityMovment(tiles[i][j+int(Dir.LEFT)], None, tiles[i+int(Dir.UP)][j], None, exclude)
                    if bestMove == -1:
                        goToOppTile = nearestOppCell(tiles, i, j)
                        return goToOppTile
                    return(bestMove)
                elif (actionType == Action["SPAWN"]):
                    ableToSpawn = prioritySpawn(tiles[i][j+int(Dir.LEFT)], None, tiles[i+int(Dir.UP)][j], None, exclude, loopedNumber)
                    return(ableToSpawn)
                elif (actionType == Action["BUILD"]):
                    needRecycler = priorityBuild(tiles[i][j+int(Dir.LEFT)], None, tiles[i+int(Dir.UP)][j], None, matter)
                    return needRecycler
            else:#DOWN
                exclude = tilesToExclude(tiles[i][j+int(Dir.LEFT)], tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], None, [3])
                if (actionType == Action["MOVE"]):
                    bestMove = priorityMovment(tiles[i][j+int(Dir.LEFT)], tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], None, exclude)
                    if bestMove == -1:
                        goToOppTile = nearestOppCell(tiles, i, j)
                        return goToOppTile
                    return(bestMove)
                elif (actionType == Action["SPAWN"]):
                    ableToSpawn = prioritySpawn(tiles[i][j+int(Dir.LEFT)], tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], None, exclude, loopedNumber)
                    return(ableToSpawn)
                elif (actionType == Action["BUILD"]):
                    needRecycler = priorityBuild(tiles[i][j+int(Dir.LEFT)], tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], None, matter)
                    return needRecycler
        elif j == 0:#LEFT
            exclude = tilesToExclude(None, tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], tiles[i+int(Dir.DOWN)][j], [4])
            if (actionType == Action["MOVE"]):
                bestMove = priorityMovment(None, tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], tiles[i+int(Dir.DOWN)][j], exclude)
                if bestMove == -1:
                    goToOppTile = nearestOppCell(tiles, i, j)
                    return goToOppTile
                return(bestMove)
            elif (actionType == Action["SPAWN"]):
                ableToSpawn = prioritySpawn(None, tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], tiles[i+int(Dir.DOWN)][j], exclude, loopedNumber)
                return(ableToSpawn)
            elif (actionType == Action["BUILD"]):
                needRecycler = priorityBuild(None, tiles[i][j+int(Dir.RIGHT)], tiles[i+int(Dir.UP)][j], tiles[i+int(Dir.DOWN)][j], matter)
                return needRecycler
        else:#RIGHT
            exclude = tilesToExclude(tiles[i][j+int(Dir.LEFT)], None, tiles[i+int(Dir.UP)][j], tiles[i+int(Dir.DOWN)][j], [2])
            if (actionType == Action["MOVE"]):
                bestMove = priorityMovment(tiles[i][j+int(Dir.LEFT)], None, tiles[i+int(Dir.UP)][j], tiles[i+int(Dir.DOWN)][j], exclude)
                if bestMove == -1:
                    goToOppTile = nearestOppCell(tiles, i, j)
                    return goToOppTile
                return(bestMove)
            elif (actionType == Action["SPAWN"]):
                ableToSpawn = prioritySpawn(tiles[i][j+int(Dir.LEFT)], None, tiles[i+int(Dir.UP)][j], tiles[i+int(Dir.DOWN)][j], exclude, loopedNumber)
                return(ableToSpawn)
            elif (actionType == Action["BUILD"]):
                needRecycler = priorityBuild(tiles[i][j+int(Dir.LEFT)], None, tiles[i+int(Dir.UP)][j], tiles[i+int(Dir.DOWN)][j], matter)
                return needRecycler

def move(params: tuple[list[list[Field]], list[int], tuple[int, int]]):
    tiles = params[0]
    for i in range(len(tiles)):
        for j in range(len(tiles[i])):
            if tiles[i][j].own == 1 and tiles[i][j].units > 0:
                moveTo = checkAround(tiles, i, j, Action["MOVE"], 0, params[1][0])
                if (type(moveTo) == list and moveTo[0] != -1):
                    print("MOVE", str(tiles[i][j].units), str(j), str(i), str(moveTo[0]), str(moveTo[1]) +";", end="")
                elif (type(moveTo) == list and moveTo[0] == -1):
                    if moveTo[2] == 1:
                        print("MOVE", str(tiles[i][j].units), str(j), str(i), str(j), str(i-1) +";", end="")
                    if moveTo[2] == 2:
                        print("MOVE", str(tiles[i][j].units), str(j), str(i), str(j+1), str(i)+";", end="")
                    if moveTo[2] == 3:
                        print("MOVE", str(tiles[i][j].units), str(j), str(i), str(j), str(i+1)+";", end="")
                    if moveTo[2] == 4:
                        print("MOVE", str(tiles[i][j].units), str(j), str(i), str(j-1), str(i)+";", end="")
                else:
                    if moveTo == 1: #Move Up
                        print("MOVE", str(tiles[i][j].units), str(j), str(i), str(j), str(i-1) +";", end="")
                    if moveTo == 2: #Move Right
                        print("MOVE", str(tiles[i][j].units), str(j), str(i), str(j+1), str(i)+";", end="")
                    if moveTo == 3: #Move Down
                        print("MOVE", str(tiles[i][j].units), str(j), str(i), str(j), str(i+1)+";", end="")
                    if moveTo == 4: #Move Left
                        print("MOVE", str(tiles[i][j].units), str(j), str(i), str(j-1), str(i)+";", end="")

def spawn(params: tuple[list[list[Field]], list[int], tuple[int, int]]):
    tiles = params[0]
    tempMatter = [{'pos': -1, 'cost': -1}]
    position = 0
    for loopedNumber in range(0, 4):
        for i in range(len(tiles)):
            for j in range(len(tiles[i])):
                if tiles[i][j].own == 1:
                    spawnHere = checkAround(tiles, i, j, Action["SPAWN"], loopedNumber, params[1][0])
                    if type(spawnHere) == list:
                        tempMatter.append({'pos': position, 'cost': 10*spawnHere[1][1]})
                        position += 1
                        # print("SPAWN", str(math.floor(params[1][0]/10)), str(j), str(i)+";", end="")
                        # params[1][0] -= (10*math.floor(params[1][0]/10))
                        # if params[1][0] < 10:
                        #     return params
                    #elif spawnHere == True:
                    #    print("SPAWN", str(math.floor(params[1][0]/10)), str(j), str(i)+";", end="")
                    #    params[1][0] -= (10*math.floor(params[1][0]/10))
                    #    if params[1][0] < 10:
                    #        return params
    tempMatter.sort(key=operator.itemgetter('cost'))
    print("MESSAGE", str(tempMatter)+";", end="")
    return params

def build(params: tuple[list[list[Field]], list[int], tuple[int, int]]):
    tiles = params[0]
    for i in range(len(tiles)):
        for j in range(len(tiles[i])):
            if tiles[i][j].own == 1 and tiles[i][j].build == 1:
                buildHere = checkAround(tiles, i, j, Action["BUILD"], 0, params[1][0])
                if buildHere == True:
                    print("BUILD", str(j), str(i)+";", end="")
                    params[1][0] -= 10
                    params[0][i][j].recycler = 1
                    if params[1][0] < 10:
                        return params
    return params

# game loop
def main():
    turns = 0
    while True:
        params = ([], [0, 0], (0, 0))
        params = getParams(params[0])
        params = build(params)
        if (turns == 0):
            for i in range(len(params[0])):
                for j in range(len(params[0][i])):
                    if (params[0][i][j].build == 1):
                        print("BUILD", str(j), str(i)+";", end="")
                        params[1][0] -= 10
        turns+=1
        params = spawn(params)
        move(params)
        freeParams(params[0])
        print("WAIT")

main()