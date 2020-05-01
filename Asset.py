import const
import os, random, pygame

class Asset():
    def __init__(self):
        self.imageDirectory = os.path.join(os.path.dirname(__file__), 'assets/images/' + const.IMAGEDIRECTORY)
        self.soundDirectory = os.path.join(os.path.dirname(__file__), 'assets/sounds/' + const.SOUNDDIRECTORY)
        self.levelDirectory = os.path.join(os.path.dirname(__file__), 'assets/levels/' + const.LEVELDIRECTORY)
        self.fontDirectory = os.path.join(os.path.dirname(__file__), 'assets/fonts')
        self.controlsDirectory = os.path.join(os.path.dirname(__file__), 'assets/controls')

    def createBackground(self):
        background = []

        for x in range(const.MAPWIDTH):
            background.append([])

        for y in range(const.MAPHEIGHT):
            for x in range(const.MAPWIDTH):
                tileKey = ' '
                if random.randint(0, 99) < const.OUTSIDEDECORATIONPERCENTAGE:
                    tileKey = random.choice(('1', '2', '3', '4'))
                
                background[x].append(tileKey)

        return background

    def loadFonts(self):
        self.fonts = {
            'text32': self.__loadFontFile('HannoverMesseSans-dewK.ttf', 32),
            'text48': self.__loadFontFile('HannoverMesseSans-dewK.ttf', 48),
            'text96': self.__loadFontFile('HannoverMesseSans-dewK.ttf', 96)
        }

    def loadControls(self):
        self.controls = {
            'sound_enabled':    self.__loadControlImageFile('sound_enabled.png'),
            'sound_disabled':   self.__loadControlImageFile('sound_disabled.png'),
            'reset':            self.__loadControlImageFile('reset.png'),
            'undo':             self.__loadControlImageFile('undo.png'),
            'back':             self.__loadControlImageFile('back.png'),
            'next':             self.__loadControlImageFile('next.png'),
            'solution':         self.__loadControlImageFile('solution.png')
        }

    def loadLevels(self):
        self.levels = self.__loadLevelsFile('levels.txt')

    def loadSounds(self):
        self.sounds = {
            'step1': self.__loadSoundFile('step1.ogg'),
            'step2': self.__loadSoundFile('step2.ogg'),
            'move block': self.__loadSoundFile('move.ogg')
        }

    def loadImages(self):
        self.images = {
            'destination_uncovered':    self.__loadImageFile('destination_uncovered.png'),
            'destination_covered':      self.__loadImageFile('destination_covered.png'),
            'box':                      self.__loadImageFile('box.png'),
            'corner':                   self.__loadImageFile('corner.png'),
            'wall':                     self.__loadImageFile('wall.png'),
            'floor':                    self.__loadImageFile('floor.png'),
            'ground':                   self.__loadImageFile('ground.png'),
            'player':                   self.__loadImageFile('player.png'),
            'rock':                     self.__loadImageFile('rock.png'),
            'short tree':               self.__loadImageFile('tree1.png'),
            'tall tree':                self.__loadImageFile('tree2.png'),
            'ugly tree':                self.__loadImageFile('tree3.png'),
            'solved':                   self.__loadImageFileUnscaled('gewonnen.png')
        }

        # Map the character that appears in the level file to the Surface object it represents.
        self.tileMapping = {
            'x': self.images['corner'],
            '#': self.images['wall'],
            'f': self.images['floor'],
            ' ': self.images['ground'],
            '1': self.images['rock'],
            '2': self.images['short tree'],
            '3': self.images['tall tree'],
            '4': self.images['ugly tree']
        }

        self.playerImage = self.images['player']


    def __loadSoundFile(self, fileName):
        fileName = os.path.join(self.soundDirectory, fileName)
        assert os.path.exists(fileName), 'Cannot find the sound file: %s' % (fileName)
        return pygame.mixer.Sound(fileName)

    def __loadFontFile(self, fileName, size):
        fileName = os.path.join(self.fontDirectory, fileName)
        assert os.path.exists(fileName), 'Cannot find the font file: %s' % (fileName)
        return pygame.font.Font(fileName, size)

    def __loadControlImageFile(self, fileName):
        fileName = os.path.join(self.controlsDirectory, fileName)
        assert os.path.exists(fileName), 'Cannot find the control image file: %s' % (fileName)
        return pygame.transform.scale(pygame.image.load(fileName), (const.CONTROLWIDTH, const.CONTROLHEIGHT))

    def __loadImageFile(self, fileName):
        fileName = os.path.join(self.imageDirectory, fileName)
        assert os.path.exists(fileName), 'Cannot find the image file: %s' % (fileName)
        return pygame.transform.scale(pygame.image.load(fileName), (const.TILEWIDTH, const.TILEHEIGHT))

    def __loadImageFileUnscaled(self, fileName):
        fileName = os.path.join(self.imageDirectory, fileName)
        assert os.path.exists(fileName), 'Cannot find the image file: %s' % (fileName)
        return pygame.image.load(fileName)

    def __loadLevelsFile(self, fileName):
        fileName = os.path.join(self.levelDirectory, fileName)
        assert os.path.exists(fileName), 'Cannot find the level file: %s' % (fileName)

        mapFile = open(fileName, 'r')

        # Each level must end with a blank line
        content = mapFile.readlines() + ['\r\n']
        mapFile.close()

        levels = [] # Will contain a list of level objects.
        currentLevelIndex = 0
        mapTextLines = [] # contains the lines for a single level's map.
        mapObj = [] # the map object made from the data in mapTextLines
        lurdString = ''     # solution string in LURD format 

        for lineNum in range(len(content)):
            # Process each line that was in the level file.
            line = content[lineNum].rstrip('\r\n')
            solution = ''

            # Comment line?
            if ';' in line:
                # Solution?
                if line.find(';Solution:') > -1:
                    lurdString = line.split(';Solution:')[1]
                    if len(lurdString) > 0:
                        solutionArray = []
                        i = 0
                        while i < len(lurdString):
                            direction = ''
                            numberOfSteps = '1'

                            while lurdString[i] in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9') and i < len(lurdString):
                                numberOfSteps = numberOfSteps + lurdString[i]
                                i = i + 1

                            if i < len(lurdString):
                                direction = lurdString[i]

                            i = i + 1

                            if direction != '':
                                for x in range(0, int(numberOfSteps)):
                                    solutionArray.append(direction.lower())

                        solution = ''.join(solutionArray)

                # Otherwise ignore the ; lines, they're comments in the level file.
                line = line[:line.find(';')]

            if "'" in line:
                line = line[:line.find("'")]

            if line != '':
                # This line is part of the map.
                mapTextLines.append(line)
            elif line == '' and len(mapTextLines) > 0:
                # A blank line indicates the end of a level's map in the file.
                # Convert the text in mapTextLines into a level object.

                # Find the longest row in the map.
                maxWidth = -1
                for i in range(len(mapTextLines)):
                    if len(mapTextLines[i]) > maxWidth:
                        maxWidth = len(mapTextLines[i])
                
                # Add spaces to the ends of the shorter rows. This
                # ensures the map will be rectangular.
                for i in range(len(mapTextLines)):
                    mapTextLines[i] += ' ' * (maxWidth - len(mapTextLines[i]))

                # Convert mapTextLines to a map object.
                for x in range(len(mapTextLines[0])):
                    mapObj.append([])
                for y in range(len(mapTextLines)):
                    for x in range(maxWidth):
                        mapObj[x].append(mapTextLines[y][x])

                # Loop through the spaces in the map and find the @, ., and $
                # characters for the starting game state.
                startx = None # The x and y for the player's starting position
                starty = None
                destinations = [] # list of (x, y) tuples for each destination.
                boxes = [] # list of (x, y) for each box's starting position.
                for x in range(maxWidth):
                    for y in range(len(mapObj[x])):
                        if mapObj[x][y] in ('@', '+'):
                            # '@' is player, '+' is player & destination
                            startx = x
                            starty = y
                        if mapObj[x][y] in ('.', '+', '*'):
                            # '.' is destination, '*' is box & destination
                            destinations.append((x, y))
                        if mapObj[x][y] in ('$', '*'):
                            # '$' is box
                            boxes.append((x, y))

                # Basic level design sanity checks:
                assert startx != None and starty != None, 'Level %s (around line %s) in %s is missing a "@" or "+" to mark the start point.' % (currentLevelIndex+1, lineNum, fileName)
                assert len(destinations) > 0, 'Level %s (around line %s) in %s must have at least one destination.' % (currentLevelIndex+1, lineNum, fileName)
                assert len(boxes) >= len(destinations), 'Level %s (around line %s) in %s is impossible to solve. It has %s destinations but only %s boxes.' % (currentLevelIndex+1, lineNum, filename, len(destinations), len(boxes))

                # Create level object and starting game state object.
                gameStateObj = {'player': (startx, starty),
                                'stepCounter': 0,
                                'steps': [],
                                'boxes': boxes
                }
                levelObj = {'width': maxWidth,
                            'height': len(mapObj),
                            'mapObj': mapObj,
                            'destinations': destinations,
                            'startState': gameStateObj,
                            'solution': solution
                }

                levels.append(levelObj)

                # Reset the variables for reading the next map.
                mapTextLines = []
                mapObj = []
                gameStateObj = {}
                currentLevelIndex += 1
                solution = ''                

        return levels
