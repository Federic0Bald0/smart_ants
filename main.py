# -*- coding: utf-8 -*-

import time
import curses
import traceback
import evolution
from ant import Ant
from danger import Danger
from environment import Environment


if __name__ == "__main__":

    # TODO get arguments form stdin 

    # build environment 
    env_size = 200
    env = Environment(env_size)
    # create danger
    n_danger = 30
    dangers = []
    for i in range(n_danger):
        dangers.append(Danger(env))
    # create ants
    colony_size = 200
    colony = []
    for i in range(colony_size):
        colony.append(Ant(env))
    gen = 0
    while True:
        try:
            for i in range(20):
                # win = curses.initscr()
                # win.clear()
                # win.addstr(env.to_string(gen))
                # win.addstr('Turno : ' + str(i))
                # win.refresh()
                time.sleep(0.001)

                for ant in colony:
                    action = ant.pick_action(env)      
                    ant.move_or_act(env, action, dangers)

                # win = curses.initscr()
                # win.clear()
                # win.addstr(env.to_string(gen))
                # win.addstr('Turno : ' + str(i))
                # win.refresh()
                # time.sleep(0.5)
                
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
            selected = evolution.select_from_population(colony, (len(colony)/2) - 1, 1)
            # print ('SELECTED:')
            # print (len(selected))
            colony = evolution.create_children(selected, env, colony_size - len(selected))
            # print ('CHILDREN:')
            # print (len(colony))
            colony = evolution.mutate_colony(colony, env, 20)
            for ant in selected:
                ant[0].reset(env)
                colony.append(ant[0])
            dangers = []
            for i in range(n_danger):
                # danger now have a bound on maximum possible power that scales with generations
                min_dangers_power = max(gen/50, 2)
                dangers.append(Danger(env, min(9, min_dangers_power)))
            gen += 1
            print('generation :')
            print(gen)
        except Exception as e:
            traceback.print_exc()
            break