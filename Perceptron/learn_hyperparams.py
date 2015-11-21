from perceptron import learn_perceptron, train_perceptron
from winnow import learn_winnow, train_winnow
from constants import count_mistakes_dimensions

class HyperparamResult:
    def __init__(self):
        self.gamma = 0
        self.eta = 0


def learn_hyperparams_perceptron (n_val, training, testing, margin_range, learning_rate_range):
    return_val = HyperparamResult()
    best = -float('inf')
    
    for gamma in margin_range:
        for eta in learning_rate_range:
            weight_vector = learn_peceptron (count_mistakes_dimensions[n_val],
                                    training, gamma, eta)
            accuracy = train_perceptron (testing, weight_vector, gamma, eta)
            if accuracy > best:
                best = accuracy
                return_val.gamma = gamma
                return_val.eta = eta
            
    return return_val

def learn_hyperparams_winnow (training, testing, margin_range, learning_rate_range):
    return_val = HyperparamResult()
    best = -float('inf')
    
    for gamma in margin_range:
        for eta in learning_rate_range:
            weight_vector = learn_peceptron (count_mistakes_dimensions[n_val],
                                    training, gamma, eta)
            accuracy = train_perceptron (testing, weight_vector, gamma, eta)
            if accuracy > best:
                best = accuracy
                return_val.gamma = gamma
                return_val.eta = eta
            
    return return_val
    
