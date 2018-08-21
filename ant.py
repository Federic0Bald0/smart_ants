# -*- coding: utf-8 -*-

# https://www.python.org/dev/peps/pep-0008/  ------ PEP8 style guide
import random
import numpy as np

def init_weights(shape):
    init_random_dist = np.random.normal(scale=3, size=[2,25])
    return init_random_dist

class Ant(object):
    
    def __init__(self, env, genetic_inh=None):
        
        self.energy = 20
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

        #JUST A CHECK
        self.id = random.randint(0, 100000)


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
        input = np.reshape(self.get_surrounding(env), [-1])

        # effective ant brain: a matrix multiplication betweeen inputs and weigths to produce the outputs
        # the highest output value is selected as next action
        # the weigths represent the genes that we are going to pass to the next generation

        # matmul for compute the NN output
        attack = np.matmul(input.astype(float), self.synapses[0].astype(float))
        eat = np.matmul(input.astype(float), self.synapses[1].astype(float))

        # manually applied RELU
        attack = max(attack, 0)
        eat = max(eat, 0)

        # if both action have low value the ant move at random
        if max(attack, eat, 100) == attack:
            action = 0
        elif  max(attack, eat, 100) == eat:
            action = 1
        else:
            action = 2
        self.status = action

        return action
    
    
    def set_movement(self, env, target_position):

        # set the direction of the incoming movement, X axis
        if (abs(self.position[0] - target_position[0])) == 1:
            new_x = self.position[0] + (target_position[0] - self.position[0])
            new_x = int(new_x)        
        elif (abs(self.position[0] - target_position[0])) == 2:
            new_x = self.position[0] + (target_position[0] - self.position[0])/2
            new_x = int(new_x)
        else:
            new_x = self.position[0]
        
        # Y axis
        if (abs(self.position[1] - target_position[1])) == 1:
            new_y = self.position[1] + (target_position[1] - self.position[1])
            new_y = int(new_y)
        elif (abs(self.position[1] - target_position[1])) == 2:
            new_y = self.position[1] + (target_position[1] - self.position[1])/2
            new_y = int(new_y)
        else:
            new_y = self.position[1]
        
        if [new_x, new_y] == self.position:
            self.move_to(env, new_x, new_y)
        else:
            if env.is_free(new_x, new_y) == True:
                self.move_to(env, new_x, new_y, m = 1)
            else:
                target_position = self.find_nearest_free(env, [new_x, new_y])
                if target_position == self.position:
                    self.move_to(env, target_position[0], target_position[1])
                else:
                    #print('check on value = ', env.get_value(new_x, new_y))
                    self.move_to(env,target_position[0], target_position[1], m = 1)

    def move_to(self, env, x, y, m=0):

        if m == 1:
            old_position = self.position
            self.position = [x, y]
            env.set_value(x, y, 2) # move ant 
            env.remove_element(old_position[0], old_position[1])
        
    def move_or_act(self, env, action, dangers):

        # pick the action
        #action = self.pick_action(env)
        
        env_size = env.get_size()
        # if the ants decide to move randomly
        if action == 2:
            
            # choose the new position
            x = -1
            while ((x<0) or ((x > env_size-1) or (y<0) or (y > env_size-1))):
                x = self.position[0] + random.randint(0, 3) - 1
                y = self.position[1] + random.randint(0, 3) - 1
            
            target_position = [x,y]
            
            # moves on it
            self.set_movement(env, target_position)
        
        # attack/eat scenario
        else:
        
            # read the target's location
            target_position = self.get_target(env, action)

            # if the target is near enough the ant move or eat
            if (abs(self.position[0] - target_position[0]) - 1) and (abs(self.position[1] - target_position[1]) - 1)\
                and (self.position != target_position):
               self.act(env, target_position, action, dangers)

            # if no it moves towards the target
            else:
                self.set_movement(env, target_position)
    
    # look at the close positions to see what's in it
    def get_surrounding(self, env):
        env_size = env.get_size()
        input = np.zeros([5,5])
        for i in range(5):
            for j in range(5):

                x = (self.position[0]-1+i)
                y = (self.position[1]-1+j)
            
                if not ((x<0) or (x > (env_size-1)) or \
                    (y<0) or (y > (env_size-1))):
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
    
    # funzione per il calcolo dei danni 
    def get_damage(self, env, damage= -1):
        self.energy = self.energy + damage
        if self.energy <= 0:
            env.remove_element(self.position[0], self.position[1])
            return False
        return True
        
    
    # TOTALLY CHANGED
    def find_nearest_free(self, env, target_position):
    # if no positions are free this function returns self.position and the ant does not move
    # also added a check for make sure that the ants doe not try to move out of the env

        # if X axis is the same the ant looks for the two closest position along the X axis
        env_size = env.get_size()
        
        if target_position[0] == self.position[0]:
            if (target_position[0]+1) < env_size-1:
                if env.is_free((target_position[0]+1), target_position[1]):
                    #print(env.get_value((target_position[0]+1), target_position[1]))
                    target_position = [(target_position[0]+1), target_position[1]]
                    return target_position
            if (target_position[0]-1) > 0:
                if env.is_free((target_position[0]-1), target_position[1]):
                    #print(env.get_value((target_position[0]-1), target_position[1]))
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
    
                    





        
