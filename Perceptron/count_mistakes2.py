#!/usr/bin/python
import matplotlib.pyplot as plt
from datahelper import file_read, partition_data

n_val = 1000
perceptron_parameters = [[[0],[1]],[[1],[1.5,0.25,0.03,0.005,0.001]]]
winnow_parameters = [[[0],[1.1,1.01,1.005,1.0005,1.0001]], [[2.0,0.3,0.04,0.006,0.001], [1.1,1.01,1.005,1.0005,1.0001]]]
count_mistakes_files = {
    500: 'dataset-500.libsvm',
    1000: 'dataset-1000.libsvm'
}
num_rounds = 20
instance_intervals = [i * 100 for i in range(1, 501)]

class PerceptronParams:
    def __init__ (self):
        self.weight_vector = []
        self.bias = 0.0
        self.gamma = 0.0
        self.eta = 0.0
        self.mistakes = 0
        self.accuracy = 0.0

class WinnowParams:
    def __init__(self):
        self.weight_vector = []
        self.gamma = 0.0
        self.eta = 0.0
        self.mistakes = 0
        self.accuracy = 0.0

def active_to_index (active):
    return int(active.split(':')[0])

def perceptron_hypothesis_result (instance_vector, weight_vector, bias):
    cur_sum = bias
    for active in instance_vector:
        index = active_to_index (active)
        cur_sum += weight_vector[index]
    
    return cur_sum

def perceptron_update_weights (instance_vector, actual, weight_vector, learning_rate):
    for active in instance_vector:
        index = active_to_index (active)
        weight_vector[index] += actual * learning_rate
    
    return weight_vector

def winnow_hypothesis_result (instance_vector, weight_vector, threshold):
    cur_sum = -threshold
    for active in instance_vector:
        index = active_to_index (active)
        cur_sum += weight_vector[index]
    
    return cur_sum

def perceptron_update_bias (bias, actual, learning_rate):
    return bias + actual * learning_rate

def winnow_update_weights (instance_vector, actual, weight_vector, learning_rate):
    for active in instance_vector:
        index = active_to_index (active)
        weight_vector[index] *= pow (learning_rate, actual)

    return weight_vector

def winnow_train (dimensions, training_set, margin, learning_rate):
    weight_vector = [1.0] * (dimensions + 1)
    cur_round = 0
    threshold = dimensions / 2.0
    
    while cur_round < num_rounds:
        for instance in training_set:
            outcome = 1 if instance[0] == '+1' else -1
            prediction = winnow_hypothesis_result (instance[1:], weight_vector, threshold)
            if outcome * prediction <= margin:
                weight_vector = winnow_update_weights (instance[1:], outcome, weight_vector, learning_rate)
        cur_round += 1
    
    return weight_vector

def winnow_test (testing_set, weight_vector, instance_intervals):
    cumulative_mistakes = []
    mistakes_so_far = 0
    threshold = len (weight_vector) / 2.0
    
    for i in range(len(testing_set)):
        instance = testing_set[i]
        outcome = 1 if instance[0] == '+1' else -1
        prediction = winnow_hypothesis_result (instance[1:], weight_vector, threshold)
        prediction_class = 1 if prediction >= 0 else -1
        if outcome != prediction_class:
            mistakes_so_far += 1
        if (i + 1) in instance_intervals:
            cumulative_mistakes.append (mistakes_so_far)
        
    return cumulative_mistakes

def perceptron_train (dimensions, training_set, margin, learning_rate):
    weight_vector = [0.0] * (dimensions + 1)
    bias = 0.0
    cur_round = 0
    
    while cur_round < num_rounds:
        for instance in training_set:
            outcome = 1 if instance[0] == '+1' else -1
            prediction = perceptron_hypothesis_result (instance[1:], weight_vector, bias)
            if outcome * prediction <= margin:
                weight_vector = perceptron_update_weights (instance[1:], outcome, weight_vector, learning_rate)
                bias = perceptron_update_bias (bias, outcome, learning_rate)
        cur_round += 1
    
    return [weight_vector, bias]

def perceptron_test (testing_set, weight_vector, bias, instance_intervals):
    cumulative_mistakes = []
    mistakes_so_far = 0
    
    for i in range (len(testing_set)):
        instance = testing_set[i]
        outcome = 1 if instance[0] == '+1' else -1
        prediction = perceptron_hypothesis_result (instance[1:], weight_vector, bias)
        prediction_class = 1 if prediction >= 0 else -1
        if outcome != prediction_class:
            mistakes_so_far += 1
        if (i + 1) in instance_intervals:
            cumulative_mistakes.append (mistakes_so_far)
    
    return cumulative_mistakes

def perceptron_generate_best_hyperparams (dimensions, training_set, testing_set, is_with_margin):
    margin = 0 if is_with_margin is False else 1
    gamma_range = perceptron_parameters[margin][0]
    eta_range = perceptron_parameters[margin][1]
    
    cur_best_mistakes = float('inf')
    best_hyperparams = PerceptronParams ()
    
    for gamma in gamma_range:
        for eta in eta_range:
            print 'currently training model with => gamma: ' + str(gamma) + ' eta: ' + str(eta)
            training_result = perceptron_train (dimensions, training_set, gamma, eta)
            weight_vector = training_result[0]
            bias = training_result[1]
            print 'training complete...testing on D2'
            cumulative_mistakes = perceptron_test (testing_set, weight_vector, bias, [len(testing_set)])
            if cumulative_mistakes[0] >= cur_best_mistakes:
                print 'no improvement in accuracy, ignoring current gamma/eta settings...'
            else:
                print 'improved accuracy, updating current gamma/eta settings...'
                cur_best_mistakes = cumulative_mistakes[0]
                best_hyperparams.weight_vector = list(weight_vector)
                best_hyperparams.bias = bias
                best_hyperparams.gamma = gamma
                best_hyperparams.eta = eta
                best_hyperparams.mistakes = cur_best_mistakes
                best_hyperparams.accuracy = 1.0 - float(cur_best_mistakes) / len(testing_set)
    
    print '\ncompleted running current algorithm, following are the findings: '
    print 'best gamma: ' + str(best_hyperparams.gamma)
    print 'best eta: ' + str(best_hyperparams.eta)
    print 'mistakes made (D2): ' + str(best_hyperparams.mistakes)
    print 'accuracy (D2): ' + str(best_hyperparams.accuracy)
    
    return best_hyperparams

def winnow_generate_best_hyperparams (dimensions, training_set, testing_set, is_with_margin):
    margin = 0 if is_with_margin is False else 1
    gamma_range = winnow_parameters[margin][0]
    eta_range = winnow_parameters[margin][1]
    
    cur_best_mistakes = float('inf')
    best_hyperparams = WinnowParams ()
    
    for gamma in gamma_range:
        for eta in eta_range:
            print 'currently training model with => gamma: ' + str(gamma) + ' eta: ' + str(eta)
            weight_vector = winnow_train (dimensions, training_set, gamma, eta)
            print 'training complete...testing on D2'
            cumulative_mistakes = winnow_test (testing_set, weight_vector, [len(testing_set)])
            if cumulative_mistakes[0] >= cur_best_mistakes:
                print 'no improvement in accuracy, ignoring current gamma/eta settings...'
            else:
                print 'improved accuracy, updating current gamma/eta settings...'
                cur_best_mistakes = cumulative_mistakes[0]
                best_hyperparams.weight_vector = list(weight_vector)
                best_hyperparams.gamma = gamma
                best_hyperparams.eta = eta
                best_hyperparams.mistakes = cur_best_mistakes
                best_hyperparams.accuracy = 1.0 - float(cur_best_mistakes) / len(testing_set)
    
    print '\ncompleted running current algorithm, following are the findings: '
    print 'best gamma: ' + str(best_hyperparams.gamma)
    print 'best eta: ' + str(best_hyperparams.eta)
    print 'mistakes made (D2): ' + str(best_hyperparams.mistakes)
    print 'accuracy (D2): ' + str(best_hyperparams.accuracy)
    
    return best_hyperparams
            
def generate_best_hyperparams (dimensions, training_set, testing_set):
    hyperparams = [None] * 4
    
    print '\ncurrent algorithm: perceptron without margin'
    hyperparams[0] = perceptron_generate_best_hyperparams (dimensions, training_set, testing_set, False)
    print '\ncurrent algorithm: perceptron with margin'
    hyperparams[1] = perceptron_generate_best_hyperparams (dimensions, training_set, testing_set, True)
    print '\ncurrent algorithm: winnow without margin'
    hyperparams[2] = winnow_generate_best_hyperparams (dimensions, training_set, testing_set, False)
    print '\ncurrent algorithm: winnow with margin'
    hyperparams[3] = winnow_generate_best_hyperparams (dimensions, training_set, testing_set, True)
    
    return hyperparams

def plot_cumulative_mistakes_versus_instances (p_mistakes_no_margin, p_mistakes_margin, w_mistakes_no_margin, w_mistakes_margin):
    plt.plot(instance_intervals, p_mistakes_no_margin, 'r-', label='perceptron without margin')
    plt.plot(instance_intervals, p_mistakes_margin, 'b--', label='perceptron with margin')
    plt.plot(instance_intervals, w_mistakes_no_margin, 'g-.', label='winnow without margin')
    plt.plot(instance_intervals, w_mistakes_margin, 'y:', label='winnow with margin')
    plt.xlabel('number of instances')
    plt.ylabel('number of mistakes') 
    plt.legend(loc='upper left')
    plt.savefig('mistakes-versus-instances-'+ str(n_val) + '.pdf')

def main ():
    print 'n = ' + str(n_val)
    libsvm_filename = count_mistakes_files[n_val]
    ##################### Generate D1,D2 from libsvm #############################
    dataset = file_read (libsvm_filename)
    partition = partition_data (dataset)
    training_set = partition.training
    testing_set = partition.testing
    
    ######## Learn best performing hyperparameters for all four algorithms #######
    best_hyperparams = generate_best_hyperparams (n_val, training_set, testing_set)
    best_hyperparams_perc = best_hyperparams[0]
    best_hyperparams_perc_margin = best_hyperparams[1]
    best_hyperparams_winnow = best_hyperparams[2]
    best_hyperparams_winnow_margin = best_hyperparams[3]
    
    ######## Count cumulative mistakes for all four algorithms on 50K dataset ####
    print '\ncounting cumulative mistakes on N = 50,000 dataset...'
    print 'current algorithm: perceptron without margin'
    cumulative_mistakes_perc = perceptron_test (dataset, best_hyperparams_perc.weight_vector, best_hyperparams_perc.bias, instance_intervals)
    print 'current algorithm: perceptron with margin'
    cumulative_mistakes_perc_margin = perceptron_test (dataset, best_hyperparams_perc_margin.weight_vector, best_hyperparams_perc_margin.bias, instance_intervals)
    print 'current algorithm: winnow without margin'
    cumulative_mistakes_winnow = winnow_test (dataset, best_hyperparams_winnow.weight_vector, instance_intervals)
    print 'current algorithm: winnow with margin'
    cumulative_mistakes_winnow_margin = winnow_test (dataset, best_hyperparams_winnow_margin.weight_vector, instance_intervals)
    ################ Plot mistakes versus instances for current n value ##########
    plot_cumulative_mistakes_versus_instances (cumulative_mistakes_perc, cumulative_mistakes_perc_margin, cumulative_mistakes_winnow, cumulative_mistakes_winnow_margin)
    
    

if __name__ == '__main__':
    main ()
