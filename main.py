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
    
    if len(sys.argv) != 9:
        print
        print 'Usage: python main.py \
        <size_environment> \
        <amount_food> \
        <size_colony> \
        <power_ants higher than zero> \
        <number_dangers> \
        <power_dangers maximum power> \
        <turns> \
        <mode>'
        # TODO mancano parametri, tipo numero di figli, numero selezionati 
        print 
    else:
        env_size = int(sys.argv[1])
        n_food = int(sys.argv[2])
        colony_size = int(sys.argv[3])
        ants_power = int(sys.argv[4])
        n_danger = int(sys.argv[5])
        danger_power = int(sys.argv[6])
        turns = int(sys.argv[7])
        mode = int(sys.argv[8])
        # build environment 
        env = Environment(env_size)
        # create danger
        dangers = []
        for i in range(n_danger):
            dangers.append(Danger(env))
        # create ants
        colony = []
        for i in range(colony_size):
            colony.append(Ant(env, mode))
        gen = 0
        while True:
            try:
                for i in range(turns):

                    # if gen > 0:
                        # win = curses.initscr()
                        # win.clear()
                        # win.addstr(env.to_string(gen))
                        # win.addstr('Turno : ' + str(i))
                        # win.addstr('\n')
                        # win.addstr('Generation : ' + str(gen))
                        # win.refresh()
                        # time.sleep(0.1)

                    for ant in colony:
                        action = ant.pick_action(env)      
                        ant.move_or_act(env, action, dangers)
                        ant.get_damage(env, colony, 1)
                    
                    # if gen > 0:
                        # win = curses.initscr()
                        # win.clear()
                        # win.addstr(env.to_string(gen))
                        # win.addstr('Turno : ' + str(i))
                        # win.addstr('\n')
                        # win.addstr('Generation : ' + str(gen))
                        # win.refresh()
                        # time.sleep(0.1)
                    
                    for danger in dangers:                    
                        if not danger.get_damage(env, dangers):

                            if not danger.attack_ant(env, colony):
                                danger.move_random(env)

                            danger.reset_attacking_ants()
                    colony = [ant for ant in colony if ant is not None]

                
                env = Environment(env_size)
                # print('COLONY SIZE:')
                # print(colony_size)
                # print('SURVIVED ANTS:')
                # print(len(colony))
                selected = evolution.select_from_population(colony, (len(colony)/3), 2)
                # print ('SELECTED:')
                # print (len(selected))
                colony = evolution.create_children(selected, env, colony_size - len(selected), mode)
                # print ('CHILDREN:')
                # print (len(colony))
                colony = evolution.mutate_colony(colony, env, 20, mode)
                for ant in selected:
                    ant[0].reset(env, mode)
                    colony.append(ant[0])
                dangers = []
                for i in range(n_danger):
                    # danger now have a bound on maximum possible power that scales with generations
                    min_dangers_power = max(gen/5000, 2)
                    dangers.append(Danger(env, min(9, min_dangers_power)))
                gen += 1
                print('generation :')
                print(gen)
            except Exception as e:
                traceback.print_exc()
                break