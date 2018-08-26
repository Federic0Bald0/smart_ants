# -*- coding: utf-8 -*-

import time
import random
import numpy as np


class Ant(object):
    
    def __init__(self, env, genetic_inh=None):
        
        self.energy = 50
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

    def reset(self, env):
        # reset values for 
        # fitness function
        self.energy = 50
        self.food_harvest = 0
        self.enemy_killed = 0
        self.status = 2
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

    def fitness(self):
        energy = self.energy
        killings = self.enemy_killed
        harvest = self.food_harvest
        fitness = energy/10 + harvest*10 + killings*10
        return fitness

    def get_status(self):
        # status defines what ant
        # is allowed to do:
        #
        # 0 -> attacking
        # 1 -> eating
        # 2 -> moving
        return self.status

    def get_synapses(self):
        # returns weigths NN
        return self.synapses


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
        """ 
        Ho ripristinato le variabili come prima

        L'idea e' quella di cercare i bug nelle varie funzioni in maienra separata:
        Io avevo gia' testato la funzione di moveimento valutando il vettore (attack, eat, 1000)

        E quella di Eat con (attack, 1000, 1).
        
        Entrambe le funzioni sembravano fare il loro dovere l'unico piccolo bug e' che le formiche
        non percepivano i target a due caselle di distanza (ma se il cibo era adiacente a loro lo 
        senza problemi)
        """
        if max(attack, eat, 1) == attack:
            action = 0
        elif max(attack, eat, 1) == eat:
            action = 1
        else:
            action = 2
        self.set_status(action)

        return action
    
    
    def set_movement(self, env, target_position, dangers):
        # function sets direction of the incoming movement

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

            """ 
            Questa parte rappresentava il caso in cui la formica non aveva la possibilita' di avvicinarsi al
            bersaglio, allora settava il target uguale alla sua posizione e la passava alla funzione ed in un 
            un successivo controllo del tipo

            if (target_position == self.position):
                self.move_to(env, new_position[0], new_position[1], m = 0)
            decideva si non fare nulla perche' la variabile m era settata a 0

            ma come effettivamente mi hai fatto notare ci sono delle parti ridondanti quindi vanno riviste

            pero' dato che preferirei non mettere mano al tuo codice faro' queste piccole modifiche nella fuzione che 
            ho aggiunto in commento a fondo pagina (che era quella vecchia che usavo io)

            il cosiglio che ti do per testarle e' di settare 

            if max(attack, eat, 1000) == attack:
                action = 0
            elif max(attack,eat, 1000) == eat:
                action = 1
            else:
                action = 2
            self.set_status(action)

            qeusti valori e fari test: in questo modo le formiche si muovono e basta e cercare dei bug
            nel movimento e' piu' semplice

            """
            new_y = self.position[1]
        
        if [new_x, new_y] != self.position:
            if env.is_free(new_x, new_y) == True:
                self.move_to(env, new_x, new_y)
            else:
                target_position = self.find_nearest_free(env, [new_x, new_y])
                if target_position != self.position:
                    self.move_to(env,target_position[0], target_position[1])

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

        # if not env.is_free(new_x, new_y):
        #     new_position = self.find_nearest_free(env, target_position)
        #     self.move_to(env, new_position[0], new_position[1])
        # elif (target_position != self.position):
        #     self.move_to(env, new_position[0], new_position[1])


    def move_to(self, env, x, y):
        """ 
        il parametro m lo usavo per assicurarmi che la formica non si muovesse se non doveva
        ma come hai scritto tu la funzione e' meglio e quindi la teniamo cosi'
        """
        env.remove_element(self.position[0], self.position[1])
        env.set_value(x, y, 2)
        self.position = [x, y]
         
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
            '''
            in questo if la formica controlla se il bersaglio e' in uno dei quadretti adiacenti ad essa:
            se lo e' effettua l'azione designata
            '''
            # read the target's location
            target_position = self.get_target(env, action)
            # if the target is near enough the ant move or eat
            if ((abs(self.position[0] - target_position[0]) - 1) <= 0) \
                and ((abs(self.position[1] - target_position[1]) - 1) <= 0) \
                and (self.position != target_position):
                self.act(env, target_position, action, dangers)
            # else moves it towards the target
            else:
                '''
                altrimenti si muove per avvicinarsi
                '''
                # move towards the target
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
                    danger.get_damage(env, dangers)
        # eat            
        else:
            # status needs to be coherent with the action
            if self.get_status() != 1:
                self.set_status(1)
            # rise its energy and his fitness parameter
            self.rise_energy(10)
            self.food_harvest += 1
            env.remove_element(target_position[0], target_position[1])
            # print env.get_value(target_positon[0], target_position[1])


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
    init_random_dist = np.random.normal(scale=3, size=[2,25])
    return init_random_dist
    


    '''

    OLD SET_MOVEMENT

    # per leggerlo ti conviene togliere il commento generale
    # i commenti in italiano pensavo di toglierli alla fine, stanno qui solo per te
    
    
    def set_movement(self, env, target_position):

        # The ant moves to tareget_position
        # set the direction of the incoming movement, X axis

        if (abs(self.position[0] - target_position[0])) == 1:

            # in questo caso la posizione bersaglio si trova ad una colonna di distanza dalla formica
            # la formica si prepara a muoversi di 1 quella direzione (l'asse delle X)
            new_x = self.position[0] + (target_position[0] - self.position[0])
            new_x = int(new_x)  

        elif (abs(self.position[0] - target_position[0])) == 2:      

            # in questo caso la posizione bersaglio si trova a due colonne di distanza dalla formica
            # la formica si prepara a muoversi di 1 quella direzione (l'asse delle X)
            # anche se il movimento e' sempre di uno ho usato due diversi controlli, altrimenti
            # la formica si sarebbe mossa di due caselle e questo non va bene (infatti nella prossima riga c'e /2)

            # IMPORTANTE
                # se siamo in questa parte significa che target_position rappresenta la funzione
                # del bersaglio da attaccare/mangiare e NON quella della posizione in cui muoversi
                # ma dato che in questo caso target_position sarebbe comunque irraggingibile
                # questa funzione viene usata per avvicinarsi ad esso

            new_x = self.position[0] + (target_position[0] - self.position[0])/2
            new_x = int(new_x)

        else:
            # formica e bersaglio sono sulla stessa colonna
            # la formica non si sposta da essa
            new_x = self.position[0]
        
        # Y axis
        # stesso lavoro di prima
        if (abs(self.position[1] - target_position[1])) == 1:
            new_y = self.position[1] + (target_position[1] - self.position[1])
            new_y = int(new_y)
        elif (abs(self.position[1] - target_position[1])) == 2:
            new_y = self.position[1] + (target_position[1] - self.position[1])/2
            new_y = int(new_y)
        else:
            new_y = self.position[1]
        
        # new_x = self.position[0]
        # new_y = self.position[1] e' necessrio perche' la funzione get_target
        # restituisce target.position = self.position se non trova alcun target per l-azione designata
        # cosa che potrebbe benissimo succedere nelle simuzioni
        # ed in questo caso la formica non deve fare nulla e per assicurarmi di cio'
        # ho usato l'if sottostante


        # a this point the ant try to move just if [new_x, new_y] != self.position
        if [new_x, new_y] != self.position:

            # firt chechk to make sure that the designed position is free
            if env.is_free(new_x, new_y) == True:

                # if it is the ant moves
                self.move_to(env, new_x, new_y)

            else:

                # else she look for the closest free position
                target_position = self.find_nearest_free(env, [new_x, new_y])
                if target_position != self.position:
                    
                    # and she moves just if she finds one
                    self.move_to(env, target_position[0], target_position[1])



'''
                    





        
