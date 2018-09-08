# -*- coding: utf-8 -*-

import math
import random 

class Danger(object):

    def __init__(self, env):

        env_size = env.get_size()
        # position in env
        while True: 
            x = random.randint(0, env_size-1)
            y = random.randint(0, env_size-1)
            if env.is_free(x, y):
                self.position = [x, y]
                env.set_value(x, y, -1)
                break
        # number ants close to the danger
        self.nn_ant = 0
        self.get_surrounding_ants(env)
        # power danger
        self.power = - random.randint(1, 7)


    def get_position(self):
        # returns the position 
        # of the ant 
        return self.position


    def get_power(self):
        # returns the power
        # of the danger
        return self.power
    
    '''
    added this
    Now the ants call this function (get_aggro) to attack enemies
    the nn_ant value increases by 1 for each attacking ant nearby
    but it is reset at 0 at the end of each turn
    '''

    def get_aggro(self):
         self.nn_ant += 1
        
    def reset_aggro(self):
        self.nn_ant = 0

    '''
    end add
    '''
    '''
    this function is deprecated
    '''
    # DEPRECATED
    def get_surrounding_ants(self, env):
        # check in the surrounding matrix 3X3 
        # if there are ants
        # TODO missing check of ant status ???
        env_size = env.get_size()
        for i in range(3):
            for j in range(3):
                x = (self.position[0]-1+i)
                y = (self.position[1]-1+j)
                if not ((x<0) or (x > env_size-1) or \
                    (y<0) or (y > env_size-1)):
                        if env.get_value(x, y) == 2:
                            self.nn_ant += 1


    def move_random(self, env):
        # defines random move for 
        # the danger
        axis = random.uniform(0, 3)
        way = random.uniform(0, 1)
        env_size = env.get_size()
        x = self.position[0]
        y = self.position[1]
        if axis > 3:
            # move on x-axis
            if (way > 0.5) and \
                (x < env_size-1) and \
                (x >= 0) and \
                (env.is_free(x+1, y)):
                # move up
                    env.set_value(x+1, y, -1)
                    env.remove_element(x, y)
                    self.position = [x+1, y]
            elif (way <= 0.5) and \
                (x <= env_size-1) and \
                (x > 0) and \
                (env.is_free(x-1, y)):
                # move down
                    env.set_value(x-1, y, -1)
                    env.remove_element(x, y)
                    self.position = [x-1, y]
        elif axis > 2:
            # move on y-axis
            if (way > 0.5) and \
                (y < env_size-1) and \
                (y >= 0) and \
                (env.is_free(x, y+1)):
                # move right
                    env.set_value(x, y+1, -1)
                    env.remove_element(x, y)
                    self.position = [x, y+1]
            elif (way <= 0.5) and \
                (y <= env_size-1) and \
                (y > 0) and \
                (env.is_free(x, y-1)):
                # move left
                    env.set_value(x, y-1, -1)
                    env.remove_element(x, y)
                    self.position = [x, y-1]
        elif axis > 1:
            # move on z-axis (diagonally)
            if (way > 1) and \
                (y < env_size-1) and \
                (x < env_size-1) and \
                (y >= 0) and \
                (x >= 0) and \
                (env.is_free(x+1, y+1)):
                # move north-est
                    env.set_value(x+1, y+1, -1)
                    env.remove_element(x, y)
                    self.position = [x+1, y+1]
            elif (way > 0.75) and \
                (y <= env_size-1) and \
                (x < env_size-1) and \
                (y > 0) and \
                (x >= 0) and \
                (env.is_free(x+1, y-1)):
                # move south-est 
                    env.set_value(x+1, y-1, -1)
                    env.remove_element(x, y)
                    self.position = [x+1, y-1]
            elif (way > 0.50) and \
                (y <= env_size-1) and \
                (x <= env_size-1) and \
                (y > 0) and \
                (x > 0) and \
                (env.is_free(x-1, y-1)):
                # move south-west
                    env.set_value(x-1, y-1, -1)
                    env.remove_element(x, y)
                    self.position = [x-1, y-1]
            elif (way > 0.25) and \
                (y < env_size-1) and \
                (x <= env_size-1) and \
                (y >= 0) and \
                (x > 0) and \
                (env.is_free(x-1, y+1)):
                # move north-west
                    env.set_value(x-1, y+1, -1)
                    env.remove_element(x, y)
                    self.position = [x-1, y+1]


    def damage_ant(self, env, ant, colony):
        # if we are close to an ant it damages it 
        return ant.get_damage(env, colony, damage=self.get_power()*(10))


    def attack_ant(self, env, colony):
        env_size = env.get_size()
        for i in range(3):
            for j in range(3):
                x = (self.position[0]-1+i)
                y = (self.position[1]-1+j)
                if not ((x<0) or (x > env_size-1) or \
                    (y<0) or (y > env_size-1)):
                    if env.get_value(x, y) == 2:
                        for ant in colony:
                            ant_position = ant.get_position() 
                            if ant_position == [x, y]:
                                self.damage_ant(env, ant, colony)
                                    # colony.remove(ant)
                                return True
        return False
                        

    def get_damage(self, env, dangers):
        #il power e' definito negativo ergo ci va un * -1
        if (-1 * (self.power / 2)) <= self.nn_ant:
            env.remove_element(self.position[0], self.position[1])
            dangers.remove(self)
            return True
        return False

    

    
