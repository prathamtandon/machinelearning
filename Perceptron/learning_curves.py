#!/usr/bin/python
from constants import learning_curves_datasets, learning_curves_dimensions
from datahelper import file_read, partition_data
from perceptron import perceptron_get_params, perceptron_mistakes_survive
from winnow import winnow_get_params, winnow_mistakes_survive
from plothelper import plot_learning_curves

def learn_curves_perceptron (n_val, dataset, training, testing):
    dimensions = learning_curves_dimensions[n_val]
    perceptron_params = perceptron_get_params (dimensions, training, testing)
    
    perceptron_params_without_margin = perceptron_params.get_params(0)
    perceptron_params_with_margin = perceptron_params.get_params(1)
    
    mistakes_without_margin = perceptron_mistakes_survive (dataset, 
                                perceptron_params_without_margin)
    
    return mistakes_without_margin

def learn_curves_winnow (n_val, dataset, training, testing):
    dimensions = learning_curves_dimensions[n_val]
    winnow_params = winnow_get_params (dimensions, training, testing)
    
    winnow_params_without_margin = winnow_params.get_params (0)
    winnow_params_with_margin = winnow_params.get_params (1)
    
    mistakes_with_margin = winnow_mistakes_survive (dataset, 
                                winnow_params_with_margin)
    
    return mistakes_with_margin

def learn_curves (n_val):
    dataset = file_read (learning_curves_datasets[n_val])
    partition = partition_data (dataset)
    #return learn_curves_perceptron (n_val, dataset, partition.training, partition.testing)
    return learn_curves_winnow (n_val, dataset, partition.training, partition.testing)

def main ():
    plot_learning_curves([
        # n = 40
        learn_curves (0),
        # n = 80
        learn_curves (1),
        # n = 120
        learn_curves (2),
        # n = 160
        learn_curves (3),
        # n = 200
        learn_curves (4)
        ],
        learning_curves_dimensions,
        'winnow_with_margin_lc',
        'winnow with margin'
    )

if __name__ == '__main__':
    main ()
