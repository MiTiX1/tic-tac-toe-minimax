from tic_tac_toe import TicTacToe

def main():
    game = TicTacToe()
    play = True
    while play:
        game.reset()
        game.play()
        play = True if input("""Play again "Y/N": """).upper() == 'Y' else False
        print()
    
if __name__ == "__main__":
    main()



