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
                    

    def pick_action(self, env):

    #   osserva l-abiente circostante
        input = check_surrounding(env)

    #   matmul per determinare quale azione esegure + relu
        attack = tf.nn.relu(tf.matmul(input, self.synapses[0]))[0]
        eat = tf.nn.relu(tf.matmul(input, self.synapses[1]))[0]

    #   sceglie l'azione con il valore maggiore
    #   se entrambe le azioni possibili hanno un valore basso si muove in una direzione a caso
        action = tf.argmax([attack, eat, 0.2])        

        return action
    
    
    def move_to_target(self, target_position): 

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

        if self.env.is_free(target_position) == False
            target_position = find_nearest_free(target_position)

        self.position = [new_x, new_y]
        
    def move_or_act(self, action):

        # se l'azione scelta e' un movimento casuale
        if action == 2:
            
        #   determina la direzione del movimento
            target_position = [self.position[0] + random.randint(0, 3) - 1]
            target_position = [self.position[0] + random.randint(0, 3) - 1]

        #   effettua il movimento
            self.move_to_target(target_position)
        
        # se invece vuole effettuare una posizione specifica
        else:
        
        #determina la posizione dell'obiettivo
            target_position = self.get_target(action)

            # se l'obiettivo della propria azione si trova in una delle caselle adiacenti la formica esegue una delle due azioni disponibili
            if (abs(self.position[0] - target_position[0]) - 1) and (abs(self.position1[1]] - target_position[1]) - 1):
               self.act(target_position, action)

            # altrimenti si muove verso di esso
            else:
                self.move_to_target(target_position)
    
    # esamina le posizioni vicino ad essa
    def check_surrounding(self, env):

        input = np.zeros([5,5], dype=np.float32)
        for i in range(5):
            input[i] = env[self.position[0]-2+i, self.position[1]-2 : self.position[1]+2]
        # restitusce il un arrya con shape ([24]), non una matrice
        np.reshape(input, [24])

        return (input)
    
    # altra funzione per esaminare le poszioni adiacenti
    def get_surrounding(self, env):

        # large_surrounding indica il quaadrato 5x5 intorno alla formica
        large_surrounding = np.zeros([5,5], dype=np.float32)
        # small_surrounding indica il quaadrato 3x3 intorno alla formica
        small_surrounding = np.zeros([3,3], dype=np.float32)

        for i in range(5):
            large_surrounding[i] = env[self.position[0]-2+i, self.position[1]-2 : self.position[1]+2]
        
        for i in range(3):
            small_surrounding[i] = env[self.position[0]-2+i, self.position[1]-2 : self.position[1]+2]
        
        return (small_surrounding, large_surrounding)

    # esegue l'azione scelta (attack o eat) su un obiettivo adicente ad essa
    def act(target_position, action):

        if action == 0:
    #       attack
        else:
    #       eat

    # rileva la posizione del suo target in base all'azione che vuole effettuare
    def get_target(self, action):

        # la ricerca e' effettuata dapprima sulle caselle adiacenti alla formica (il quadrato 3x3)
        # e poi sulle caselle della cornice piy' esterna
        small_surrounding, large_surrounding = self.check_surrounding(env)

        # se l'azione scelta e' eat
        if action == 0:

            # restituaisce la poszione del cibo piu' vicino
            for i in range (3):
                for j in range (3):
                    if small_surrounding[self.position[0]-1+i, self.position[1]-1+j] < 0
                        return (self.position[0]-1+i, self.position[1]-1+j)
            
            for i in range (5):
                for j in range (5):
                    if small_surrounding[self.position[0]-2+i, self.position[1]-2+j] < 0 
                        return (self.position[0]-2+i, self.position[1]-2+j)
        
         # se l'azione scelta e' attack
        if action == 0:

            # restituisce la posizione del nemico piu' vicino
            for i in range (3):
                for j in range (3):
                    if small_surrounding[self.position[0]-1+i, self.position[1]-1+j] == 1
                        return (self.position[0]-1+i, self.position[1]-1+j)
            
            for i in range (5):
                for j in range (5):
                    if small_surrounding[self.position[0]-2+i, self.position[1]-2+j] == 1
                        return (self.position[0]-2+i, self.position[1]-2+j)
    
    # funzione per il calcolo dei danni 
    def get_damage(self, damage=1):
        self.energy = self.energy - damage
        
        if self.energy <= 0:
            self.die
    
    # fuzione che la formica effettua ad ogni turno come 'routine'
    # ovvero: esamina l'ambiente --> scegli un'azione --> effettua l'azione --> prendi 1 danno
    def make_a_move(self):

        env = self.read_env()
        self.pick_action(env)
        self.move_or_act
        self.get_damage
    
    # se la posizione desiderata e' occupata si muove nella prima posizione libera controllando
    # le posizioni in senso antiorario
    def find_nearest_free(self, target_position, end=False):

        c = 0
        while end == False and c < 9:

            if target_position[0] < self.position[0]:
                if target_position[1] <= self.position[1]:

                    target_position[1] = target_position[1] + 1 
                    end = self.env.is_free(target_position)
                                                  
                else:
                    target_position[0] = target_position[0] + 1
                    end = self.env.is_free(target_position)

            if target_position[0] = self.position[0]:
                if target_position[1] < self.position[1]:

                    target_position[0] = target_position[0] - 1 
                    end = self.env.is_free(target_position)
                
                else:

                    target_position[0] = target_position[0] + 1 
                    end = self.env.is_free(target_position)
            
            if target_position[0] > self.position[0]:
                if target_position[1] >= self.position[1]:

                    target_position[1] = target_position[1] - 1 
                    end = self.env.is_free(target_position)
                
                else:

                    target_position[0] = target_position[0] - 1 
                    end = self.env.is_free(target_position)

        id c > 8:
            target_position = self.position
        
        return(target_position)

    #aumenta la propria energia
    def get_energy(self, energy):
        self.energy = self.energy + energy
                    
    
    # fuzione che aggiorna lo stato attuale dell'ambiente
    def read_env():
        
        ### need something
        pass



############ TODO
#   READ ENVIRONMENT
#   EAT SIGNAL
#   ATTACK SIGNAL
#   CHANGE env[] to get_stuff ...
    
                    





        
