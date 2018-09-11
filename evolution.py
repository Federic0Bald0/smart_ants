# -*- coding: utf-8 -*-

import random
import operator
import numpy as np
from ant import Ant

#TODO CHECK THIS Fx
def grade_ants(colony):
    antsPerf = {}
    for ant in colony:
        antsPerf[ant] = ant.fitness()
    return sorted(antsPerf.items(), key = operator.itemgetter(1), reverse=True)

def select_from_population(colony, best_sample, lucky_few):
    nextGen = []
    population_sorted = grade_ants(colony)
    print ('BEST ANT FITNESS SCORE:')
    print (population_sorted[0][0].fitness())
    for i in range(best_sample):
        nextGen.append(population_sorted[i])
    for i in range(lucky_few):
        nextGen.append(random.choice(population_sorted))
    random.shuffle(nextGen)
    return nextGen

'''
    In queste funzioni potrebbe essere necessario un reshape delle sinapsi da [2,25] a [50]    
'''
def select_genes(ant1, ant2):
    father_genes = np.reshape(ant1[0].get_synapses(), [-1])
    mother_genes = np.reshape(ant2[0].get_synapses(), [-1])
    gen_inheritance = []

    for i in range (len(father_genes)):
        if (int(100 * random.random()) < 50):
            gen_inheritance.append(father_genes[i])        
        else:            
            gen_inheritance.append(mother_genes[i])
    
    gen_inheritance = np.reshape(gen_inheritance, [2,25])
    return gen_inheritance

def create_children(breeders, env, number_of_child):
    nextColony = []
    breeders_indexes = np.arange(len(breeders))
    breeders_indexes_shuffled = np.arange(len(breeders))
    np.random.shuffle(breeders_indexes_shuffled)
    
    for i in range(len(breeders)/2):
        # first round of childrean, each pair of randomly selected parents create one of them
        # each parent can be selected only once
        first_parent_id = breeders_indexes_shuffled[i]
        second_parent_id = breeders_indexes_shuffled[len(breeders_indexes_shuffled) - i - 1]
        synapses = select_genes(breeders[first_parent_id], breeders[second_parent_id])
        nextColony.append(Ant(env, genetic_inh=synapses))

    for j in range(number_of_child - (len(breeders)/2)):
        # if we need more children, we are going to use again some of the old parents
        random_parent = random.choice(breeders_indexes)
        synapses = select_genes(breeders[random_parent], breeders[len(breeders) - random_parent - 1])
        nextColony.append(Ant(env, genetic_inh=synapses))
    return nextColony

def mutate_genes(ant, mutation_prob):
    ant_genes = np.reshape(ant.get_synapses(), [-1])
    mutated_genes = []
    for gene in ant_genes:
        if (int(100 * random.random()) < mutation_prob):
            mutated_genes.append(gene * random.uniform(0, 1))
        elif (int(100 * random.random()) > 100 - mutation_prob):
            mutated_genes.append(gene + random.uniform(0, 1)*10 - random.uniform(0, 1)*10)
        else:
            mutated_genes.append(gene)
    mutated_genes = np.reshape(mutated_genes, [2,25])
    return mutated_genes

def mutate_colony(colony, env, mutation_prob):
    for i in range(len(colony)):
        if random.random() * 100 < mutation_prob:
            colony[i] = Ant(env, genetic_inh=mutate_genes(colony[i], mutation_prob))
    return colony



'''
OLD AND DEPRECATED

def create_children(breeders, env, number_of_child): # number of child???
    nextColony = []
    # la riga immediatamente sotto e' inutile a questo punto
    breeders_indexes = np.arange(len(breeders))
    for i in range(len(breeders)/2):
        for j in range(number_of_child):
            synapses = select_genes(breeders[i], breeders[len(breeders) - 1 - i]) # 1 (+) (-1)... is this good?
            # random_parent = random.choice(breeders_indexes)
            # synapses = select_genes(breeders[random_parent], breeders[len(breeders) - random_parent - 1])
            nextColony.append(Ant(env, genetic_inh=synapses))
    return nextColony
'''