from perceptron import perceptron_train, perceptron_test
from winnow import winnow_train, winnow_test
from constants import count_mistakes_dimensions

class HyperparamResult:
    def __init__(self):
        self.gamma = 0
        self.eta = 0
        self.weight_vector = []
        self.bias = 0


def learn_hyperparams_perceptron (n_val, training, testing, margin_range, learning_rate_range):
    return_val = HyperparamResult()
    best = -float('inf')
    
    for gamma in margin_range:
        for eta in learning_rate_range:
            accuracy = 0
            result = perceptron_train (count_mistakes_dimensions[n_val],
                                    training, gamma, eta)
            weight_vector = result[0]
            bias = result[1]
            accuracy = perceptron_test (testing, weight_vector, bias, gamma, eta)
            if accuracy > best:
                best = accuracy
                return_val.gamma = gamma
                return_val.eta = eta
                return_val.weight_vector = list(weight_vector)
                return_val.bias = bias
            
    return return_val

def learn_hyperparams_winnow (n_val, training, testing, margin_range, learning_rate_range):
    return_val = HyperparamResult()
    best = -float('inf')
    
    for gamma in margin_range:
        for eta in learning_rate_range:
            accuracy = 0
            weight_vector = winnow_train (count_mistakes_dimensions[n_val],
                                        training, gamma, eta)
            accuracy = winnow_test (testing, weight_vector, gamma)
            if accuracy > best:
                best = accuracy
                return_val.gamma = gamma
                return_val.eta = eta
                return_val.weight_vector = list(weight_vector)
    
    return return_val
    
