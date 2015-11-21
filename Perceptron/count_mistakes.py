#!/usr/bin/python
from constants import count_mistakes_datasets, perceptron_without_margin, 
                    perceptron_with_margin, winnow_without_margin, 
                    winnow_with_margin
from datahelper import partition_data
from learn_hyperparams import learn_hyperparams_perceptron
from learn_hyperparams import learn_hyperparams_winnow

def count_mistakes(n_val):
    dataset = partition_data(count_mistakes_datasets[n_val])
    D1 = dataset.training
    D2 = dataset.testing 
    
    learn_hyperparams_perceptron(n_val,D1,D2,perceptron_without_margin[0], 
                                perceptron_without_margin[1])
    learn_hyperparams_perceptron(n_val,D1,D2,perceptron_with_margin[0], 
                                perceptron_with_margin[1])
    learn_hyperparams_winnow(n_val,D1,D2,winnow_without_margin[0],
                            winnow_without_margin[1])
    learn_hyperparams_winnow(n_val,D1,D2,winnow_with_margin[0],
                            winnow_with_margin[1])
    
def main():
    # n = 500
    count_mistakes(0)
    # n = 1000
    count_mistakes(1)

if __name__ == '__main__':
    main()
