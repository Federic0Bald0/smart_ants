# -*- coding: utf-8 -*-

# https://www.python.org/dev/peps/pep-0008/  ------ PEP8 style guide
import random
import numpy as np
import tensorflow as tf

def init_weights(shape):
    init_random_dist = tf.truncated_normal(shape, stddev=1.0)
    return tf.Variable(init_random_dist)

class Ant(object):
    
    def __init__(self, env, genetic_inh=None):
        
        self.energy = 100
        self.food_harvest = 0
        self.enemy_killed = 0
        self.status = 2
        """
        0 -> attacking
        1 -> eating
        2 -> moving
        """
        env_size = env.get_size()
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
        return self.status

    def get_position(self):
        return self.position

    def get_energy(self):
        return self.energy  

    def pick_action(self, env):

        # gets information from the surroundings
        input = tf.reshape(self.get_surrounding(env), [25])

        # effective ant brain: a matrix multiplication betweeen inputs and weigths to produce the outputs
        # the highest output value is selected as next action
        # the weigths represent the genes that we are going to pass to the next generation
        attack = tf.nn.relu(tf.matmul(input, self.synapses[0]))[0]
        eat = tf.nn.relu(tf.matmul(input, self.synapses[1]))[0]

        # if both action have low value the ant move at random
        action = tf.argmax([attack, eat, 0.2])        
        self.status = action

        return action
    
    
    def move_to_target(self, env, target_position): 

        # set the direction of the incoming movement, X axis
        new_x = self.position[0] + (abs(self.position[0] - target_position[0]) - 1)/(self.position[0] - target_position[0]) 

        # Y axis
        new_y = self.position[1] + (abs(self.position[1] - target_position[1]) - 1)/(self.position[1] - target_position[1]) 
        
        if env.is_free(target_position) == False:
        # if the designed position is already occupied the ant look for a new one
            target_position = self.find_nearest_free(target_position)
            self.move_to_target(env, target_position)
            
        self.position = [new_x, new_y]
        env.remove_element(targer_position[0], targer_position[1])
        env.set_value(new_x, new_y, 2) # move ant 
        
    def move_or_act(self, env, action, dangers):

        # if the ants decide to move randomly
        if action == 2:
            
            # choose the new position
            
            x = -1
            while ((x<0) or ((x > env_size-1) or (y<0) or (y > env_size-1))):
                x = self.position[0] + random.randint(0, 3) - 1
                y = self.position[1] + random.randint(0, 3) - 1
            
            target_position = [x,y]
            
            # moves on it
            self.move_to_target(target_position)
        
        # attack/eat scenario
        else:
        
            # read the target's location
            target_position = self.get_target(action)

            # if the target is near enough the ant move or eat
            if (abs(self.position[0] - target_position[0]) - 1) and (abs(self.position[1] - target_position[1]) - 1):
               self.act(env, target_position, action, dangers)

            # if no it moves towards the target
            else:
                self.move_to_target(target_position)
    
    # look at the close positions to see what's in it
    def get_surrounding(self, env):
        env_size = env.get_size()
        input = np.zeros([5,5])
        for i in range(5):
            for j in range(5):

                x = (self.position[0]-1+i)
                y = (self.position[1]-1+j)
            
                if not ((x<0) or ((x/env_size-1)>1) or \
                    (y<0)or ((y/env_size-1)>1)):
                        input[i,j] = env.get_value(x, y)

        input[2, 2] = 0

        return input

    # attack or eat
    def act(self, env, target_position, action, dangers):

        # attack
        if action == 0:
            for danger in dangers:
                if target_position == danger.get_position():
                    danger.get_damage(env)

        # eat            
        else:

            # rise his energy and his fitness parameter
            self.rise_energy(10)
            self.food_harvest += 1
            env.remove_element(x, y)

    # rileva la posizione del suo target in base all'azione che vuole effettuare
    def get_target(self, env, action):
        for k in range (1):
            for i in range(3+(2*k)):
                for j in range(3+(2*k)):

                    x = (self.position[0]-1-k+i)
                    y = (self.position[1]-1-k+j)
                
                    if not ((x<0) or ((x > env_size-1) or (y<0) or (y > env_size-1))):

                        if ((action==0) and (env.get_value(x, y) == -1)) or \
                             ((action  == 1) and (env.get_value(x, y) == -1)):
                           
                            return(x, y)
    
    # funzione per il calcolo dei danni 
    def get_damage(self, env, damage=1):
        self.energy = self.energy + damage
        if self.energy <= 0:
            env.remove_element(self.position[0], self.position[1])
            return self
    
    # se la posizione desiderata e' occupata si muove nella prima posizione libera controllando
    # le posizioni in senso antiorario
    def find_nearest_free(self, target_position, end=False):

        c = 0
        while end == False and c < 9:

            if target_position[0] < self.position[0]:
                if target_position[1] <= self.position[1]:

                    target_position[1] = target_position[1] + 1 
                    end = env.is_free(target_position)
                                                  
                else:
                    target_position[0] = target_position[0] + 1
                    end = env.is_free(target_position)

            if target_position[0] == self.position[0]:
                if target_position[1] < self.position[1]:

                    target_position[0] = target_position[0] - 1 
                    end = env.is_free(target_position)
                
                else:

                    target_position[0] = target_position[0] + 1 
                    end = env.is_free(target_position)
            
            if target_position[0] > self.position[0]:
                if target_position[1] >= self.position[1]:

                    target_position[1] = target_position[1] - 1 
                    end = env.is_free(target_position)
                
                else:

                    target_position[0] = target_position[0] - 1 
                    end = self.env.is_free(target_position)

        if c > 8:
            target_position = self.position
        
        return target_position

    # rise current energy level
    def rise_energy(self, energy):
        self.energy += energy
    
    # get energy and a fitness parameter point as reward for killing dangers
    def kill_reward(self, energy):
        self.energy += energy
        self.enemy_killed += 1
    
    # should update current environment status
    def read_env():
        
        ### need something
        pass



############ TODO
#   READ ENVIRONMENT
#   EAT SIGNAL
#   ATTACK SIGNAL
#   CHANGE env[] to get_stuff ...
    
                    





        
