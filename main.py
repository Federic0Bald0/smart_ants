from ants import Ant
from environment import Environment

if __name__ == "__main__":

    # TODO get arguments form stdin 

    # build environment 
    env_size = 10
    env = Environment(env_size)
    # create ants
    colony_size = 10
    colony = []
    for i in range(colony_size):
        colony.append(Ant(env))
    
    while True:

        # do things