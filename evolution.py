# -*- coding: utf-8 -*-

import random
import operator
import numpy as np
from ant import Ant

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


def select_genes(ant1, ant2):
    father_genes = ant1[0].get_brain
    mother_genes = ant1[0].get_brain
    gen_inheritance = []

    for i in range (len(father_genes)):
        father_brain_section = np.reshape(father_genes[i], [-1])
        mother_brain_section = np.reshape(mother_genes[i], [-1])
        new_brain_section = np.zeros([len(father_brain_section)])
        for j in range(len(father_brain_section)):
            if (int(100 * random.random()) < 50):
                new_brain_section[j] = father_brain_section[j]     
            else:
                new_brain_section[i] = mother_brain_section[i]
        if 1 <= 2:
            new_brain_section = np.reshape(new_brain_section, [2,3])
        if 1 == 6:
            new_brain_section = np.reshape(new_brain_section, [4,9])
        if 1 == 7:
            new_brain_section = np.reshape(new_brain_section, [2,3])
        if 1 == 8:
            new_brain_section = np.reshape(new_brain_section, [2,8])
        gen_inheritance.append(new_brain_section)    
    return gen_inheritance

def create_children(breeders, env, number_of_child, mode = 0):
    nextColony = []
    breeders_indexes = np.arange(len(breeders))
    breeders_indexes_shuffled = np.arange(len(breeders))
    np.random.shuffle(breeders_indexes_shuffled)
    
    for i in range(len(breeders)/2):
        # first round of childrean, each pair of randomly selected parents create one of them
        # each parent can be selected only once
        first_parent_id = breeders_indexes_shuffled[i]
        second_parent_id = breeders_indexes_shuffled[len(breeders_indexes_shuffled) - i - 1]
        brain = select_genes(breeders[first_parent_id], breeders[second_parent_id])
        nextColony.append(Ant(env, mode, genetic_inh=brain))

    for j in range(number_of_child - (len(breeders)/2)):
        # if we need more children, we are going to use again some of the old parents
        random_parent = random.choice(breeders_indexes)
        brain = select_genes(breeders[random_parent], breeders[len(breeders) - random_parent - 1])
        nextColony.append(Ant(env, mode, genetic_inh=brain))
    return nextColony

def mutate_genes(ant, mutation_prob):
    ant_brain = ant.get_brain
    mutated_genes = []
    for i in range(len(ant_brain))
        brain_section = np.reshape(ant_brain[1], [-1])
        new_brain_section = np.zeros([len(brain_section)])
        for j in range(len(brain_section)):
            if (int(100 * random.random()) < mutation_prob):
                new_brain_section[j] = brain_section[j] * random.uniform(0, 1)
            elif (int(100 * random.random()) > 100 - mutation_prob):
                new_brain_section[j] = brain_section[j] + random.uniform(0, 1)*10 - random.uniform(0, 1)*10
            else:
                new_brain_section[j] = brain_section[j]
        if 1 <= 2:
            new_brain_section = np.reshape(new_brain_section, [2,3])
        if 1 == 6:
            new_brain_section = np.reshape(new_brain_section, [4,9])
        if 1 == 7:
            new_brain_section = np.reshape(new_brain_section, [2,3])
        if 1 == 8:
            new_brain_section = np.reshape(new_brain_section, [2,8])
        mutated_genes.append(new_brain_section)    
    return mutated_genes

def mutate_colony(colony, env, mutation_prob, mode = 0):
    for i in range(len(colony)):
        if random.random() * 100 < mutation_prob:
            colony[i] = Ant(env, mode, genetic_inh=mutate_genes(colony[i], mutation_prob))
    return colonye(len(colony)):
        if random.random() * 100 < mutation_prob:
            colony[i] = Ant(env, genetic_inh=mutate_genes(colony[i], mutation_prob))
    return colony

