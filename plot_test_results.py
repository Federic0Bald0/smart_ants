# -*- coding: utf-8 -*-

import os
import matplotlib.pyplot as plt

for filename in os.listdir('test_results'):
    gen = []
    survivor = []
    avg = []
    best_ant = []
    with open('test_results/' + filename, 'r') as file:
        for line in file:
            temp = line.split()
            gen.append(temp[0])
            survivor.append(temp[1])
            avg.append(temp[2])
            best_ant.append(temp[3])

    plt.plot(gen, avg, color="green")
    plt.autoscale(enable=True, axis='y')
    plt.autoscale(enable=True, axis='x')
    plt.xticks(" ")
    plt.yticks(" ")
    plt.xlabel('generation')
    plt.ylabel('fitness')
    plt.savefig('test_results/' + filename + '_avg.png')
    plt.close()
    plt.plot(gen, best_ant, color="blue")
    plt.autoscale(enable=True, axis='y')
    plt.autoscale(enable=True, axis='x')
    plt.xticks(" ")
    plt.yticks(" ")
    plt.xlabel('generation')
    plt.ylabel('fitness')
    plt.savefig('test_results/' + filename + '_best_ant.png')
    plt.close()