# -*- coding: utf-8 -*-
import time
import random 
import curses
import numpy as np

class Environment(object):

    def __init__(self, size):
        self.size = size
        self.dangers = []
        # enviromment
        self.env = np.zeros(self.size, self.size)
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
        return self.env[x][y] != 0

    def remove_element(self, x, y):
        self.env[x][y] = 0

    def get_value(self, x, y):
        return self.env[x][y]

    def display(self):
        # display environment 
        # TODO missing ants
        i = 0 
        while True:
            try:
                win = curses.initscr()
                win.clear()
                win.addstr(self.beautify())
                win.refresh
                time.sleep(1)
                self.move_danger()
            except Exception as e:
                print e
                pass

    def beautify(self):
        # build string environment
        # TODO missing ants
        """
        <> -> danger
        *  -> food 
        """
        env_str = ""
        for i in range(self.size):
            env_str += '|  '
            for j in range(self.size):
                # if self.env[i][j] < 0:
                #     env_str += '<>  '
                if self.env[i][j] > 0:
                    env_str +=  '*  '
                if self.env[i][j] == 0: 
                    env_str +=  '   '
            env_str +=  '|\n'
        return env_str
