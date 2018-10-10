# -*- coding: utf-8 -*-

import time
import random
import numpy as np


class Ant(object):
    
    def __init__(self, env, energy = 100,  food_value = 10, genetic_inh=None, child = 0):
        
        self.energy = energy
        self.food_value = food_value

        self.food_harvest = 0
        self.enemy_killed = 0
        self.good_actions = 0
        self.bad_actions = 0
        self.neighbours = 0   
        self.movements = 0     
        
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
        self.starting_position = self.position                                                    
        if child == 1:
            # child
            self.brain = genetic_inh
        else:
            # first generation 
            self.brain = self.create_new_brain()


    def reset(self, energy, env):
        # reset values for 
        # fitness function
        self.energy = energy
        self.food_harvest = 0
        self.enemy_killed = 0
        self.good_actions = 0
        self.bad_actions = 0
        self.neighbours = 0  
        self.food_harvest = 0
        self.enemy_killed = 0
        self.movements = 0     

        # choose randomly position in environment
        env_size = env.get_size()
        while True:
            x = random.randint(0, env_size-1)
            y = random.randint(0, env_size-1)
            # position i, j is free
            if env.is_free(x, y):
                self.position = [x, y]    
                env.set_value(x, y, 2)
                break
        self.starting_position = self.position     
    
    def fitness(self, env):
        '''
        The following values are the coefficient of the fitness function
        Modify them will also modify the evolution parameters
        '''
        har_coef = 100
        kill_coef = 1000
        comb_coef = 2000
        good_coef = 1000
        bad_coef = 1000
        neig_coef = 5
        hp_coef = 3
        border_malus = 500000
        immobile_malus = 100000
        harvest_malus = 5000
        kill_malus = 2000
        movement_coef = 1500
        bonus_ratio = 25

        # Check the ant stats
        energy = self.energy
        surroundings = self.observe_environment(env, self.position)
        killings = self.enemy_killed
        harvest = self.food_harvest
        good_actions = self.good_actions
        bad_actions = self.bad_actions
        movements = self.movements
        malus = 0
        bonus = 0

        # Check ulterior stats to compute the bonus
        # and the malus
        global_neighbours = int(self.neighbours)
        if self.position[0] == 0 or \
            self.position[0] == env.get_size() - 1 or \
            self.position[1] == 0 or \
            self.position[1] == env.get_size() - 1:
            malus += border_malus
        
        if self.position[0] == 1 or \
            self.position[0] == env.get_size() - 2 or \
            self.position[1] == 1 or \
            self.position[1] == env.get_size() - 2:
            malus += border_malus/2

        if self.position == self.starting_position:
            malus += immobile_malus
        if killings == 0:
            malus += kill_malus
        if harvest == 0:
            malus += harvest_malus
        if surroundings[0] > 0:
            bonus += surroundings[0]*bonus_ratio
        
        # Evaluate the fitness function
        fitness = energy*hp_coef + global_neighbours * neig_coef + \
                    harvest*har_coef + killings*kill_coef + \
                    harvest*killings*comb_coef + good_actions*good_coef - \
                    bad_actions*bad_coef + movements*movement_coef - \
                    malus + bonus
        
        return fitness

    def create_new_brain(self):
        brain = []
        movement_neurons = init_weights([31,4])
        brain.append(movement_neurons)
        action_neurons = init_weights([27,3])
        brain.append(action_neurons)
        biases_neurons = init_weights([7])
        brain.append(biases_neurons)
        return brain

    def get_brain(self):
        # returns weigths NN
        return self.brain

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

    def get_neighbours(self, env):
        surroundings = self.observe_environment(env, self.position)
        self.neighbours += surroundings[0]

    def get_damage(self, env, colony, damage=0):
        # DAMAGE HAS TO BE A NEGATIVE NUMBER
        # returns true if it's dead
        self.energy = self.energy + damage
        if self.energy <= 0:
            env.remove_element(self.position[0], self.position[1])
            colony.remove(self)
            return True
        return False

    def get_surrounding(self, env, center):
        # return a matric 5X5 representing 
        # the surrounding of the ant
        env_size = env.get_size()
        inputs = np.zeros([9,3])
        for c in range(3):
            for i in range(3):
                for j in range(3):
                    x = (center[0]-1+i)
                    y = (center[1]-1+j)           
                    if not ((x<0) or (x > (env_size-1)) or \
                        (y<0) or (y > (env_size-1))):
                            if c == 0 and \
                                env.get_value(x, y) == 2:
                                inputs[i*3 + j][c] = 1
                            elif c == 1 and \
                                env.get_value(x, y) == -1:
                                inputs[i*3 + j][c] = 1
                            if c == 2 and \
                                env.get_value(x, y) == 1:
                                inputs[i*3 + j][c] = 1

        # subtract the value brought by the ant itself
        inputs[4][0] = 0
        input_eat = inputs
        input_attack = inputs
        for i in range (9):
            input_eat[i][1]
            input_attack[i][2]
        inputs = np.reshape(inputs, [-1])
        input_eat = np.reshape(input_eat, [-1])
        input_attack = np.reshape(input_attack, [-1])
        return inputs, input_attack, input_eat

    def observe_environment(self, env, center):
        # return a matric 3x3 representing 
        # the surrounding of the ant
        env_size = env.get_size()
        input = np.zeros([3])
        for c in range(3):
            for i in range(3):
                for j in range(3):
                    x = (center[0]-1+i)
                    y = (center[1]-1+j)           
                    if not ((x<0) or (x > (env_size-1)) or \
                        (y<0) or (y > (env_size-1))):
                            if c == 0 and \
                                env.get_value(x, y) == 2:
                                input[c] += 1
                            elif c == 1 and \
                                env.get_value(x, y) == -1:
                                input[c] += 1
                            if c == 2 and \
                                env.get_value(x, y) == 1:
                                input[c] += 1

            # subtract the value brought by the ant itself
            input[0] -= 1
            return input

    def pick_action(self, env):
        surrounding_env = np.zeros(31)
        patch_center = self.position

        for i in range (3):
            for j in range (3):
                patch_center[0] = self.position[0] - 1 + j
                patch_center[1] = self.position[1] - 1 + i
                observation = self.observe_environment(env, patch_center)
                for k in range(len(observation)):
                    surrounding_env[i*9 + j*3 + k] = observation[k]
        
        if self.position[0] <= 1:
            if self.position[0] <= 0:
                surrounding_env[27] = 3
            else:
                surrounding_env[27] = 1
        
        if self.position[1] <= 1:
            if self.position[1] <= 0:
                surrounding_env[28] = 3
            else:
                surrounding_env[28] = 1
        
        if self.position[0] >= env.get_size() - 2:
            if self.position[0] >= env.get_size() - 1:
                surrounding_env[29] = 3
            else:
                surrounding_env[29] = 1
        
        if self.position[0] >= env.get_size() - 2:
            if self.position[0] >= env.get_size() - 1:
                surrounding_env[30] = 3
            else:
                surrounding_env[30] = 1
        
        near_env, attack_matrix, eat_matrix = self.get_surrounding(env, self.position)
        
        movement_dir = np.matmul(surrounding_env.astype(float),
                            self.brain[0].astype(float))
        
        attack_value = np.matmul(attack_matrix.astype(float),
                                    self.brain[1].astype(float))[0]
        eat_value = np.matmul(eat_matrix.astype(float),
                                    self.brain[1].astype(float))[1]
        move_value = np.matmul(near_env.astype(float),
                                    self.brain[1].astype(float))[2]

        choosen_action = np.zeros([7])
        choosen_action[0] = attack_value
        choosen_action[1] = eat_value
        choosen_action[2] = move_value

        for i in range (4):
            choosen_action[i+3] = movement_dir[i]
        
        for i in range(len(choosen_action)):
            choosen_action[i] += self.brain[2][i]
            choosen_action[i] = max(choosen_action[i], 0)
        
        if max(choosen_action[0], choosen_action[1], choosen_action[2]) == choosen_action[0]:
            choosen_action[1] = 0
            choosen_action[2] = 0
        elif max(choosen_action[0], choosen_action[1], choosen_action[2]) == choosen_action[1]:
            choosen_action[0] = 0
            choosen_action[2] = 0
        elif max(choosen_action[0], choosen_action[1], choosen_action[2]) == choosen_action[2]:
            choosen_action[1] = 0
            choosen_action[0] = 0
        

        if choosen_action[3] >= choosen_action[4]:
            choosen_action[4] = 0
        else:
            choosen_action[3] = 0

        if choosen_action[5] >= choosen_action[6]:
            choosen_action[6] = 0
        else:
            choosen_action[5] = 0

        return choosen_action
    
    def get_target(self, env, action):
        # returns position of the nearest target
        env_size = env.get_size()
        for i in range(3):
            for j in range(3):
                x = (self.position[0]-1+i)
                y = (self.position[1]-1+j)
                if not ((x<0) or (x > env_size-1) or (y<0) or (y > env_size-1)):                        
                    if ((action==0) and (env.get_value(x, y) == -1)) or \
                            ((action  == 1) and (env.get_value(x, y) == 1)):
                        return([x, y])
        
        return(self.position)

    def move_or_act(self, env, next_move, dangers):
        env_size = env.get_size()
        x = self.position[0]
        y = self.position[1]

        if next_move[0] > 0:
            target_position = self.get_target(env, 0)
            if target_position != self.position:
                self.act(env, target_position, 0, dangers)
                self.good_actions += 1
            else:
                self.bad_actions -= 1

        elif next_move[1] > 0:
            target_position = self.get_target(env, 1)
            if target_position != self.position:
                self.act(env, target_position, 1, dangers)
                self.good_actions += 1
            else:
                self.bad_actions -= 1

        else:
            self.movements += 1     
            if next_move[3] > 0:
                if self.position[0] + 1 <= env.get_size() -1:
                    x += 1
            elif next_move[4] > 0:
                if self.position[0] - 1 >= 0:
                    x -= 1
            if next_move[5] > 0:
                if self.position[1] + 1 <= env.get_size() -1:
                    y += 1
            elif next_move[6] > 0:
                if self.position[1] - 1 >= 0:
                    y -= 1
            
            if x == self.position[0] and y == self.position[1]:                
                while True:
                    x = self.position[0] + random.randint(0, 3) - 1
                    y = self.position[1] + random.randint(0, 3) - 1
                    if ((x >= 0) and (x <= env_size-1) and (y >= 0) and \
                        (y <= env_size-1)):
                        break
                choosen_action = [x, y]
            else:
                choosen_action = [x, y]
            self.set_movement(env, choosen_action)

    def act(self, env, target_position, action, dangers):
        # performes action: attack or eat
        # attack
        if action == 0:
            for danger in dangers:
                if target_position == danger.get_position():
                    danger.add_attacking_ant(self.position)
        # eat            
        else:
            # status needs to be coherent with the action
            # rise its energy and his fitness parameter
            self.rise_energy(self.food_value)
            self.food_harvest += 1
            env.remove_element(target_position[0], target_position[1])

    def set_movement(self, env, choosen_action):
        new_x = choosen_action[0]
        new_y = choosen_action[1]        
        if [new_x, new_y] != self.position:
            if env.is_free(new_x, new_y) == True:
                self.move_to(env, new_x, new_y)
            else:
                target_position = self.find_nearest_free(env, [new_x, new_y])
                if target_position != self.position:
                    self.move_to(env,target_position[0], target_position[1])

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

    def move_to(self, env, x, y):
        env.remove_element(self.position[0], self.position[1])
        env.set_value(x, y, 2)
        self.position = [x, y]

    
# SUPPORT FUNCTION
# initialize NNR weights
def init_weights(shape):
    init_random_dist = np.random.normal(scale=3, size=shape)
    return init_random_dist
    
