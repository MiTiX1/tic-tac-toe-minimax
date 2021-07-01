class TicTacToe:
  def __init__(self) -> None:
      self.board = {
        7:' ', 8:' ', 9:' ',
        4:' ', 5:' ', 6:' ',
        1:' ', 2:' ', 3:' '
      }
  
  def printBoard(self):
      for move in self.board.keys():
          if move%3 == 0:
              print(self.board[move])
              if move != 3:
                  print("-"*10)
          else:
              print(self.board[move], end=' | ')
      print()
  
  def printInfo(self):
    for move in self.board.keys():
        if move%3 == 0:
            print(move)
            if move != 3:
                print("-"*10)
        else:
            print(move, end=' | ')
    print()
      
  def isValid(self, move) -> bool:
      return self.board[move] == ' '

  def checkWin(self) -> str:
      if self.board[1] == self.board[2] == self.board[3] != ' ':
      	  return self.board[1]
      elif self.board[4] == self.board[5] == self.board[6] != ' ':
          return self.board[4]
      elif self.board[7] == self.board[8] == self.board[9] != ' ':
          return self.board[7]
      elif self.board[1] == self.board[4] == self.board[7] != ' ':
          return self.board[1]
      elif self.board[2] == self.board[5] == self.board[8] != ' ':
          return self.board[2]
      elif self.board[3] == self.board[6] == self.board[9] != ' ':
          return self.board[3]
      elif self.board[1] == self.board[5] == self.board[9] != ' ':
          return self.board[1]
      elif self.board[7] == self.board[5] == self.board[3] != ' ':
          return self.board[7]
      return None
  
  def checkFull(self) -> bool:
	  return list(self.board.values()).count(' ') == 0

  def playPlayer(self):
      move = int(input("Your move: "))
      print()
      if self.isValid(move):
          self.board[move] = 'X'
      else:
          print("Move isn't valid")
          self.playPlayer()

  def playBot(self):
      bestScore = -999
      bestMove = 0
      for move in self.board.keys():
          if self.isValid(move):
              self.board[move] = 'O'
              score = self.minimax(0, False)
              self.board[move] = ' '
              if score > bestScore:
                  bestScore = score
                  bestMove = move
      self.board[bestMove] = 'O'

  def minimax(self, depth, isMaximizing) -> int:
      if self.checkWin() == 'O':
          return 1
      elif self.checkWin() == 'X':
          return -1
      elif self.checkFull():
          return 0

      if isMaximizing:
          bestScore = -999
          for move in self.board.keys():
              if self.board[move] == ' ':
                  self.board[move] = 'O'
                  score = self.minimax(depth+1, False)
                  self.board[move] = ' '
                  if score > bestScore:
                      bestScore = score
          return bestScore
      else:
          bestScore = 999
          for move in self.board.keys():
              if self.board[move] == ' ':
                  self.board[move] = 'X'
                  score = self.minimax(depth+1, True)
                  self.board[move] = ' '
                  if score < bestScore:
                      bestScore = score
          return bestScore

  def reset(self):
      for i in self.board.keys():
          self.board[i] = ' '

  def play(self):
      self.printInfo()
      self.playPlayer()
      if self.checkWin():
          self.printBoard()
          print("You won")
          return
      elif self.checkFull():
          self.printBoard()
          print("Draw")
          return 

      self.printBoard()

      self.playBot()
      if self.checkWin():
          self.printBoard()
          print("Bot won")
          return
      elif self.checkFull():
          self.printBoard()
          print("Draw")
          return
    
      self.printBoard()
      self.play()