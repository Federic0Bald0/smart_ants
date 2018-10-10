# -*- coding: utf-8 -*-

# 50 500 100 150 30 3 10 0  --> increasing turns
# 50 500 250 100 75 3 99 0  -- fized turns

import sys
import time
import curses
import traceback
import evolution
from ant import Ant
from danger import Danger
from environment import Environment


if __name__ == "__main__":
    
    if len(sys.argv) != 9:
        print
        print 'Usage: python main.py \
        <environment size> \
        <food amount> \
        <colony size> \
        <ants energy higher than zero> \
        <number of dangers> \
        <dangers base power> \
        <selected ratio> \
        <turns>'
        # TODO mancano parametri, tipo numero di figli, numero selezionati 
        print 

    else:
        env_size = int(sys.argv[1])
        n_food = int(sys.argv[2])
        colony_size = int(sys.argv[3])
        ants_energy = int(sys.argv[4])
        n_danger = int(sys.argv[5])
        base_danger_power = int(sys.argv[6])
        selected_ratio = int(sys.argv[7])
        turns = int(sys.argv[8])

        '''
        other paramters to insert to test
        '''
        damage_per_turn = 3
        lucky_few = 2
        base_mutation = 40
        mutation_rate = 50
        mutation_cap = 30   
        danger_spawn = 50  
        danger_mode = 0
        danger_ratio = 5
        danger_increase_rate =  100
        max_danger_power = 10
        graphic_display = 10
        food_value = 10

        # build environment 
        env = Environment(env_size, n_food)
        # create danger
        dangers = []
        for i in range(n_danger):
            dangers.append(Danger(env, mode = danger_mode))
        # create ants
        colony = []
        for i in range(colony_size):
            colony.append(Ant(env, energy = ants_energy, 
                                food_value = food_value))
        danger_count = n_danger

        gen = 0
        data = open('data.txt', 'w')
        data_best = open('data_best.txt', 'w')
        data_all = open('data_all.txt', 'w')
        data_foods = open('data_foods.txt', 'w')
        data_dangers = open('data_dangers.txt', 'w')

        while True:
            try:
                for i in range(turns + min(gen/100, 0)):

                    if gen > graphic_display:
                        win = curses.initscr()
                        win.clear()
                        win.addstr(env.to_string(gen))
                        win.addstr('Turno : ' + str(i))
                        win.addstr('\n')
                        win.addstr('Generation : ' + str(gen))
                        win.refresh()
                        time.sleep(0.1)

                    for ant in colony:
                        action = ant.pick_action(env)      
                        ant.move_or_act(env, action, dangers)
                        ant.get_damage(env, colony, -1*damage_per_turn)
                        ant.get_neighbours(env)
                    
                    if gen > graphic_display:
                        win = curses.initscr()
                        win.clear()
                        win.addstr(env.to_string(gen))
                        win.addstr('Turno : ' + str(i))
                        win.addstr('\n')
                        win.addstr('Generation : ' + str(gen))
                        win.refresh()
                        time.sleep(0.1)
                    
                    for danger in dangers:                    
                        if not danger.get_damage(env, dangers, colony):

                            if not danger.attack_ant(env, colony):
                                danger.move_random(env)

                            danger.reset_attacking_ants()
                        else:
                            danger_count -= 1
                    colony = [ant for ant in colony if ant is not None]

                
                score_to_save = str(env.get_food())
                score_to_save += '\n'
                data_foods.write(score_to_save)
                score_to_save = str(danger_count)
                score_to_save += '\n'
                data_dangers.write(score_to_save)

                env = Environment(env_size, n_food)
                # print('COLONY SIZE:')
                # print(colony_size)
                # print('SURVIVED ANTS:')
                # print(len(colony))
                selected = evolution.select_from_population(colony, colony_size, 
                                                            (len(colony)/selected_ratio),
                                                            lucky_few, env, 
                                                            data, data_best, data_all)
                # print ('SELECTED:')
                # print (len(selected))
                colony = evolution.create_children(selected, env, 
                                                    colony_size - len(selected), 
                                                    ants_energy, food_value)
                # print ('CHILDREN:')
                # print (len(colony))
                mutation_probability = base_mutation - \
                                        min(gen/mutation_rate, mutation_cap)
                colony = evolution.mutate_colony(colony, env, mutation_probability, 
                                                    ants_energy, food_value)

                for ant in selected:
                    ant[0].reset(ants_energy, env)
                    colony.append(ant[0])
                dangers = []
                if gen >= danger_spawn and n_danger == 0:
                    n_danger += len(colony)/danger_ratio
                for i in range(n_danger):
                    # danger now have a bound on maximum possible power that scales with generations
                    min_dangers_power = max((gen - danger_spawn)/danger_increase_rate, 
                                            base_danger_power)
                    dangers.append(Danger(env, base_power = min(max_danger_power, 
                                                                min_dangers_power),  
                                                                mode = danger_mode))
                danger_count = n_danger

                gen += 1
                print('generation :')
                print(gen)

            except Exception as e:
                traceback.print_exc()
                break