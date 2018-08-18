# -*- coding: utf-8 -*-
import random
import numpy as np
import tensorflow as tf

def init_weights(shape):
    init_random_dist = tf.truncated_normal(shape, stddev=1.0)
    return tf.Variable(init_random_dist)

class Ant(object):
    
    def __init__(self, env, genetic_inh=None):
        
        self.energy = 100
        size = env.get_size()
        # choose randomly position in environment
        while True:
            x = random.randint(0, size-1)
            y = random.randint(0, size-1)
            # position i, j is free
            if env.is_free(x, y):
                self.position = [x, y]    
                                                                
        if genetic_inh:
            self.synapses = genetic_inh
        else:
            self.synapses = init_weights([2,24])

    def get_position(self):
        return self.position
                    
            
#
#    def look_arond(""grid""):
#        .
#        .
#        return(input)

    def pick_action(env):

        input = check_surrounding(env)

        attack = tf.nn.relu(tf.matmul(input, self.synapses[0]))[0]
        eat = tf.nn.relu(tf.matmul(input, self.synapses[1]))[0]

        action = tf.argmax([attack, eat, 0.2])        

        return action
    
    # def pass_genes():
    
    def move_to_target(target_position): 

        # self.position e target_position sono le coordinate [x,y] del target e di se stessi
        # se la differenza (abs(self.position[0] - target_position[0]) - 1) e' uguale ad uno allora significa che l'obiettivo
        # si trova in una delle colonne adiacenti a quella in cu si trova la formica e quindi non sara' necesasrio nessun
        # movimento lungo l'asse delle X.
        # Altrimenti significa che c'e' piu' di una colonna di distanza tra la formica ed il target e quindi e' necessario un movimento.
        # Eg: Fo[3,4]; Ob[4,6] --> non e' necessario muoversi lungo le X.
        # Fo[3,4]; Ob[5,5] --> Fo passa in [4,4]
        new_x = self.position[0] + (abs(self.position[0] - target_position[0]) - 1)/(self.position[0] - target_position[0])

        # stesso discorso per le colonne
        new_y = self.position[1] + (abs(self.position1[1]] - target_position[1]) - 1)/(self.position[1] - target_position[1])

        self.position = [new_x, new_y]
        
    def move_or_act(action):

        if action == 2:

            target_position = [self.position[0] + random.randint(0, 3) - 1]
            target_position = [self.position[0] + random.randint(0, 3) - 1]

            self.move_to_target(target_position)
        
        else:

            target_position = self.get_target(action)

            # se l'obiettivo della propria azione si trova in una delle caselle adiacenti la formica esegue una delle due azioni disponibili
            if (abs(self.position[0] - target_position[0]) - 1) and (abs(self.position1[1]] - target_position[1]) - 1):
               self.act(target_position, action)

            # altrimenti si muove verso di esso
            else:
                self.move_to_target(target_position)
    
    def check_surrounding(env):

        input = np.zeros([5,5], dype=np.float32)
        for i in range(5):
            input[i] = env[self.position[0]-2+i, self.position[1]-2 : self.position[1]+2]
        
        np.reshape(input, [24])

        return (input)
    
    def get_surrounding(env):

        large_surrounding = np.zeros([5,5], dype=np.float32)
        small_surrounding = np.zeros([3,3], dype=np.float32)

        for i in range(5):
            large_surrounding[i] = env[self.position[0]-2+i, self.position[1]-2 : self.position[1]+2]
        
        for i in range(3):
            small_surrounding[i] = env[self.position[0]-2+i, self.position[1]-2 : self.position[1]+2]
        
        return (small_surrounding, large_surrounding)

    def act(target_position, action):

        if action == 0:
    #       attack
        else:
    #       eat

    def get_target(action):

        small_surrounding, large_surrounding = self.check_surrounding(env)

        if action == 0:

            for i in range (3):
                for j in range (3):
                    if small_surrounding[self.position[0]-1+i, self.position[1]-1+j] < 0
                        return (self.position[0]-1+i, self.position[1]-1+j)
            
            for i in range (5):
                for j in range (5):
                    if small_surrounding[self.position[0]-2+i, self.position[1]-2+j] < 0 
                        return (self.position[0]-2+i, self.position[1]-2+j)
        
        if action == 0:

            for i in range (3):
                for j in range (3):
                    if small_surrounding[self.position[0]-1+i, self.position[1]-1+j] == 1
                        return (self.position[0]-1+i, self.position[1]-1+j)
            
            for i in range (5):
                for j in range (5):
                    if small_surrounding[self.position[0]-2+i, self.position[1]-2+j] == 1
                        return (self.position[0]-2+i, self.position[1]-2+j)
    
    def get_damage(damage=1):
        self.energy = self.energy - damage
        
        if self.energy == 0:
            self.die
    
                    





        
