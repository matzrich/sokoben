import const
import copy, pygame
import Controls 

from pygame.locals import *
from Level import Level
from Asset import Asset
from Sound import Sound

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Sokoben")

        self.asset = Asset()
        self.background = self.asset.createBackground()
        self.sound = Sound(self.asset)

        self.asset.loadImages()
        self.asset.loadLevels()
        self.asset.loadSounds()
        self.asset.loadFonts()
        self.asset.loadControls()

        self.levelIndex = 0
        self.level = None

        Controls.add('sound_enabled', self.asset.controls['sound_enabled'], (const.MAPWIDTH * const.TILEWIDTH) - ((1 * 64) + 64), 10, self.sound.enabled)
        Controls.add('sound_disabled', self.asset.controls['sound_disabled'], (const.MAPWIDTH * const.TILEWIDTH) - ((1 * 64) + 64), 10, not self.sound.enabled)
        Controls.add('reset', self.asset.controls['reset'], (const.MAPWIDTH * const.TILEWIDTH) - ((2 * 64) + 64), 10, True)
        Controls.add('undo', self.asset.controls['undo'], (const.MAPWIDTH * const.TILEWIDTH) - ((3 * 64) + 64), 10, True)
        Controls.add('next', self.asset.controls['next'], (const.MAPWIDTH * const.TILEWIDTH) - ((4 * 64) + 64), 10, True)
        Controls.add('back', self.asset.controls['back'], (const.MAPWIDTH * const.TILEWIDTH) - ((5 * 64) + 64), 10, True)
        Controls.add('solution', self.asset.controls['solution'], (const.MAPWIDTH * const.TILEWIDTH) - ((6 * 64) + 64), 10, False)
        
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((const.MAPWIDTH * const.TILEWIDTH, (const.MAPHEIGHT - 1) * const.TILEANGLEHEIGHT + const.TILEHEIGHT))

    def play(self, useSolution):
        self.level = Level(self.asset, self.levelIndex, self.background)

        gameState = copy.deepcopy(self.level.data['startState'])
        gameStateHistory = []
        solution = self.level.data['solution']

        if len(solution) > 0:
            Controls.controls['solution'].enabled = True
        else:
            Controls.controls['solution'].enabled = False

        mapNeedsRedraw = True

        i = 0
        while True:
            playerMoveTo = None
            moveBySolution = False
            skipSolutionDelay = False

            key = pygame.key.get_pressed()
            if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT]:
                skipSolutionDelay = True

            for event in pygame.event.get(): 
                # Player clicked the "X" at the corner of the window.
                if event.type == pygame.QUIT:
                    return 'exit'

                # Player clicked somewhere on the screen
                if event.type == pygame.MOUSEBUTTONUP:
                    # Sound toggle
                    if Controls.controls['sound_enabled'].isClicked(pygame.mouse.get_pos()) or Controls.controls['sound_disabled'].isClicked(pygame.mouse.get_pos()):
                        Controls.controls['sound_enabled'].toggle()
                        Controls.controls['sound_disabled'].toggle()
                        self.sound.toggle()
                        mapNeedsRedraw = True

                    if Controls.controls['reset'].isClicked(pygame.mouse.get_pos()):
                        return 'reset'

                    if Controls.controls['next'].isClicked(pygame.mouse.get_pos()):
                        return 'next'

                    if Controls.controls['back'].isClicked(pygame.mouse.get_pos()):
                        return 'back'

                    if Controls.controls['solution'].isClicked(pygame.mouse.get_pos()):
                        return 'solution'

                    if Controls.controls['undo'].isClicked(pygame.mouse.get_pos()):
                        i = len(solution) + 1
                        if gameState['stepCounter'] > 0:
                            gameState = gameStateHistory.pop()
                            mapNeedsRedraw = True

                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        playerMoveTo = const.LEFT
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        playerMoveTo = const.RIGHT
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        playerMoveTo = const.UP
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        playerMoveTo = const.DOWN

                    elif event.key == K_n:
                        return 'next'
                    elif event.key == K_b:
                        return 'back'

                    elif event.key == pygame.K_u:
                        i = len(solution) + 1
                        if gameState['stepCounter'] > 0:
                            gameState = gameStateHistory.pop()
                            mapNeedsRedraw = True

                    elif event.key == pygame.K_ESCAPE:
                        return 'exit'

                    elif event.key == pygame.K_BACKSPACE:
                        return 'reset' 

            # Disable automatic solution play when user pressed a direction key.
            if playerMoveTo != None:
                useSolution = False
                i = len(solution) + 1

            if useSolution and i < len(solution):
                direction = solution[i]

                if direction in ('l', 'L'):
                    playerMoveTo = const.LEFT
                elif direction in ('u', 'U'):
                    playerMoveTo = const.UP
                elif direction in ('r', 'R'):
                    playerMoveTo = const.RIGHT
                elif direction in ('d', 'D'):
                    playerMoveTo = const.DOWN

                moveBySolution = True
                i = i + 1

            if playerMoveTo != None: 
                moved = self.level.makeMove(gameState, gameStateHistory, playerMoveTo)

                if moved in (1, 2):
                    gameState['stepCounter'] += 1
                    mapNeedsRedraw = True

                    if gameState['stepCounter'] % 2 == 0:
                        self.sound.play('step1')
                    else:
                        self.sound.play('step2')

                    if moved == 2:
                        self.sound.play('move block')

            if mapNeedsRedraw:
                self.screen.fill(const.BGCOLOR)

                # draw level based on gameState
                mapSurface = self.level.draw(gameState)
                self.screen.blit(mapSurface, mapSurface.get_rect())

                # draw all controls
                for key in Controls.controls:
                    controlSurface = Controls.controls[key].draw()
                    if controlSurface != None:
                        self.screen.blit(controlSurface, (Controls.controls[key].x, Controls.controls[key].y))

                pygame.display.update() 
                mapNeedsRedraw = False

            if self.level.isFinished(gameState):
                print(''.join(gameState['steps']))
                return 'solved'

            # wait some time to care about CPU.
            if moveBySolution:
                if not skipSolutionDelay:
                    pygame.time.wait(const.SOLUTIONDELAY)

            self.clock.tick(const.FPS)

    def nextLevel(self):
        self.levelIndex += 1
        if self.levelIndex >= len(self.asset.levels):
            self.levelIndex = 0

    def previousLevel(self):
        self.levelIndex -= 1
        if self.levelIndex < 0:
            self.levelIndex = len(self.asset.levels) - 1

    def intro(self):
        print('intro')
        return 'level_play'

    def solved(self):
        print('solved')

        tile = self.asset.images['solved']
        tileWidth = tile.get_width()
        tileHeight = tile.get_height()
        screenWidth = (const.MAPWIDTH * const.TILEWIDTH)
        screenHeight = (const.MAPHEIGHT * const.TILEHEIGHT)

        print(screenWidth, screenHeight, tileWidth, tileHeight)
        print((int((screenWidth - tileWidth) / 2 * const.ZOOMFACTOR), int((screenHeight - tileHeight) / 2 * const.ZOOMFACTOR)))
        surface = pygame.Surface((tileWidth, tileHeight), pygame.SRCALPHA, 32)
        surface = surface.convert_alpha()
        surface.blit(tile, (0,0))

        self.screen.blit(surface, (int((screenWidth - tileWidth) / 2 * const.ZOOMFACTOR), int((screenHeight - tileHeight) / 2 * const.ZOOMFACTOR)))
        pygame.display.update() 

        while True:
            for event in pygame.event.get(): 
                # Player clicked the "X" at the corner of the window.
                if event.type == QUIT:
                    return 'exit'

                elif event.type in (KEYDOWN, MOUSEBUTTONUP):
                    return 'continue'

            self.clock.tick(const.FPS)

        return 'exit'

    def outro(self):
        print('outro')

    def exit(self):
        pygame.quit()
