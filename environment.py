# -*- coding: utf-8 -*-

import random
import numpy as np

class Environment(object):

    def __init__(self, size, n_food):
        self.size = size
        # enviromment
        self.env = np.zeros([self.size, self.size])
        # n_food = self.size
        # placing food
        k = 0
        self.food_count = n_food
        while k < n_food:
            x = random.randint(0, size-1)
            y = random.randint(0, size-1)
            if self.env[x][y] == 0:
                # if location empty
                self.env[x][y] = 1
                k += 1

    def get_size(self):
        # returns size of the environment
        return self.size

    def is_free(self, x, y):
        # the location in the environment
        # is free ?
        return self.env[x][y] == 0

    def remove_element(self, x, y):
        # remove an element
        # from the environment
        if self.env[x][y] == 1:
            self.food_count -= 1
        self.env[x][y] = 0

    def get_value(self, x, y):
        # get value of a specific cell
        # in the environment
        return self.env[x][y]

    def set_value(self, x, y, v):
        # set value of a specific cell
        # in the environment
        self.env[x][y] = v

    def get_food(self):
        return self.food_count

    def to_string(self, generation):
        # build string environment
        """
        <> -> danger
        *  -> food
        ++ -> ant
        """
        env_str = "Generation : " + str(generation) + '\n'
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
