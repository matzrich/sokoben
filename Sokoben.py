from Game import Game

def main():
    useSolution = False
    runGame = True
    state = 'intro'
    
    game = Game()

    while runGame: 
        # show intro screen
        if state == 'intro':
            state = game.intro()

        # play the game
        elif state == 'level_play':
            result = game.play(useSolution)
            useSolution = False

            if result == 'solved':
                state = 'level_solved'

            elif result == 'next':
                game.nextLevel()

            elif result == 'back':
                game.previousLevel()

            elif result == 'solution':
                useSolution = True

            elif result == 'reset':
                pass

            else: # result == 'exit'
                state = 'outro'

        # show solved screen
        elif state == 'level_solved':
            result = game.solved()

            if result == 'continue':
                game.nextLevel()
                state = 'level_play'
                
            else: # result == 'exit'
                state = 'outro'

        # show outro screen
        elif state == 'outro':
            game.outro()
            state = 'exit'

        # exit game
        elif state == 'exit':
            runGame = False
            
    game.exit()
    print('Bye')

if __name__ == '__main__':
    main()