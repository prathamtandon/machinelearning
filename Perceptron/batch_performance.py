#!/usr/bin/python
from constants import batch_performance_datasets, batch_performance_n
from datahelper import file_read, partition_data
from perceptron import perceptron_get_params, perceptron_train, perceptron_test
from winnow import winnow_get_params, winnow_train, winnow_test

def perceptron_learn_batch_performance_params (testing, training):
    return perceptron_get_params (batch_performance_n, testing, training)
    
def winnow_learn_batch_performance_params (testing, training):
    return winnow_get_params (batch_performance_n, testing, training)
    

def learn_batch_performance_params (m_val):
    testing_file = batch_performance_datasets[m_val][0]
    training_file = batch_performance_datasets[m_val][1]
    
    testing_set = file_read (testing_file)
    training_set = file_read (training_file)
    
    partition = partition_data (testing_set)
    D1 = partition.training
    D2 = partition.testing
    
    perceptron_params = perceptron_learn_batch_performance_params (D1, D2)
    perceptron_params_without_margin = perceptron_params.get_params (0)
    perceptron_params_with_margin = perceptron_params.get_params (1)
    print 'perceptron without margin acc(D2): ' + str(perceptron_params_without_margin.accuracy)
    print 'perceptron with margin acc(D2): ' + str(perceptron_params_with_margin.accuracy)
    
    print '\n\nRunning perceptron on Test set...'
    
    perceptron_trained_without_margin = perceptron_train (batch_performance_n, training_set, perceptron_params_without_margin.gamma, perceptron_params_without_margin.eta)
    perceptron_trained_with_margin = perceptron_train (batch_performance_n, training_set, perceptron_params_with_margin.gamma, perceptron_params_with_margin.eta)
    perceptron_mistakes_without_margin = perceptron_test (testing_set, perceptron_trained_without_margin[0], perceptron_trained_without_margin[1])
    perceptron_mistakes_with_margin = perceptron_test (testing_set, perceptron_trained_with_margin[0], perceptron_trained_with_margin[1])
    print 'perecptron without margin acc(Test): ' + str(1.0 - float(perceptron_mistakes_without_margin[len(perceptron_mistakes_without_margin)-1]) / len (testing_set))
    print 'perecptron with margin acc(Test): ' + str(1.0 - float(perceptron_mistakes_with_margin[len(perceptron_mistakes_with_margin)-1]) / len (testing_set))
    
    winnow_params = winnow_learn_batch_performance_params (D1, D2)
    winnow_params_without_margin = winnow_params.get_params (0)
    winnow_params_with_margin = winnow_params.get_params (1)
    print 'winnow without margin acc(D2): ' + str(winnow_params_without_margin.accuracy)
    print 'winnow with margin acc(D2): ' + str(winnow_params_with_margin.accuracy)
    
    print '\n\nRunning winnow on Test set...'
    
    winnow_trained_without_margin = winnow_train (batch_performance_n, training_set, winnow_params_without_margin.gamma, winnow_params_with_margin.eta)
    winnow_trained_with_margin = winnow_train (batch_performance_n, training_set, winnow_params_with_margin.gamma, winnow_params_with_margin.eta)
    winnow_mistakes_without_margin = winnow_test (testing_set, winnow_trained_without_margin)
    winnow_mistakes_with_margin = winnow_test (testing_set, winnow_trained_with_margin)
    print 'winnow without margin acc(Test): ' + str(1.0 - float(winnow_mistakes_without_margin[len(winnow_mistakes_without_margin)-1]) / len(testing_set))
    print 'winnow with margin acc(Test): ' + str(1.0 - float(winnow_mistakes_with_margin[len(winnow_mistakes_with_margin)-1]) / len(testing_set))
    
    
    
    
def main ():
    print 'Running with m = 1000'
    learn_batch_performance_params (2)

if __name__ == '__main__':
    main ()
