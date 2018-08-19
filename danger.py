import math
import random 

class Danger(object):

    def __init__(self, env):

        env_size = env.get_size()
        # position in env 
        x = randint(0, env_size-1)
        y = randint(0, env_size-1)
        self.position = [x, y]
        # power danger
        self.power = - randint(-1, -10)

    def get_position(self):
        return self.position

    def get_power(self):
        return self.power

    def move_random(self, env):

        axis = random.uniform(0, 3)
        way = random.uniform(0, 1)
        env_size = env.get_size()
        x = self.position[0]
        y = self.position[1]
        if axis > 3:
            # move on x-axis
            if (way > 0.5) and \
                (x < env_size-1) and \
                (x >= 0) and \
                (env.is_free(x+1, y)):
                # move up
                    self.position = [x+1, y]
            if (way <= 0.5) and \
                (x <= env_size-1) and \
                (x > 0) and \
                (env.is_free(x-1, y)):
                # move down
                    self.position = [x-1, y]
        if axis > 2:
            # move on y-axis
            if (way > 0.5) and \
                (y < env_size-1) and \
                (y >= 0) and \
                (env.is_free(x, y+1)):
                # move right
                    self.position = [x, y+1]
            if (way <= 0.5) and \
                (y <= env_size-1) and \
                (y > 0) and \
                (env.is_free(x, y-1)):
                # move left
                    self.position = [x, y-1]
        if axis > 1:
            # move on z-axis (diagonally)
            if (way > 1) and \
                (y < env_size-1) and \
                (x < env_size-1) and \
                (y >= 0) and \
                (x >= 0) and \
                (env.is_free(x+1, y+1)):
                # move north-est
                    self.position = [x+1, y+1]
            if (way > 0.75) and \
                (y <= env_size-1) and \
                (x < env_size-1) and \
                (y > 0) and \
                (x >= 0) and \
                (env.is_free(x+1, y-1)):
                # move south-est 
                    self.position = [x+1, y-1]
            if (way > 0.50) and \
                (y <= env_size-1) and \
                (x <= env_size-1) and \
                (y > 0) and \
                (x > 0) and \
                (env.is_free(x-1, y-1)):
                # move south-west
                    self.position = [x-1, y-1]
            if (way > 0.25) and \
                (y <= env_size-1) and \
                (x < env_size-1) and \
                (y > 0) and \
                (x >= 0) and \
                (env.is_free(x-1, y+1)):
                # move north-west
                    self.position = [x-1, y+1]

    def damage_ant(self, ant):
        ant.get_damage(self.power*(-10))

    def attack_ant(self, env, colony):
        for i in range(3):
            for j in range(3):
                x = self.position[0]-1+i
                y = self.position[1]-1+j
                if (x!= 1) and ( y != 1) and (env.is_ant(x, y)):
                    for ant in colony:
                        if ant.position[0] == [x, y]:
                            self.damage_ant(ant)

    def get_damage(self, n_ant):
        if (self.power / 2) <= n_ant:
            return True
            del self
        else:
            return False
            
    

    
