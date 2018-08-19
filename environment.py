# -*- coding: utf-8 -*-

import random 
import numpy as np

class Environment(object):

    def __init__(self, size):
        self.size = size
        self.dangers = []
        # enviromment
        self.env = np.zeros([self.size, self.size])
        n_food = self.size
        # placing food
        k = 0
        while k < n_food:
            x = random.randint(0, size-1)
            y = random.randint(0, size-1)
            
            if self.env[x][y] == 0: # if location empty
                self.env[x][y] = 1
                k += 1 
    
    def get_size(self):
        return self.size

    def is_free(self, x, y):
        return self.env[x][y] == 0

    def remove_element(self, x, y):
        self.env[x][y] = 0

    def get_value(self, x, y):
        return self.env[x][y]

    def set_value(self, x, y, v):
        self.env[x][y] = v

    def to_string(self):
        # build string environment
        """
        <> -> danger
        *  -> food 
        """
        env_str = ""
        for i in range(self.size):
            env_str += '|'
            for j in range(self.size):
                if self.env[i][j] < 0:
                    env_str += '<>  '
                if self.env[i][j] == 1:
                    env_str +=  '*   '
                if self.env[i][j] == 2:
                    env_str += '++  '
                if self.env[i][j] == 0: 
                    env_str +=  '    '
            env_str +=  '|\n'
        return env_str
