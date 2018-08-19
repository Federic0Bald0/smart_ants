# selection
# breeding
# mutate
from ants import Ant
import random
import numpy as np

def fitness(ant):
    energy = ant.energy
    killings = ant.enemy_killed
    harvest = ant.food_harvest
    fitness = energy/10 + harvest*10 + killings*10

#TODO CHECK THIS Fx
def grade_antts(colony):
    antsPerf = {}
    for ant in colony:
        antsPerf[ant] = fitness(ant)
    
    return sorted(antsPerf.items(), key = operator.itemgetter(1), reverse=True)

def selectFromPopulation(colony, best_sample, lucky_few):
	nextGen = []
	for i in range(best_sample):
		nextGen.append(populationSorted[i][0])
	for i in range(lucky_few):
		nextGen.append(random.choice(populationSorted)[0])
	random.shuffle(nextGe)
	return nextGen

def selectGenes(ant1, ant2):

    father_genes = ant1.synapses
    mother_genes = ant2.synapses
    gen_inheritance = []
    for i in range (len(father_genes)):
        if (int(100 * random.random()) < 50):
            gen_inheritance.append(father_genes[i])
        
        else:            
            gen_inheritance.append(mother_genes[i])
    
    return gen_inheritance

def createChildren(breeders, number_of_child):
	nextColony = []
    colony_shuffled = np.random.shuffle(np.arange(len(breeders)))
    for i in range(len(breeders)/2):
		for j in range(number_of_child):
            nextColony.append(Ant(genetic_inh = selectGenes(breeders[2*colony_shuffled[i]], (breeders[2*colony_shuffled[i]+1]))))
	return nextColony

def mutategenes(ant, mutation_prob):
    ant_genes = ant.synapses
    mutated_genes = []
    for gene in ant_genes:
        if (int(100 * random.random()) < mutation_prob):
            mutated_genes.append(ant_genes[gene]*random.random()/random.random())
        elif (int(100 * random.random()) > 100 - mutation_prob):
            mutated_genes.append(ant_genes[gene]+ random.random()*10 - random.random()*10)
        else:
            mutated_genes.append(ant_genes[gene])
    return mutated_genes

def mutatecolony(Colony, chance_of_mutation):
	for i in range(len(Colony)):
		if random.random() * 100 < chance_of_mutation:
			colony[i] = Ant(genetic_inh=mutategenes(colony[i], mutation_prob))
	return colony