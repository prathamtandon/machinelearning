#!/usr/bin/python
from constants import count_mistakes_datasets
from datahelper import file_read, partition_data
from perceptron import perceptron_get_params, perceptron_mistake_count
from winnow import winnow_get_params, winnow_mistake_count

def count_mistakes_perceptron (n_val, dataset, training, testing):
    perceptron_params = perceptron_get_params (n_val, training, testing)
    
    perceptron_params_without_margin = perceptron_params.get_params(0)
    perceptron_params_with_margin = perceptron_params.get_params(1)
    print '\nCounting Perceptron mistakes...'
    
    mistakes_without_margin = perceptron_mistake_count (dataset, 
                                perceptron_params_without_margin)
    mistakes_with_margin = perceptron_mistake_count (dataset, 
                                perceptron_params_with_margin)
                                
    print '\n\nMistakes without margin: ' + str(mistakes_without_margin)
    print 'Mistakes with margin: ' + str(mistakes_with_margin)

def count_mistakes_winnow (n_val, dataset, training, testing):
    winnow_params = winnow_get_params (n_val, training, testing)
    winnow_params_without_margin = winnow_params.get_params (0)
    winnow_params_with_margin = winnow_params.get_params (1)
    
    print '\nCounting Winnow mistakes...'
    
    mistakes_without_margin = winnow_mistake_count (dataset,
                                winnow_params_without_margin)
    mistakes_with_margin = winnow_mistake_count (dataset,
                                winnow_params_with_margin)
    
    print '\n\nMistakes without margin: ' + str(mistakes_without_margin)
    print 'Mistakes with margin: ' + str(mistakes_with_margin)
    

def count_mistakes(n_val):
    dataset = file_read (count_mistakes_datasets[n_val])
    partition = partition_data (dataset)
    count_mistakes_perceptron (n_val, dataset, partition.training, partition.testing)
    count_mistakes_winnow (n_val, dataset, partition.training, partition.testing)
                              
def main():
    # n = 500
    count_mistakes(0)
    # n = 1000
    # count_mistakes(1)

if __name__ == '__main__':
    main()


'''
Findings: 

winnow(with margin)
n = 500; gamma = 0.001, eta = 1.01
n = 1000; gamma = 0.001 eta = 1.1

winnow(without margin)
n = 500; gamma = 0, eta = 1.005
n = 1000; gamma = 0, eta = 1.1

perceptron(with margin)
n = 500; gamma = 1, eta = 0.25, mistakes = 1245
n = 1000; gamma = 1, eta = 0.25, mistakes = 1497

perceptron(without margin)
n = 500; gamma = 0, eta = 1, mistakes = 1871
n = 1000; gamma = 0, eta = 1, mistakes = 1560
'''
