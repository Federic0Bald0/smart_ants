# -*- coding: utf-8 -*-
import sys
import time
import random 
import curses

class Environment(object):

    def __init__(self, size):
        self.size = size
        self.dangers = []
        # enviromment
        self.env = [[0 for x in range(self.size)] for y in range(self.size)]
        n_danger = self.size 
        n_food = self.size
        # placing dangers
        k = 0
        while k < n_danger:
            x = random.randint(0, size-1)
            y = random.randint(0, size-1)
            c = random.randint(0, 10) # value danger
            if self.env[x][y] == 0: # if location empty
                self.env[x][y] = -c
                self.dangers.append([x, y])
                k += 1 

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

    def remove_danger(self, x, y):
        self.env[x][y] = 0

    def get_value(self, x, y):
        return self.env[x][y]

    def display(self):
        i = 0 
        while True:
            win = curses.initscr()
            win.clear()
            win.addstr(self.beautify())
            win.refresh
            time.sleep(0.1)
            self.move_danger()
        curses.endwin()

    def beautify(self):
        env_str = ""
        for i in range(self.size):
            env_str += '|  '
            for j in range(self.size):
                if self.env[i][j] < 0:
                    env_str += '<> '
                if self.env[i][j] > 0:
                    env_str +=  '*  '
                if self.env[i][j] == 0: 
                    env_str +=  '   '
            env_str +=  '|\n'
        return env_str

    def move_danger(self):
        
        for i in range(len(self.dangers)):
            x = self.dangers[i][0]
            y = self.dangers[i][1]
            if random.uniform(0, 1) > 0.5:
                if (random.uniform(0, 1) > 0.5) and \
                    (x < self.size-1) and \
                    (x >= 0) and \
                    (self.env[x+1][y] == 0):

                    self.env[x+1][y] = self.env[x][y]
                    self.env[x][y] = 0
                    self.dangers[i] = [x+1, y]

                elif (x <= self.size-1) and \
                      (x > 0) and \
                      (self.env[x-1][y] == 0) :

                    self.env[x-1][y] = self.env[x][y]
                    self.env[x][y] = 0
                    self.dangers[i] = [x-1, y]
            else:
                if (random.uniform(0, 1) > 0.5) and \
                    (y < self.size-1) and \
                    (y >= 0) and \
                    (self.env[x][y+1] == 0):

                    self.env[x][y+1] = self.env[x][y]
                    self.env[x][y] = 0
                    self.dangers[i] = [x, y+1]

                elif (y <= self.size-1) and  \
                      (y > 0) and \
                      (self.env[x][y-1] == 0):

                    self.env[x][y-1] = self.env[x][y]
                    self.env[x][y] = 0
                    self.dangers[i] = [x, y-1]

env = Environment(50)
print env.display()
