# -*- coding: utf-8 -*-

import time
import curses
import traceback
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
    colony_size = 10
    colony = []
    for i in range(colony_size):
        colony.append(Ant(env))

    while True:
        try:
            # win = curses.initscr()
            # win.clear()
            # win.addstr(env.to_string())
            # win.refresh
            time.sleep(1)
            for ant in colony:
                action = ant.pick_action(env)
                # if action == 0:
                #     print 'attack'
                # elif action == 2:
                #     print 'move'
                # elif action == 1:
                #     print 'eat'         
                ant.move_or_act(env, action, dangers)
            for danger in dangers:
                if not danger.attack_ant(env, colony):
                    danger.move_random(env)
                    danger.get_surrounding_ants(env)
        except Exception as e:
            traceback.print_exc()
            break