# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt

for filename in os.listdir('test_results'):
    gen = []
    survivor = []
    avg = []
    best_ant = []
    with open('test_results/' + filename, 'r') as file:
        for line in file:
            temp = line.split()
            gen.append(int(temp[0]))
            survivor.append(int(temp[1]))
            avg.append(int(temp[2])) 
    plt.plot(gen, avg, color="green")
    plt.xlabel('generation')
    plt.ylabel('fitness')
    plt.savefig('test_results/' + filename + '_avg.png')
    plt.close()
    plt.plot(gen, survivor, color="red")
    plt.xlabel('generation')
    plt.ylabel('colony size')
    plt.savefig('test_results/' + filename + '_size.png')
    plt.close()