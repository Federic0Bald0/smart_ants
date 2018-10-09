# -*- coding: utf-8 -*-

import time
import random
import numpy as np


class Ant(object):
    
    def __init__(self, env, mode = 0, genetic_inh=None, child = 0):
        
        self.energy = 100
        self.food_harvest = 0
        self.enemy_killed = 0
        self.status = 2
        self.good_actions = 0
        self.neighbours = 0
        self.mode = mode
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

        
    
    def create_new_brain(self):

        brain = []
        # sensors_outer = init_weights([3,2])
        sensors_outer = np.array([[-0.622128, 0.46205002], [-0.04153039, -0.22355694], [ 0.44143412, 0.7377847 ]], dtype = np.float32)
        brain.append(sensors_outer)
        sensors_central = init_weights([31,4])
        brain.append(sensors_central)
        sensors_inner = init_weights([7])
        brain.append(sensors_inner)
        priority_outer = init_weights([2])
        brain.append(priority_outer)
        priority_central = init_weights([2])
        brain.append(priority_central)
        priority_inner = init_weights([2])
        brain.append(priority_inner)
        destination_neurons = init_weights([9,4])
        brain.append(destination_neurons)
        actions_filter = init_weights([3,2])
        brain.append(actions_filter)
        action_neurons = init_weights([27,3])
        brain.append(action_neurons)

        return brain

    def get_neighbours(self, env):
        surroundings = self.get_small_surrounding(env, self.position)
        self.neighbours += surroundings[0]


    def reset(self, env, mode):
        # reset values for 
        # fitness function
        self.energy = 50
        self.food_harvest = 0
        self.enemy_killed = 0
        self.status = 2
        self.good_actions = 0
        self.neighbours = 0
        self.mode = mode
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
        self.starting_position = self.position

    def fitness(self, env):
        m = 0
        b = 0
        global_neighbours = int(self.neighbours)
        if self.position[0] == 0 or \
            self.position[0] == env.get_size() - 1 or \
            self.position[1] == 0 or \
            self.position[1] == env.get_size() - 1:
            m += 3000
        if self.position[0] == 1 or \
            self.position[0] == env.get_size() - 2 or \
            self.position[1] == 1 or \
            self.position[1] == env.get_size() - 2:
            m += 1500
        surroundings = self.get_small_surrounding(env, self.position)
        if surroundings[0] > 0:
            b += surroundings[0]*25
        good_actions = self.good_actions
        if self.position == self.starting_position:
            m += 10000
        energy = self.energy
        killings = self.enemy_killed
        if killings == 0:
            m += 1000
        harvest = self.food_harvest
        if harvest == 0:
            m += 1000
        # print(m)
        fitness = energy*0 + harvest*100 + killings*750 - m + b*0 + max(good_actions, 0)*300 + min(good_actions, 0) * 100 + global_neighbours * 3 + harvest*killings*2000
        # print(fitness)
        return fitness

    def get_status(self):
        # status defines what ant

        # is allowed to do:
        #
        # 0 -> attacking
        # 1 -> eating
        # 2 -> moving
        return self.status

    def get_brain(self):
        # returns weigths NN
        return self.brain

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

        surrounding_env = []
        ####
        close_env = np.zeros(31)
        patch_center = self.position

        for i in range (3):
            for j in range (3):
                patch_center[0] = self.position[0] - 1 + j
                patch_center[1] = self.position[1] - 1 + i
                observation = self.get_small_surrounding(env, patch_center)
                for k in range(len(observation)):
                    close_env[i*9 + j*3 + k] = observation[k]
                    ###
                surrounding_env.append(observation)  
        
        if self.position[0] <= 1:
            if self.position[0] <= 0:
                close_env[27] = 2
            else:
                close_env[27] = 1
        
        if self.position[1] <= 1:
            if self.position[1] <= 0:
                close_env[28] = 2
            else:
                close_env[28] = 1
        
        if self.position[0] >= env.get_size() - 2:
            if self.position[0] >= env.get_size() - 1:
                close_env[29] = 2
            else:
                close_env[29] = 1
        
        if self.position[0] >= env.get_size() - 2:
            if self.position[0] >= env.get_size() - 1:
                close_env[30] = 2
            else:
                close_env[30] = 1
        
        close_surr = self.get_small_surrounding(env, self.position)
        surrounding_env.append(close_surr)
        ###
        env_around = self.get_surrounding(env, self.position)
        ###
    
        # possible_actions = np.zeros(18)

        # biases = np.array([-2.3995202, -1.6695873], dtype = np.float32)

        # for i in range (9):
        #     actions = np.matmul(surrounding_env[i].astype(float),
        #                             self.brain[0].astype(float))
        #     for k in range(len(actions)):
        #         actions[k] = actions[k] + biases[k]
        #         actions[k] = max(actions[k], 0)
        #         possible_actions[i*2 + k]


        # destination = np.matmul(possible_actions.astype(float),
        #                             self.brain[1].astype(float))

        
        dest = np.matmul(close_env.astype(float),
                                    self.brain[1].astype(float))

        choose_action = np.matmul(env_around.astype(float),
                                    self.brain[8].astype(float))

        destination = np.zeros([7])
        for i in range(3):
            destination[i] = choose_action[i]
        for i in range (4):
            destination[i+3] = dest[i]
        
        for i in range(len(destination)):
            destination[i] += self.brain[2][i]
            destination[i] = max(destination[i], 0)
        
        if max(destination[0], destination[1], destination[2]) == destination[0]:
            destination[1] = 0
            destination[2] = 0
        elif max(destination[0], destination[1], destination[2]) == destination[1]:
            destination[0] = 0
            destination[2] = 0
        elif max(destination[0], destination[1], destination[2]) == destination[2]:
            destination[1] = 0
            destination[0] = 0
        
        for i in range(2):
            if destination[i*2+3] >= destination[i*2+4]:
                destination[i*2+4] = 0
            else:
                destination[i*2+3] = 0


        # for i in range(2):
        #     outer_actions = np.matmul(surrounding_env[2*i].astype(float),
        #                             self.brain[0].astype(float))
        #     for i in range(len(outer_actions)):
        #         outer_actions[i] = max(outer_actions[i], 0)
        #     possible_actions.append(outer_actions)
        # for i in range(2):
        #     outer_actions = np.matmul(surrounding_env[2*i+6].astype(float),
        #                             self.brain[0].astype(float))
        #     for i in range(len(outer_actions)):
        #         outer_actions[i] = max(outer_actions[i], 0)
        #     possible_actions.append(outer_actions)
        # for i in range(4):
        #     central_actions = np.matmul(surrounding_env[2*i + 1].astype(float),
        #                                 self.brain[0].astype(float))
        #     for i in range(len(central_actions)):
        #         central_actions[i] = max(central_actions[i], 0)
        #     possible_actions.append(central_actions)
        # inner_actions = np.matmul(surrounding_env[2*i + 1].astype(float),
        #                         self.brain[0].astype(float))
        # for i in range(len(inner_actions)):
        #     inner_actions[i] = max(inner_actions[i], 0)
        # possible_actions.append(inner_actions)

        # priority = np.zeros([9])
        # for i in range (4):
        #     priority[i] = np.matmul(possible_actions[i].astype(float),
        #                             self.brain[3].astype(float))
        # for i in range (4):
        #     priority[i+4] = np.matmul(possible_actions[i+4].astype(float),
        #                             self.brain[4].astype(float))
        # priority[8] = np.matmul(possible_actions[8].astype(float),
        #                             self.brain[5].astype(float))
        # for i in range(len(priority)):
        #     priority[i] = max(priority[i], 0)
        
        # destination = np.matmul(priority.astype(float),
        #                             self.brain[6].astype(float))        
        
        # for i in range(len(destination)):
        #     destination[i] = max(destination[i], 0)
        # if destination[0] >= destination[1]:
        #     destination[1] = 0
        # else:
        #     destination[0] = 0
        # if destination[2] >= destination[3]:
        #     destination[2] = 0
        # else:
        #     destination[3] = 0
        
        # last_inputs = np.zeros([7])
        # for i in range(len(destination)):
        #     last_inputs[i] = destination[i]    

        # for i in range(3):
        #     last_inputs[i+len(destination)] = surrounding_env[4][i]
        
        # for i in range(3):
        #     last_inputs[i+len(destination) + 3] = surrounding_env[9][i]  


        # possible_actions = np.matmul(surrounding_env[9].astype(float),
        #                             self.brain[0].astype(float))
        # for i in range (len(possible_actions)):
        #     possible_actions[i] += biases[i]
        #     last_inputs[i+len(destination)] = possible_actions[i]
        
        # for i in range(2):
        #     last_inputs[i+len(destination)] = possible_actions[i]    
        #     
        # outer_actions = np.matmul(surrounding_env[4].astype(float),
        #                             self.brain[0].astype(float))   

        # for i in range (len(outer_actions)):
        #     outer_actions[i] += biases[i]
        #     last_inputs[i+len(destination)+len(possible_actions)] = outer_actions[i]

        # for i in range(2):
        #     last_inputs[i + len(destination) + len(possible_actions)] = \
        #     outer_actions[i]        
        # for i in range(len(last_inputs)):
        #     last_inputs[i] = max(last_inputs[i], 0)

        # choosen_action = np.matmul(last_inputs.astype(float),
        #                             self.brain[8].astype(float))

        # # add biases
        # for i in range(len(choosen_action)):
        #     choosen_action[i] += self.brain[2][4+i]

        # for i in range(len(choosen_action)):
        #     choosen_action[i] = max(choosen_action[i], 0)

        # if choosen_action[0] >= choosen_action[1]:
        #     choosen_action[1] = 0
        # else:
        #     choosen_action[0] = 0
        # next_move = []
        # for i in range(len(choosen_action)):
        #     next_move.append(choosen_action[i])
        # for i in range(len(destination)):
        #     next_move.append(destination[i])
        return destination
    
    def move_or_act(self, env, next_move, dangers):
        env_size = env.get_size()
        x = self.position[0]
        y = self.position[1]
        if next_move[0] > 0:
            # print('I WANNA ATTACK')
            target_position = self.get_target(env, 0)
            if target_position != self.position:
                self.act(env, target_position, 0, dangers)
                self.good_actions += 3
            else:
                self.good_actions -= 1
        elif next_move[1] > 0:
            target_position = self.get_target(env, 1)
            if target_position != self.position:
                self.act(env, target_position, 1, dangers)
                self.good_actions += 3
            else:
                self.good_actions -= 1
        else:
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
                destination = [x, y]
            else:
                destination = [x, y]
            self.set_movement(env, destination)

    def set_movement(self, env, destination):
        new_x = destination[0]
        new_y = destination[1]        
        if [new_x, new_y] != self.position:
            if env.is_free(new_x, new_y) == True:
                self.move_to(env, new_x, new_y)
            else:
                target_position = self.find_nearest_free(env, [new_x, new_y])
                if target_position != self.position:
                    self.move_to(env,target_position[0], target_position[1])

    def move_to(self, env, x, y):
        env.remove_element(self.position[0], self.position[1])
        env.set_value(x, y, 2)
        self.position = [x, y]
    
    def get_surrounding(self, env, center):
        # return a matric 5X5 representing 
        # the surrounding of the ant
        env_size = env.get_size()
        input = np.zeros([9,3])
        for c in range(3):
            for i in range(3):
                for j in range(3):
                    x = (center[0]-1+i)
                    y = (center[1]-1+j)           
                    if not ((x<0) or (x > (env_size-1)) or \
                        (y<0) or (y > (env_size-1))):
                            if c == 0 and \
                                env.get_value(x, y) == 2:
                                input[i*3 + j][c] = 1
                            elif c == 1 and \
                                env.get_value(x, y) == -1:
                                input[i*3 + j][c] = 1
                            if c == 2 and \
                                env.get_value(x, y) == 1:
                                input[i*3 + j][c] = 1

        # subtract the value brought by the ant itself
        input[4][0] = 0
        input = np.reshape(input, [-1])
        return input

    def get_small_surrounding(self, env, center):
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
            self.rise_energy(10)
            self.food_harvest += 1
            env.remove_element(target_position[0], target_position[1])
            # print env.get_value(target_positon[0], target_position[1])

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
    

    def get_damage(self, env, colony, damage=0):
        # given the damage the function
        # updates the energy of the ant
        # returns true if it's dead
        self.energy = self.energy + (damage * 10)
        if self.energy <= 0:
            env.remove_element(self.position[0], self.position[1])
            colony.remove(self)
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
    init_random_dist = np.random.normal(scale=3, size=shape)
    return init_random_dist
    
