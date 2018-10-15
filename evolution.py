# -*- coding: utf-8 -*-

import random
import operator
import numpy as np
from ant import Ant


def grade_ants(colony, colony_size, env):
    # sort ants using fitness function
    antsPerf = {}
    sum = 0
    for ant in colony:
        antsPerf[ant] = ant.fitness(env)
        sum += ant.fitness(env)
    # average fitness
    if sum == 0:
        avg = 0
        AVG = 0
    else:
        avg = sum/len(colony)
        AVG = sum/colony_size
    return sorted(antsPerf.items(), key = operator.itemgetter(1), reverse=True), avg, AVG


def select_from_population(colony, colony_size, best_sample, lucky_few, env):
    # selects ants from the colony
    nextGen = []
    population_sorted, avg, AVG = grade_ants(colony, colony_size, env)
    for i in range(best_sample):
        nextGen.append(population_sorted[i])
    for i in range(lucky_few):
        nextGen.append(random.choice(population_sorted))
    best_ant = population_sorted[0][0].fitness(env)
    random.shuffle(nextGen)
    return nextGen, avg, best_ant


def select_genes(ant1, ant2):
    # selects based on crossover value wich genes (weights)
    # are going to be used in the breeding process
    father_brain = ant1[0].get_brain()
    mother_brain = ant2[0].get_brain()
    gen_inheritance = []
    for i in range (len(father_brain)):
        father_brain_section = np.reshape(father_brain[i], [-1])
        mother_brain_section = np.reshape(mother_brain[i], [-1])
        new_brain_section = np.zeros([len(father_brain_section)])
        for j in range(len(father_brain_section)):
            if (int(100 * random.random()) < 50):
                new_brain_section[j] = father_brain_section[j]
            else:
                new_brain_section[j] = mother_brain_section[j]
        if i == 0:
            # movement brain
            new_brain_section = np.reshape(new_brain_section, [31,4])
        elif i == 1:
            # action brain
            new_brain_section = np.reshape(new_brain_section, [27,3])
            new_brain_section = np.reshape(new_brain_section, [27,3])
        gen_inheritance.append(new_brain_section)
    return gen_inheritance


def create_children(breeders, env, number_of_child, ants_energy, food_value):
    # creates children using genes from to selected ants
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
        nextColony.append(Ant(env, energy = ants_energy, food_value = food_value,
                                genetic_inh=brain, child=1))
    for j in range(number_of_child - (len(breeders)/2)):
        # if we need more children, we are going to use again some of the old parents
        random_parent = random.choice(breeders_indexes)
        brain = select_genes(breeders[random_parent],
                            breeders[len(breeders) - random_parent - 1])
        nextColony.append(Ant(env, energy = ants_energy, food_value = food_value,
                                genetic_inh=brain, child=1))
    return nextColony


def mutate_genes(ant, mutation_prob):
    # mutates the children we produced with the breeding
    ant_brain = ant.get_brain()
    mutated_genes = []

    for i in range(len(ant_brain)):
        brain_section = np.reshape(ant_brain[i], [-1])
        new_brain_section = np.zeros([len(brain_section)])

        for j in range(len(brain_section)):
            if (int(100 * random.random()) < mutation_prob) and i != 0:
                new_brain_section[j] = brain_section[j] * random.uniform(0, 1)
            elif (int(100 * random.random()) > 100 - mutation_prob) and i != 0:
                new_brain_section[j] = brain_section[j] + \
                random.uniform(0, 1)*10 - random.uniform(0, 1)*10
            else:
                new_brain_section[j] = brain_section[j]

        if i == 0:
            new_brain_section = np.reshape(new_brain_section, [31,4])
        elif i == 1:
            new_brain_section = np.reshape(new_brain_section, [27,3])
        mutated_genes.append(new_brain_section)
    return mutated_genes


def mutate_colony(colony, env, mutation_prob, ants_energy, food_value):
    # mutates the whole colony
    for i in range(len(colony)):
        if random.random() * 100 < mutation_prob:
            colony[i] = Ant(env, energy = ants_energy,
                            food_value = food_value,
                            genetic_inh=mutate_genes(colony[i], mutation_prob),
                            child=1)
    return colony