#!/usr/bin/python
from datahelper import file_read, partition_data
from count_mistakes2 import perceptron_generate_best_hyperparams, winnow_generate_best_hyperparams
from count_mistakes2 import perceptron_hypothesis_result, winnow_hypothesis_result
from count_mistakes2 import perceptron_update_weights, perceptron_update_bias, winnow_update_weights
from constants import num_rounds
import matplotlib.pyplot as plt


n_vals = [40, 80, 120, 160, 200]
halting_instances = 700
learning_curves_files = {
    40: 'dataset-40.libsvm',
    80: 'dataset-80.libsvm',
    120: 'dataset-120.libsvm',
    160: 'dataset-160.libsvm',
    200: 'dataset-200.libsvm'
}

def does_winnow_converge (dataset, dimensions, margin, learning_rate, mistakes, index):
    weight_vector = [1.0] * (dimensions + 1)
    threshold = dimensions / 2.0
    cur_round = 0
    
    while cur_round < num_rounds:
        print 'cur round: ' + str(cur_round + 1)
        instances_survived = 0
        mistakes_made = 0
        for data_row in dataset:
            outcome = 1 if data_row[0] == '+1' else -1
            prediction = winnow_hypothesis_result (data_row[1:], weight_vector, threshold)
            if outcome * prediction > margin:
                instances_survived += 1
                if instances_survived >= halting_instances:
                    mistakes[index] = mistakes_made
                    return True
            else:
                weight_vector = winnow_update_weights (data_row[1:], outcome, weight_vector, learning_rate)
                mistakes_made += 1
                instances_survived = 0
                
        print 'total mistakes at end of round: ' + str(mistakes_made)
        cur_round += 1

    return False

def does_perceptron_converge (dataset, dimensions, margin, learning_rate, mistakes, index):
    weight_vector = [0.0] * (dimensions + 1)
    bias = 0.0
    cur_round = 0
    
    while cur_round < num_rounds:
        print 'cur round: ' + str(cur_round + 1)
        instances_survived = 0
        mistakes_made = 0
        for data_row in dataset:
            outcome = 1 if data_row[0] == '+1' else -1
            prediction = perceptron_hypothesis_result (data_row[1:], weight_vector, bias)
            if outcome * prediction > margin:
                instances_survived += 1
                if instances_survived >= halting_instances:
                    mistakes[index] = mistakes_made
                    return True
            else:
                weight_vector = perceptron_update_weights (data_row[1:], outcome, weight_vector, learning_rate)
                bias = perceptron_update_bias (bias, outcome, learning_rate)
                mistakes_made += 1
                instances_survived = 0
        
        print 'total mistakes at end of round: ' + str(mistakes_made)
        cur_round += 1
    
    return False

def plot_mistakes_versus_n ():
    winnow_with_margin_mistakes = [435, 253, 489, 516, 472]
    winnow_mistakes = [169, 349, 376, 466, 472]
    perceptron_with_margin_mistakes = [188, 677, 377, 194, 462]
    perceptron_mistakes = [456, 530, 377, 194, 577]
    plt.plot(n_vals, winnow_mistakes, 'g-.', label='winnow without margin')
    plt.plot(n_vals, winnow_with_margin_mistakes, 'y:', label='winnow with margin')
    plt.plot(n_vals, perceptron_mistakes, 'r-', label='perceptron without margin')
    plt.plot(n_vals, perceptron_with_margin_mistakes, 'b--', label='perceptron with margin')
    plt.xlabel('n')
    plt.ylabel('mistakes') 
    plt.legend(loc='upper right')
    plt.savefig('mistakes-versus-n.pdf')

def main ():
    mistakes_at_halting = [0] * len(n_vals)
    index = 0
    is_success = True
    '''
    for n_val in n_vals:
        print '\nn = ' + str(n_val)
        libsvm_filename = learning_curves_files[n_val]  
        ##################### Generate D1,D2 from libsvm #############################
        dataset = file_read (libsvm_filename)
        partition = partition_data (dataset)
        training_set = partition.training
        testing_set = partition.testing
        
        ######## Learn best performing hyperparams for current algorithm #############
        best_hyperparams = winnow_generate_best_hyperparams (n_val, training_set, testing_set, True)
        
        ######## Count cumulative mistakes for current n_val, and some value of S ####
        print '\nmeasuring convergence with S = ' + str(halting_instances)
        if does_winnow_converge (dataset, n_val, best_hyperparams.gamma, best_hyperparams.eta, mistakes_at_halting, index):
            print 'winnow converges for given S, mistakes made at halt: ' + str(mistakes_at_halting[index])
            index += 1
        else:
            is_success = False
            print 'winnow does not survive given S, try with a new S'
            break
    '''
    if is_success is True:
        plot_mistakes_versus_n ()
    

if __name__ == '__main__':
    main ()
