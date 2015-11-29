#!/usr/bin/python
from constants import count_mistakes_datasets
from datahelper import file_read, partition_data
from perceptron import perceptron_get_params, perceptron_mistake_count
from winnow import winnow_get_params, winnow_mistake_count
from plothelper import plot_mistakes

def count_mistakes_perceptron (n_val, dataset, training, testing):
    perceptron_params = perceptron_get_params (n_val, training, testing)
    
    perceptron_params_without_margin = perceptron_params.get_params(0)
    perceptron_params_with_margin = perceptron_params.get_params(1)
    
    mistakes_without_margin = perceptron_mistake_count (dataset, 
                                perceptron_params_without_margin)
    mistakes_with_margin = perceptron_mistake_count (dataset, 
                                perceptron_params_with_margin)
    
    return (mistakes_without_margin, mistakes_with_margin)

def count_mistakes_winnow (n_val, dataset, training, testing):
    winnow_params = winnow_get_params (n_val, training, testing)
    winnow_params_without_margin = winnow_params.get_params (0)
    winnow_params_with_margin = winnow_params.get_params (1)
    
    mistakes_without_margin = winnow_mistake_count (dataset,
                                winnow_params_without_margin)
    mistakes_with_margin = winnow_mistake_count (dataset,
                                winnow_params_with_margin)
    
    return (mistakes_without_margin, mistakes_with_margin)
    

def count_mistakes(n_val):
    dataset = file_read (count_mistakes_datasets[n_val])
    partition = partition_data (dataset)
    retVal1 = count_mistakes_perceptron (n_val, dataset, partition.training, partition.testing)
    retVal2 = count_mistakes_winnow (n_val, dataset, partition.training, partition.testing)
    plot_mistakes(retVal1[0],retVal2[1],retVal2[0],retVal2[1])
                              
def main():
    # n = 500
    # count_mistakes(0)
    # n = 1000
    count_mistakes(1)

if __name__ == '__main__':
    main()


'''
Findings: 

winnow(with margin)
n = 500; gamma = 2.0, eta = 1.1, mistakes(50,000) = 741, mistakes(5,000) = 88
n = 1000; gamma = 0.3, eta = 1.1, mistakes(50,000) = 928, mistakes(5,000) = 88

winnow(without margin)
n = 500; gamma = 0, eta = 1.1, mistakes(50,000) = 896, mistakes(5,000) = 97
n = 1000; gamma = 0, eta = 1.1, mistakes(50,000) = 1053, mistakes(5,000) = 94

perceptron(with margin)
n = 500; gamma = 1, eta = 0.001, mistakes(50,000) = 1030, mistakes(5,000) = 126
n = 1000; gamma = 1, eta = 0.005, mistakes(50,000) = 1387, mistakes(5,000) = 138

perceptron(without margin)
n = 500; gamma = 0, eta = 1, mistakes(50,000) = 1185, mistakes(5,000) = 135
n = 1000; gamma = 0, eta = 1, mistakes(50,000) = 1462, mistakes(5,000) = 146
'''
