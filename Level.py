import const
import random, copy, pygame
from Asset import Asset
from Map import Map

class Level():
    def __init__(self, asset, levelIndex, background):
        print('Level:', (levelIndex + 1))
        self.asset = asset
        self.data = self.asset.levels[levelIndex]
        self.background = background
        self.map = Map(self.data)

    def draw(self, gameState):
        mapSurfaceWidth = const.MAPWIDTH * const.TILEHEIGHT
        mapSurfaceHeight = (const.MAPWIDTH - 1) * const.TILEHEIGHT + const.TILEHEIGHT
        mapSurface = pygame.Surface((mapSurfaceWidth, mapSurfaceHeight))
        mapOffsetX = int((const.MAPWIDTH - len(self.map.data)) / 2)
        mapOffsetY = int((const.MAPHEIGHT - len(self.map.data[0])) / 2)

        # start with a blank color on the surface.
        mapSurface.fill(const.BGCOLOR)

        # Draw the complete background with grass, trees, rocks as well as the level map.
        for x in range(len(self.background)):
            for y in range(len(self.background[x])):
                spaceRect = pygame.Rect(x * const.TILEWIDTH, y * const.TILEANGLEHEIGHT, const.TILEWIDTH, const.TILEHEIGHT)

                # First draw grass tile.
                mapSurface.blit(self.asset.tileMapping[' '], spaceRect)
                
                # Calculate the position of the level map.
                mapX = x - mapOffsetX
                mapY = y - mapOffsetY

                # Only draw trees and rocks when at (x, y) is no tile from level map.
                if not ((mapX >= 0 and mapX < len(self.map.data)) and (mapY >= 0 and mapY < len(self.map.data[mapX])) and self.map.data[mapX][mapY] != ' '):
                    mapSurface.blit(self.asset.tileMapping[self.background[x][y]], spaceRect)

                # Draw level map.
                if (mapX >= 0 and mapX < len(self.map.data)) and (mapY >= 0 and mapY < len(self.map.data[mapX])):
                    #spaceRect = pygame.Rect(x * const.TILEWIDTH, y * const.TILEANGLEHEIGHT, const.TILEWIDTH, const.TILEHEIGHT)

                    # Do not draw any grass tiles when drawing level map.
                    if self.map.data[mapX][mapY] != ' ' and self.map.data[mapX][mapY] in self.asset.tileMapping:
                        mapSurface.blit(self.asset.tileMapping[self.map.data[mapX][mapY]], spaceRect)

                    if (mapX, mapY) in gameState['boxes']:
                        if (mapX, mapY) in self.data['destinations']:
                            # A destination AND box are on this space, draw destination first.
                            mapSurface.blit(self.asset.images['destination_covered'], spaceRect)
                        else: 
                            # Then draw the box sprite.
                            mapSurface.blit(self.asset.images['box'], spaceRect)
                    elif (mapX, mapY) in self.data['destinations']:
                        # Draw a destination without a box on it.
                        mapSurface.blit(self.asset.images['destination_uncovered'], spaceRect)

                    # Last draw the player on the board.
                    if (mapX, mapY) == gameState['player']:
                        mapSurface.blit(self.asset.playerImage, spaceRect)

            #draw text
            self.draw_text(mapSurface, 'text48', 'Schritte: ' + str(gameState['stepCounter']), 100, 30)     ## 10px down from the screen

        return mapSurface

    def draw_text(self, surf, fontName, text, x, y):
        if fontName not in self.asset.fonts.keys():
            return

        textSurface = self.asset.fonts[fontName].render(text, True, const.WHITE)
        textSurface = pygame.transform.scale(textSurface, (int(textSurface.get_width() * const.ZOOMFACTOR), int(textSurface.get_height() * const.ZOOMFACTOR)))
        surf.blit(textSurface, (int(x * const.ZOOMFACTOR), int(y * const.ZOOMFACTOR)))

    def makeMove(self, gameState, gameStateHistory, playerMoveTo):
        playerx, playery = gameState['player']
        boxes = gameState['boxes']

        if playerMoveTo == const.UP:
            xOffset = 0
            yOffset = -1
            lurd = 'u'
        elif playerMoveTo == const.RIGHT:
            xOffset = 1
            yOffset = 0
            lurd = 'r'
        elif playerMoveTo == const.DOWN:
            xOffset = 0
            yOffset = 1
            lurd = 'd'
        elif playerMoveTo == const.LEFT:
            xOffset = -1
            yOffset = 0
            lurd = 'l'

        if self.isWall(playerx + xOffset, playery + yOffset):
            return 0
        else:
            result = 1

            # Create copy of gameState for history.
            gameStateCopy = copy.deepcopy(gameState)

            # There is a box in the way, see if the player can push it.
            if (playerx + xOffset, playery + yOffset) in boxes:
                # The box is blocked.
                if self.isBlocked(gameState, playerx + (xOffset * 2), playery + (yOffset * 2)):
                    return 0

                # Move the box.
                ind = boxes.index((playerx + xOffset, playery + yOffset))
                boxes[ind] = (boxes[ind][0] + xOffset, boxes[ind][1] + yOffset)
                lurd = lurd.upper()
                result = 2  # indicates a box has been moved
            
            # Move the player.
            gameState['player'] = (playerx + xOffset, playery + yOffset)

            # save history entry.
            gameStateHistory.append(gameStateCopy)

            # append step to stepp array
            gameState['steps'].append(lurd)

            return result

    def isWall(self, x, y):
        if x < 0 or x >= len(self.map.data) or y < 0 or y >= len(self.map.data[x]):
            return False 
        
        if self.map.data[x][y] in ('#', 'x'):
            return True

        return False
       
    def isBlocked(self, gameState, x, y):
        if self.isWall(x, y):
            return True

        if x < 0 or x >= len(self.map.data) or y < 0 or y >= len(self.map.data[x]):
            return True 

        if (x, y) in gameState['boxes']:
            return True

        return False 

    def isFinished(self, gameState):
        for destination in self.data['destinations']:
            if destination not in gameState['boxes']:
                return False

        return True
