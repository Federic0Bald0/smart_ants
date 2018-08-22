# -*- coding: utf-8 -*-

import time
import random
import numpy as np


class Ant(object):
    
    def __init__(self, env, genetic_inh=None):
        
        self.energy = 100
        self.food_harvest = 0
        self.enemy_killed = 0
        self.status = 2
        env_size = env.get_size()
        # identifier, it must be unique
        # millisec should be fine as long as
        # the program doesn't run for more than a day
        self.id = int(round(time.time() * 1000))
        # choose randomly position in environment
        while True:
            x = random.randint(0, env_size-1)
            y = random.randint(0, env_size-1)
            # position i, j is free
            if env.is_free(x, y):
                self.position = [x, y]    
                env.set_value(x, y, 2)
                break
        # weight inzialization                                                         
        if genetic_inh:
            # child
            self.synapses = genetic_inh
        else:
            # first generation 
            self.synapses = init_weights([2,25])

    def get_status(self):
        # status defines what ant
        # is allowed to do:
        #
        # 0 -> attacking
        # 1 -> eating
        # 2 -> moving
        return self.status


    def set_status(self, status):
        # set a specific value for 
        # the status        
        self.status = status


    def get_position(self):
        # returns the position 
        # in the board of the ant
        return self.position


    def set_position(self, x, y):
        # set new position 
        # of the ant 
        self.positon = [x, y]

    def get_energy(self):
        # returns the value representing
        # the energy of the ant 
        return self.energy  


    def rise_energy(self, energy):
        # rise current energy level
        self.energy += energy


    def kill_reward(self, energy):
        # get energy and a fitness parameter point 
        # as reward for killing dangers
        self.energy += energy
        self.enemy_killed += 1


    def pick_action(self, env):
        # function choose action to performe

        # gets information from the surroundings
        input = np.reshape(self.get_surrounding(env), [-1])
        # effective ant brain: a matrix multiplication betweeen inputs
        # and weigths to produce the outputs the highest output 
        # is selected as next action the weigths represent the genes
        # that we are going to pass to the next generation
        # 0 -> attacking
        # 1 -> eating
        # 2 -> moving
        # matmul for compute the NN output
        attack = np.matmul(input.astype(float), self.synapses[0].astype(float))
        eat = np.matmul(input.astype(float), self.synapses[1].astype(float))
        # manually applied RELU
        attack = max(attack, 0)
        eat = max(eat, 0)
        # if both action have low value the ant move at random
        """ TODO SPIEGA, perche max attack, 1000, 1 ? 
            Tra 1000 e 1 il massimo sarà sempre 1000
        """
        if max(attack, 1000, 1) == attack:
            action = 0
        elif max(attack, 1000, 1) == 1000:
            action = 1
        else:
            action = 2
        self.set_status(action)

        return action
    
    
    def set_movement(self, env, target_position, dangers):
        # function sets direction of the incoming movement

        # set the direction of the incoming movement, X axis
        if ((abs(self.position[0] - target_position[0])) == 1) and \
           ((abs(self.position[1] - target_position[1])) == 1):
           if self.get_status() != 2:
               self.move_or_act(env, self.get_status(), target_position, dangers)
        elif (abs(self.position[0] - target_position[0])) == 1:
            new_x = self.position[0] + (target_position[0] - self.position[0])
            new_x = int(new_x)        
        elif (abs(self.position[0] - target_position[0])) == 2:
            new_x = self.position[0] + (target_position[0] - self.position[0])/2
            new_x = int(new_x)  
        # Y axis
        elif (abs(self.position[1] - target_position[1])) == 1:
            new_y = self.position[1] + (target_position[1] - self.position[1])
            new_y = int(new_y)
        elif (abs(self.position[1] - target_position[1])) == 2:
            new_y = self.position[1] + (target_position[1] - self.position[1])/2
            new_y = int(new_y)
        else:
            """ TODO SPIEGA, la formica è sul target ?"""
            new_y = self.position[1]
            new_x = self.position[0] 
        
        # if [new_x, new_y] == self.position:
        #     self.move_to(env, new_x, new_y)
        # else:
        #     if env.is_free(new_x, new_y) == True:
        #         self.move_to(env, new_x, new_y, m=1)
        #     else:
        #         target_position = self.find_nearest_free(env, [new_x, new_y])
        #         if target_position == self.position:
        #             self.move_to(env, target_position[0], target_position[1])
        #         else:
        #             self.move_to(env,target_position[0], target_position[1], m = 1)

        if not env.is_free(new_x, new_y):
            new_position = self.find_nearest_free(env, target_position)
            self.move_to(env, new_position[0], new_position[1])
        elif (target_position != self.position):
            self.move_to(env, new_position[0], new_position[1])


    def move_to(self, env, x, y, m=0):
        """ TODO SPIEGA, dato che con 
            m=0 non fa nulla a che serve il 
            parametro m?
        """
        env.remove_element(self.position[0], self.position[1])
        print self.position
        print x, y
        print 
        env.set_value(x, y, 2)
        self.set_position(x, y)
            
         
    def move_or_act(self, env, action, dangers):
        # pick the action
        action = self.pick_action(env)   
        env_size = env.get_size()
        # if the ants decide to move randomly
        if action == 2:
            # choose the new position
            while True:
                x = self.position[0] + random.randint(0, 3) - 1
                y = self.position[1] + random.randint(0, 3) - 1
                # check if the new coordinates are valid
                if ((x >= 0) and (x <= env_size-1) and (y >= 0) and (y <= env_size-1)):
                    break
            target_position = [x, y]
            # moves on it
            self.set_movement(env, target_position, dangers)
        # attack/eat scenario
        else:
            # read the target's location
            target_position = self.get_target(env, action)
            # if the target is near enough the ant move or eat
            if ((abs(self.position[0] - target_position[0]) - 1) <= 0) \
                and ((abs(self.position[1] - target_position[1]) - 1) <= 0) \
                and (self.position != target_position):
                self.act(env, target_position, action, dangers)
            # else moves it towards the target
            else:
                self.set_movement(env, target_position, dangers)
    

    def get_surrounding(self, env):
        # return a matric 5X5 representing 
        # the surrounding of the ant
        env_size = env.get_size()
        input = np.zeros([5,5])
        for i in range(5):
            for j in range(5):
                x = (self.position[0]-1+i)
                y = (self.position[1]-1+j)           
                if not ((x<0) or (x > (env_size-1)) or \
                    (y<0) or (y > (env_size-1))):
                        input[i,j] = env.get_value(x, y)
        # center, where is the ant
        input[2, 2] = 0

        return input

    def act(self, env, target_position, action, dangers):
        # performes action: attack or eat
        # attack
        if action == 0:
            # status needs to be coherent with the action
            if self.get_status() != 0:
                self.set_status(0)
            for danger in dangers:
                if target_position == danger.get_position():
                    danger.get_damage(env)
        # eat            
        else:
            # status needs to be coherent with the action
            if self.get_status() != 1:
                self.set_status(1)
            # rise its energy and his fitness parameter
            self.rise_energy(10)
            self.food_harvest += 1
            env.remove_element(target_position[0], target_position[1])


    def get_target(self, env, action):
        # returns position of the nearest target
        env_size = env.get_size()
        for k in range (1):
            for i in range(3+(2*k)):
                for j in range(3+(2*k)):
                    x = (self.position[0]-1-k+i)
                    y = (self.position[1]-1-k+j)
                    if not ((x<0) or (x > env_size-1) or (y<0) or (y > env_size-1)):                        
                        if ((action==0) and (env.get_value(x, y) == -1)) or \
                             ((action  == 1) and (env.get_value(x, y) == 1)):
                            return(x, y)
        
        return(self.position)
    

    def get_damage(self, env, damage=0):
        # given the damage the function
        # updates the energy of the ant
        # returns true if it's dead
        self.energy = self.energy + (damage * 10)
        if self.energy <= 0:
            env.remove_element(self.position[0], self.position[1])
            # improve using del self
            return True
        return False
        
    
    def find_nearest_free(self, env, target_position):
        # if no positions are free this function returns self.position and the ant does not move
        # also added a check for make sure that the ants does not try to move out of the env

        # if X axis is the same the ant looks for the two closest position along the X axis
        env_size = env.get_size()  
        if target_position[0] == self.position[0]:
            if (target_position[0]+1) < env_size-1:
                if env.is_free((target_position[0]+1), target_position[1]):
                    target_position = [(target_position[0]+1), target_position[1]]
                    return target_position
            if (target_position[0]-1) > 0:
                if env.is_free((target_position[0]-1), target_position[1]):
                    target_position = [(target_position[0]-1), target_position[1]]
                    return target_position
            else:
                return self.position
        # if Y axis is the same the ant looks for the two closest position along the X axis
        elif target_position[1] == self.position[1]:
            if (target_position[1]+1) < env_size-1:
                if env.is_free(target_position[0], (target_position[1]+1)):
                    target_position = [target_position[0], (target_position[1]+1)]
                    return target_position
            if (target_position[1]-1) > 0:
                if env.is_free(target_position[0], (target_position[1]-1)):
                    target_position = [target_position[0], (target_position[1]-1)]
                    return target_position
            else:
                return self.position 
        # if the ant wants to move in a corner it looks for the two position near the corner
        else:
            if env.is_free(self.position[0], target_position[1]):
                target_position = [self.position[0], target_position[1]]
                return target_position
            elif env.is_free(target_position[0], self.position[1]):
                target_position = [target_position[0], self.position[1]]
                return target_position
            else: return self.position
        return self.position

    
# SUPPORT FUNCTION
# initialize NNR weights
def init_weights(shape):
    init_random_dist = np.random.normal(scale=3, size=[2,25])
    return init_random_dist
    
                    





        