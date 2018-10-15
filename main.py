# -*- coding: utf-8 -*-

import sys
import time
import curses
import traceback
import evolution
from ant import Ant
from danger import Danger
from environment import Environment


if __name__ == "__main__":

    if len(sys.argv) != 12:
        print
        print 'Usage: python main.py \
        <environment size> \
        <food amount> \
        <colony size> \
        <ants energy higher than zero> \
        <number of dangers> \
        <dangers base power> \
        <selected ratio> \
        <mutation prob> \
        <danger appereance> \
        <turns> \
        <display> '
        print

    else:
        env_size = int(sys.argv[1])
        n_food = int(sys.argv[2])
        colony_size = int(sys.argv[3])
        ants_energy = int(sys.argv[4])
        n_danger = int(sys.argv[5])
        base_danger_power = int(sys.argv[6])
        selected_ratio = int(sys.argv[7])
        mutation_prob = int(sys.argv[8])
        danger_appereance = int(sys.argv[9])
        turns = int(sys.argv[10])
        display = int(sys.argv[11])

        '''
        other paramters to insert to test
        '''
        damage_per_turn = 3
        lucky_few = 2
        base_mutation = mutation_prob # probability of mutation
        mutation_rate = 50
        mutation_cap = 0 # to avoid change of probability through the turns
        danger_appereance = danger_appereance
        danger_mode = 0
        danger_ratio = int(sys.argv[5]) # ration between ants and danger
        danger_increase_rate =  100 # ???
        max_danger_power = base_danger_power
        graphic_display = 0
        food_value = 10

        # build environment
        env = Environment(env_size, n_food)
        # create danger
        dangers = []
        for i in range(n_danger):
            dangers.append(Danger(env, mode = danger_mode))
        danger_count = n_danger
        # create ants
        colony = []
        for i in range(colony_size):
            colony.append(Ant(env, energy = ants_energy,
                                food_value = food_value))
        gen = 0
        while True:
            try:
                for i in range(turns):

                    if display == 1:
                        # display the environment
                        win = curses.initscr()
                        win.clear()
                        win.addstr(env.to_string(gen))
                        win.addstr('Turno : ' + str(i))
                        win.addstr('\n')
                        win.addstr('Generation : ' + str(gen))
                        win.refresh()
                        time.sleep(0.1)

                    for ant in colony:
                        # ants behaving
                        action = ant.pick_action(env)
                        ant.move_or_act(env, action, dangers)
                        ant.get_damage(env, colony, -1*damage_per_turn)
                        ant.get_neighbours(env)

                    for danger in dangers:
                        # dangers behaving
                        if not danger.get_damage(env, dangers, colony):
                            if not danger.attack_ant(env, colony):
                                danger.move_random(env)
                            danger.reset_attacking_ants()
                        else:
                            # if danger is dead
                            danger_count -= 1
                    colony = [ant for ant in colony if ant is not None]
                survivor = len(colony)
                env = Environment(env_size, n_food) # reset environment
                # EVOLUTION
                selected, avg, best_ant = evolution.select_from_population(
                                                colony, colony_size,
                                                (len(colony)/selected_ratio),
                                                lucky_few, env)
                colony = evolution.create_children(selected, env,
                                                colony_size - len(selected),
                                                ants_energy, food_value)
                mutation_probability = base_mutation - \
                                        min(gen/mutation_rate, mutation_cap)
                colony = evolution.mutate_colony(colony, env, mutation_probability,
                                                ants_energy, food_value)
                for ant in selected:
                    ant[0].reset(ants_energy, env)
                    colony.append(ant[0])
                dangers = []
                # reset dangers
                if n_danger == 0:
                    n_danger += n
                for i in range(n_danger):
                    # danger now have a bound on maximum possible power that scales with generations
                    # dangers.append(Danger(env, base_power= min(max_danger_power,
                    #                                             min_dangers_power),
                    #                                             mode = danger_mode))
                    dangers.append(Danger(env, base_power=max_danger_power))
                danger_count = n_danger
                print gen, survivor, avg, best_ant
                if gen == 500:
                    break
                gen += 1
                # print('generation :')
                # print(gen)

            except Exception as e:
                traceback.print_exc()
                break
