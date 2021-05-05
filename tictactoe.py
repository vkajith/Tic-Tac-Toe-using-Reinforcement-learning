import numpy as np
import pickle

class State:
    
    def __init__(self, p1, p2):
        self.board = np.zeros((3,3))
        self.p1 = p1
        self.p2 = p2
        self.isEnd = False
        self.boardHash = None
        self.playerSymbol = 1
        
    def getHash(self):
        self.boardHash = str(self.board.reshape(3*3))
        return self.boardHash
    
    def winner(self):
        #row
        for i in range(3):class State:
    
    def __init__(self, p1, p2):
        self.board = np.zeros((3,3))
        self.p1 = p1
        self.p2 = p2
        self.isEnd = False
        self.boardHas
            if sum(self.board[i, :]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[i, :]) == -3:
                self.isEnd = True
                return -1
        
        #col
        for i in range(3):
            if sum(self.board[:, i]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[:, i]) == -3:
                self.isEnd = True
                return -1
            
        #diagonal
        diag_sum1 = sum([self.board[i, i] for i in range(3)])
        diag_sum2 = sum([self.board[i, 2-i] for i in range(3)])
        diag_sum = max(abs(diag_sum1), abs(diag_sum2))
        if diag_sum == 3:
            self.isEnd = True
            if diag_sum1 == 3 or diag_sum2 == 3:
                return 1
            else:
                return -1
        
        #tie
        if len(self.availablePositions()) == 0:
            self.isEnd = True
            return 0class State:
    
    def __init__(self, p1, p2):
        self.board = np.zeros((3,3))
        self.p1 = p1
        self.p2 = p2
        self.isEnd = False
        self.boardHas
        self.isEnd = False
        return None
    
    def availablePositions(self):
        positions = []
        for i in range(3):
            for j in range(3):
                if self.board[i, j] == 0:
                    positions.append((i, j))
        return positions
    
    def updateState(self, position):
        self.board[position] = self.playerSymbol
        if self.playerSymbol == 1:
            self.playerSymbol = -1
        else:
            self.playerSymbol = 1
            
    def giveReward(self):
        result = self.winner()
        if result == 1:
            self.p1.feedReward(1)
            self.p2.feedReward(0)
        elif result == -1:
            self.p1.feedReward(0)
            self.p2.feedReward(1)
        else:
            self.p1.feedReward(0.1)
            self.p2.feedReward(0.5)
            
    def reset(self):
        self.board = np.zeros((3,3))
        self.boardHash = None
        self.isEnd = False
        self.playerSymbol = 1
        
    def play(self, rounds = 100):
        for i in range(rounds):
            print("Round number " + str(i))
            while not self.isEnd:
                #Player 1
                positions = self.availablePositions()
                p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
                #Take action and update the board state
                self.updateState(p1_action)
                board_hash = self.getHash()
                self.p1.addState(board_hash)
                #Check board status if it is the end
                
                win = self.winner()
                if win is not None:
                    self.showBoard()
                    self.giveReward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break
                    
                else:
                    #Player 2
                    positions = self.availablePositions()
                    p2_action = self.p2.chooseAction(positions, self.board, self.playerSymbol)
                    self.updateState(p2_action)
                    board_hash = self.getHash()
                    self.p2.addState(board_hash)
                    
                    win = self.winner()
                    if win is not None:
                        self.showBoard()
                        self.giveReward()
                        self.p1.reset()
                        self.p2.reset()
                        self.reset()
                        break
                        
    #Play with Human
    def play2(self):
        while not self.isEnd:
            #Player 1
            positions = self.availablePositions()
            p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
            self.updateState(p1_action)
            self.showBoard()
            win = self.winner()
            if win is not None:
                if win == 1:
                    print(self.p1.name, "wins!")
                else:
                    print("tie!")
                self.reset()
                break
                
            else:
                #Player 2
                positions = self.availablePositions()
                p2_action = self.p2.chooseAction(positions)
                self.updateState(p2_action)
                self.showBoard()
                win = self.winner()
                if win is not None:
                    if win == -1:
                        print(self.p2.name, "wins!")
                    else:
                        print("tie!")
                    self.reset()
                    break
                    
    def showBoard(self):
        for i in range(0, 3):
            print("--------------------")
            out = '| '
            for j in range(0, 3):
                if self.board[i, j] == 1:
                    token = 'x'
                if self.board[i, j] == -1:
                    token = 'o'
                if self.board[i, j] == 0:
                    token = ' '
                out += token + ' | '
            print(out)
        print("--------------------")       




class Player:
    
    def __init__(self, name, exp_rate = 0.3):
        self.name = name
        self.states = []
        self.lr = 0.2
        self.exp_rate = exp_rate
        self.decay_gamma = 0.9
        self.states_value = {}
        
    def getHash(self, board):
        boardHash = str(board.reshape(3*3))
        return boardHash
    
    def chooseAction(self, positions, current_board, symbol):
        if np.random.uniform(0, 1) <= self.exp_rate:
            #Take random action
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:
            value_max = -99999
            for p in positions:
                next_board = current_board.copy()
                next_board[p] = symbol
                next_boardHash = self.getHash(next_board)
                value = 0 if self.states_value.get(next_boardHash) is None else self.states_value.get(next_boardHash)
                if value >= value_max:
                    value_max = value
                    action = p
        return action
        
    def addState(self, state):
        self.states.append(state)
        
    def feedReward(self, reward):
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            self.states_value[st] += self.lr * (self.decay_gamma * reward - self.states_value[st])
            reward = self.states_value[st]
            
    def reset(self):
        self.states = []
        
    def savePolicy(self):
        fw = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()
        
    def loadPolicy(self, file):
        fr = open(file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()



class Player:
    
    def __init__(self, name, exp_rate = 0.3):
        self.name = name
        self.states = []
        self.lr = 0.2
        self.exp_rate = exp_rate
        self.decay_gamma = 0.9
        self.states_value = {}
        
    def getHash(self, board):
        boardHash = str(board.reshape(3*3))
        return boardHash
    
    def chooseAction(self, positions, current_board, symbol):
        if np.random.uniform(0, 1) <= self.exp_rate:
            #Take random action
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:
            value_max = -99999
            for p in positions:
                next_board = current_board.copy()
                next_board[p] = symbol
                next_boardHash = self.getHash(next_board)
                value = 0 if self.states_value.get(next_boardHash) is None else self.states_value.get(next_boardHash)
                if value >= value_max:
                    value_max = value
                    action = p
        return action
        
    def addState(self, state):
        self.states.append(state)
        
    def feedReward(self, reward):
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            self.states_value[st] += self.lr * (self.decay_gamma * reward - self.states_value[st])
            reward = self.states_value[st]
            
    def reset(self):
        self.states = []
        
    def savePolicy(self):
        fw = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()
        
    def loadPolicy(self, file):
        fr = open(file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()   



#Training 

p1 = Player("p1")
p2 = Player("p2")

st = State(p1, p2)
print("Training....")
st.play(50000)

p1.savePolicy()
p2.savePolicy()


#Game
p1 = Player("computer", exp_rate = 0)
p1.loadPolicy("policy_p1")

p2 = HumanPlayer("Aquib")

st = State(p1, p2)
st.play2()