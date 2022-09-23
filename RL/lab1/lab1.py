import numpy as np
import gym
from stable_baselines3 import PPO
import math
import itertools
import datetime

import gym
import numpy
from gym import spaces, error
import xml.etree.ElementTree as ET
import os


class XO_Env(gym.Env):
    def __init__(self, player2):
        super(XO_Env, self).__init__()
        self.win_size = 3
        self.board_size = 3
        self.symbol = 1
        self.p2 = player2
        self.human = False
        self.display = False
        self.set_rewards()
        self.action_space = spaces.MultiDiscrete([3,3])
        self.observation_space = spaces.Box(low=0, high=2, shape=(3,3), dtype=np.int64)
        

    def set_rewards(self):
        self.rewards = {}
        self.rewards['win'] = 1.0
        self.rewards['lose'] = 0.0
        self.rewards['close'] = 0.0
        self.rewards['other'] = 0.5
        

    def reset(self):
        self.state_vector = np.array([[0]*self.board_size] * self.board_size)
        return self.state_vector
    
    def set_human(self, human):
        self.human = human
        
    def set_display(self, display):
        self.display = display
  

    def check_rows(self, board):
        for row in board:
            if np.all(row == [1,1,1]):
                return 1
            if np.all(row == [-1,-1,-1]):
                return 2
        return 0

    def check_diagonals(self, board):
        mdiag = [board[i][i] for i in range(self.board_size)] 

        if np.all(mdiag == [1,1,1]):
            return 1
        if np.all(mdiag == [-1,-1,-1]):
            return 2
        
        pobdiag = [board[i][len(board)-i-1] for i in range(self.board_size)]

        if np.all(pobdiag == [1,1,1]):
            return 1
        if np.all(pobdiag == [-1,-1,-1]):
            return 2
        return 0

    def is_win(self):
        board = self.state_vector
        for newBoard in [board, np.transpose(board)]:
            result = self.check_rows(newBoard)
            if result != 0:
                return result
        return self.check_diagonals(board)


    def all_close(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.state_vector[i][j] == 0:
                    return False
        return True

   
    def step(self, action):
        is_used = False
        done = False
        x,y = action

        if self.state_vector[x][y] != 0:
 
            reward_type = 'lose'
            done = True
            return self.state_vector, self.rewards[reward_type], done, {}
        
        self.state_vector[x][y] = self.symbol
        
        if self.display:
            self.render()
            
        if self.is_win() == 1:
            reward_type = 'win'
            done = True
            return self.state_vector, self.rewards[reward_type], done, {}
        elif self.all_close():
            reward_type = 'close'
            done = True
            return self.state_vector, self.rewards[reward_type], done, {}
        """ else:
            reward_type = 'other'
            done = False
            return self.state_vector, self.rewards[reward_type], done, {}"""
         
        
        p2WinState_reward = self.p2Move()
        if p2WinState_reward != 1:
            done = True
            
        if self.display:
            self.render()
            
        return self.state_vector, p2WinState_reward, done, {}
    
    def p2Move(self):
        self.p2.move(self.state_vector, self.human)
        if self.is_win() == 2:
            reward = 0
        elif self.all_close():
            reward = 0
        else:
            reward = 1
        return reward


    def render(self, mode=None, close=False):
        print(" " + "-" * (self.board_size * 4 + 1))
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.state_vector[i][j] == 0:
                    print(" | " + " ", end='')
                else:
                    print(" | " + str("X" if self.state_vector[i][j] == 1 else "O"), end='')
            print(" |")

        print(" " + "-" * (self.board_size * 4 + 1))
        print()
        

import random

class Player2:
    def __init__(self):
        pass
        
    def move(self, board, human) -> None:
        if human:
            self.move_human(board)
        else:
            self.move_ai(board)
                
    def move_human(self, board):
        #TODO: Implement human player
        taken = True
        while taken:
            x = int(input('Input x: '))
            y = int(input('Input x: '))
            if board[x][y] == 0:
                taken = False
                board[x][y] = -1
            else:
                print('already taken')
                
    def move_ai(self, board):
        taken = True
        while taken:
            spot = random.randrange(0,9)
            if board[spot//3][spot%3] == 0:
                taken = False
                board[spot//3][spot%3] = -1
