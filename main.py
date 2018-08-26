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
    env_size = 30
    env = Environment(env_size)
    # create danger
    n_danger = 10
    dangers = []
    for i in range(n_danger):
        dangers.append(Danger(env))
    # create ants
    colony_size = 30
    colony = []
    for i in range(colony_size):
        colony.append(Ant(env))
    gen = 0
    while True:
        try:
            for i in range(20):
                win = curses.initscr()
                win.clear()
                win.addstr(env.to_string(gen))
                win.addstr('Turno : ' + str(i))
                win.refresh()
                time.sleep(0.5)
                for ant in colony:
                    action = ant.pick_action(env)      
                    ant.move_or_act(env, action, dangers)
                for danger in dangers:
                    if not danger.attack_ant(env, colony):
                        danger.move_random(env)
                        danger.get_surrounding_ants(env)
                colony = [ant for ant in colony if ant is not None]
            env = Environment(env_size)
            selected = evolution.select_from_population(colony, (len(colony)/2) - 1, 1)
            print 'SELECTED:'
            print selected
            children = evolution.create_children(selected, env, colony_size - (len(colony)/2))
            print 'CHILDREN:'
            print children
            new_colony = evolution.mutate_colony(children, env, 20)
            for ant in selected:
                ant[0].reset(env)
            selected += new_colony
            dangers = []
            for i in range(n_danger):
                dangers.append(Danger(env))
            gen += 1
            print 'NEW COLONY'
            print colony
            print '***************************'
        except Exception as e:
            traceback.print_exc()
            break