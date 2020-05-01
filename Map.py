import const
import copy, pygame
from pygame.locals import *
from Asset import Asset

class Map():
    def __init__(self, levelData):
        self.data = self.__createMap(levelData)

    def __createMap(self, levelData):
        startx, starty = levelData['startState']['player']

        mapObj = levelData['mapObj']
        mapCopy = copy.deepcopy(mapObj)

        # Remove the non-wall characters from the map data
        for x in range(len(mapCopy)):
            for y in range(len(mapCopy[0])):
                if mapCopy[x][y] in ('$', '.', '@', '+', '*'):
                    mapCopy[x][y] = ' '

        # Flood fill to determine inside/grass tiles.
        self.__floodFill(mapCopy, startx, starty, ' ', 'f')

        # Convert the adjoined walls into corner tiles.
        for x in range(len(mapCopy)):
            for y in range(len(mapCopy[0])):
                if mapCopy[x][y] == '#':
                    if (self.__isWall(mapCopy, x, y-1) and self.__isWall(mapCopy, x+1, y)) or \
                       (self.__isWall(mapCopy, x+1, y) and self.__isWall(mapCopy, x, y+1)) or \
                       (self.__isWall(mapCopy, x, y+1) and self.__isWall(mapCopy, x-1, y)) or \
                       (self.__isWall(mapCopy, x-1, y) and self.__isWall(mapCopy, x, y-1)):
                        mapCopy[x][y] = 'x'

        return mapCopy

    def __floodFill(self, map, x, y, oldCharacter, newCharacter):
        if map[x][y] == oldCharacter:
            map[x][y] = newCharacter

        if x < len(map) - 1 and map[x+1][y] == oldCharacter:
            self.__floodFill(map, x+1, y, oldCharacter, newCharacter) # call right
        if x > 0 and map[x-1][y] == oldCharacter:
            self.__floodFill(map, x-1, y, oldCharacter, newCharacter) # call left
        if y < len(map[x]) - 1 and map[x][y+1] == oldCharacter:
            self.__floodFill(map, x, y+1, oldCharacter, newCharacter) # call down
        if y > 0 and map[x][y-1] == oldCharacter:
            self.__floodFill(map, x, y-1, oldCharacter, newCharacter) # call up

    def __isWall(self, map, x, y):
        if x < 0 or x >= len(map) or y < 0 or y >= len(map[x]):
            return False 
        
        if map[x][y] in ('#', 'x'):
            return True

        return False
