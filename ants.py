import tensorflow as tf

def init_weights(shape):
    init_random_dist = tf.truncated_normal(shape, stddev=1.0)
    return tf.Variable(init_random_dist)

def ant(genetic_inh=None):
    
     def __init__(self):
        if genetic_inh:
            self.synapses = genetic_inh
        else:
            self.synapses = init_weights([3,15])
            
#
#    def look_arond(""grid""):
#        .
#        .
#        return(input)

    def pick_action():
#       input = look_arond
        move = tf.matmul(input, my_weights[0])[0]
        eat = tf.matmul(input, my_weights[1])[0]
        attack = tf.matmul(input, my_weights[2])[0]
        action = tf.argmax([move, eat, attack])        
        return action
    
    def pass_genes():