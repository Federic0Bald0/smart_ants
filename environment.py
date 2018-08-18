# -*- coding: utf-8 -*-
import sys
import time
import random 

class Environment(object):

    def __init__(self, size):
        self.size = size
        # enviromment
        self.env = [[0 for x in range(size)] for y in range(size)]
        n_danger = size 
        n_food = size
        # placing dangers
        k = 0
        while k < n_danger:
            x = random.randint(0, size-1)
            y = random.randint(0, size-1)
            c = random.randint(0, 10) # value danger
            if self.env[x][y] == 0: # if location empty
                self.env[x][y] = -c
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

    def print_env(self):
        sys.stdout.write("\r" + str(self.env))
        sys.stdout.flush()

for i in range(0, 100):
    env = Environment(10)
    env.print_env()
    time.sleep(1)