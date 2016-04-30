'''
Created on Nov 24, 2014

Python script that play Tic Tac Toe with user

@author: Xuan Mai
'''
import sys
import copy

class TicTacToeTest:
    '''
    Create a dictionary called 'puzzle' and set 'size' to 9
    Playable positions range from 1 - 9
    '''
    def __init__(self):
        self.puzzle = {}
        self.size = 9

        for i in range(1, self.size+1):     # assign each position a number
            self.puzzle[i] = i
            
    '''
    Print to the screen current state of the puzzle
    '''
    def printPuzzle(self):
        for x in range(1, self.size+1):
            print self.puzzle[x],
            
            if (x%3 == 0):
                print
                
        print

    '''
    'state' = list contains 2 elements only: dictionary of current state and character presented player
    
    Get all successors of current stage
    Return a list of dictionary of states
    '''
    def getSuccessors(self, state):
        currentState = state[0];
        player = state[1];
        successors = []
        empty = [];

        temp = {};
        for i in range(1, self.size+1):
            if (isinstance(currentState[i], int)):
                empty.append(i)

        for emptyValue in empty:
            for i in range(1, self.size+1):
                temp[i] = currentState[i]
            temp[emptyValue] = player
            successors.append(copy.deepcopy(temp))
            temp.clear()

        return successors

    ''' Helper Method
    'state' = dictionary of current state
    
    Check if any player wins in row
    Return player's symbol if there is a winner; otherwise return 0
    '''
    def winRow(self, state):
        for i in (1,4,7):       # first position of rows 
            if (state[i] == state[i+1] == state[i+2]):
                return state[i]

        return 0

    ''' Helper Method
    'state' = dictionary of puzzle
    
    Check if any player wins in column
    Return player's symbol if there is a winner; otherwise return 0
    '''
    def winCol(self, state):
        for i in (1,2,3):       # first position of columns
            if (state[i] == state[i+3] == state[i+6]):
                return state[i]

        return 0

    ''' Helper Method
    'state' = dictionary of puzzle
    
    Check if any player wins in diagonal
    Return player's symbol if there is a winner; otherwise return 0
    '''
    def winDiagonal(self, state):
        if (state[1] == state[5] == state[9]):      # position of diagonal starts from top left
            return state[1]
        if (state[7] == state[5] == state[3]):      # position of diagonal starts from bottom left
            return state[7]

        return 0
    
    '''
    'position' = a integer indicated a position on the board
    
    Check if 'position' is valid to play
    Return true if 'position' is valid; otherwise return false
    '''
    def isValid(self, position):
        if (isinstance(self.puzzle[position], int)):
            return True;
        
        return False;
    
    '''
    Check if there is a winner
    Return winner's symbol if there is one; otherwise return 0
    '''
    def winner(self):
        if ((self.winRow(self.puzzle) == 0) and (self.winCol(self.puzzle) == 0) and (self.winDiagonal(self.puzzle) == 0)):
            return 0;
        elif (self.winRow(self.puzzle) != False):
            return self.winRow(self.puzzle); 
        elif (self.winCol(self.puzzle) != False):
            return self.winCol(self.puzzle);
        else:
            return self.winDiagonal(self.puzzle);
    
    ''' Helper Method
    Check if the game is finished
    Return true if it is done; otherwise return false
    '''
    def isDone(self):
        for x in range(1, self.size+1):
            if (isinstance(self.puzzle[x], int)):
                return False;
            
        return True;
    
    '''
    Check if the game is tie
    Return true if it is tie; otherwise return false
    '''
    def tie(self):
        if (self.isDone() and (self.winner() == 0)):    # no winner and the game is finished
            return True;
        
        return False; 
    
    '''
    Prompt user for a move
    * Note: User is symbol 'X'
    '''
    def humanPlay(self):
        move = input ("Enter the position you want to play: ");
        
        while ((int(move) > 9) or (int(move) < 1) or (not (self.isValid(int(move))))):      # not valid or outside the board
            move = input ("Enter the position you want to play: ");
            
        self.puzzle[int(move)] = 'X';
            
    '''
    Computer's move using minimax algorithm
    * Note: Computer is symbol 'O'
    '''
    def comPlay(self):
        move = self.minimax(self.puzzle, 0)
        
        # clear puzzle and create an updated puzzle included this move
        self.puzzle.clear()
        self.puzzle = copy.deepcopy(move[0])

    '''
    'state' = dictionary of puzzle
    
    Find the utility of 'state'
    Return -1 if user will win; 1 if computer will win; 0 in all other cases
    '''
    def utility(self, state):
        if ((self.winCol(state) == 'X') or (self.winDiagonal(state) == 'X') or (self.winRow(state) == 'X')):
            return -1
        elif ((self.winCol(state) == 'O') or (self.winDiagonal(state) == 'O') or (self.winRow(state) == 'O')):
            return 1
        else:
            return 0

    '''
    'state' = dictionary of puzzle
    
    Check if 'state' is a terminal state
    Return true if 'state' is a terminal state; otherwise return false
    '''
    def terminalTest(self, state):
        if ((self.utility(state) == 1) or (self.utility(state) ==  -1)):        # there is a winner
            return True
        elif (self.utility(state) == 0):            # no winner
            for i in range(1, self.size+1):
                if (isinstance(state[i], int)):         # false if there is a empty position
                    return False
                
            return True             # true if the board is filled
        else:
            return False

    '''
    'state' = dictionary of puzzle
    'level' = an integer | Even number if it is computer's turn - Odd number if it is user's turn
    
    Recursive algorithm
    Find all the possible moves and theirs utilities
    Depend of the outcome of each move, decide the best move
    
    Return a list of 2 elements: dictionary of puzzle (next state) and its utility (for next state) 
    '''
    def minimax(self, state, level):
        if self.terminalTest(state):
            return [state, self.utility(state)]
        else:
            if level % 2 == 0:          # computer's turn
                max = float("-inf")
                
                for s in self.getSuccessors((state, 'O')):      # get all successors of current state
                    temp = self.minimax(s, level+1)
                    if temp[1] > max:       # successor has better utility than 'max'
                        max = copy.deepcopy(temp[1])
                        maxMove = (s, copy.deepcopy(max))
                        
                return maxMove
            else:           # user's turn
                min = float("inf")      
                
                for s in self.getSuccessors((state, 'X')):
                    temp = self.minimax(s, level+1)
                    if temp[1] < min:       # successor has utility less than 'min'
                        min = copy.deepcopy(temp[1])
                        minMove = (s, copy.deepcopy(min))
                        
                return minMove
            
    '''
    Run the game
    '''
    def playGame(self):
        game.printPuzzle();
        
        while ((self.isDone() == False) and (self.winner() == 0)):      # game is not done and no winner
            self.humanPlay();
            self.printPuzzle();

            if ((self.isDone()) or (self.winner() != 0)):
                break;
            
            self.comPlay();
            self.printPuzzle();
                
        print 'Game completed';
        if (self.tie()):
            print 'Tie!';
        else:
            print 'Winner is', self.winner();

if __name__ == '__main__':
    game = TicTacToeTest()

    game.playGame()

