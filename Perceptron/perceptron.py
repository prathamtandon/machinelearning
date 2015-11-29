from constants import num_rounds
from constants import perceptron_params_with_margin
from constants import perceptron_params_without_margin
from constants import count_mistakes_dimensions, learning_curves_dimensions
from constants import survival_count

class PerceptronParams:
    def __init__(self):
        self.gamma = 0
        self.eta = 0
        self.weight_vector = []
        self.bias = 0

class PerceptronResult:
    def __init__ (self):
        self.params_without_margin = PerceptronParams()
        self.params_with_margin = PerceptronParams()
    
    def get_params (self, index):
        if index == 0:
            return self.params_without_margin
        else:
            return self.params_with_margin

def get_params_helper (dimensions, training_set, testing_set, gamma_range, eta_range):    
    cur_best = PerceptronParams ()
    cur_best_mistakes = float('inf')
    
    for gamma in gamma_range:
        for eta in eta_range:
            print 'gamma: ' + str(gamma) + ' eta: ' + str(eta)
            result = perceptron_train (dimensions, training_set, gamma, eta)
            weights = result[0]
            bias = result[1]
            mistakes_so_far = perceptron_test (testing_set, weights, bias)
            if mistakes_so_far[len(mistakes_so_far)-1] < cur_best_mistakes:
                cur_best_mistakes = mistakes_so_far[len(mistakes_so_far)-1]
                cur_best.gamma = gamma
                cur_best.eta = eta
                cur_best.weight_vector = list (weights)
                cur_best.bias = bias
    
    return cur_best
    
def perceptron_mistakes_survive (dataset, params):
    gamma = params.gamma
    eta = params.eta
    dimensions = len(params.weight_vector)
    w = [0.0] * (dimensions + 1)
    b = 0.0
    mistakes = 0
    instances_seen_without_mistakes = 0
    best_survival_count_achieved = 0
    
    for row in dataset:
        actual_label = 1 if row[0] == '+1' else -1
        hypothesis_result = get_label (row[1:], w, b)
        if actual_label * hypothesis_result > gamma:
            instances_seen_without_mistakes += 1
            if instances_seen_without_mistakes >= survival_count:
                print 'survived with: ' + str(survival_count)
                return mistakes
        else:
            mistakes += 1
            best_survival_count_achieved = instances_seen_without_mistakes
            instances_seen_without_mistakes = 0
            w = update_weight_vector (w, eta, actual_label, row[1:])
            b = update_bias (b, eta, actual_label)
    
    print 'try with a new value of S: ' + str(best_survival_count_achieved)

def perceptron_get_params (dimensions, D1, D2):
    
    print 'Running perceptron without margin...'
    gamma_range = perceptron_params_without_margin[0]
    eta_range = perceptron_params_without_margin[1]
    params_without_margin = get_params_helper (dimensions, D1, D2, gamma_range, eta_range)
    
    print '\nbest gamma: ' + str(params_without_margin.gamma)
    print 'best eta: ' + str(params_without_margin.eta)
    
    '''
    print '\n\nRunning perceptron with margin...'
    gamma_range = perceptron_params_with_margin[0]
    eta_range = perceptron_params_with_margin[1]
    params_with_margin = get_params_helper (dimensions, D1, D2, gamma_range, eta_range)
    
    print 'best gamma: ' + str(params_with_margin.gamma)
    print 'best eta: ' + str(params_with_margin.eta)
    '''
    return_val = PerceptronResult ()
    return_val.params_without_margin = params_without_margin
    #return_val.params_with_margin = params_with_margin
    
    return return_val


def get_label (x, w, b):
    sum_val = b
    for xi in x:
        pos = xi.split(':')[0]
        pos = int(pos)
        sum_val += w[pos]
    
    return sum_val

def update_weight_vector (w, eta, y, x):
    delta = eta * y
    for xi in x:
        pos = xi.split(':')[0]
        pos = int(pos)
        w[pos] += delta 

    return w

def update_bias (b, eta, y):
    b += eta * y
    return b

def perceptron_train (dimensions, training, gamma, eta):
    t = 0
    w = [0.0] * (dimensions + 1)
    b = 0.0
    
    for t in range(num_rounds):
        for row in training:
            actual_label = 1 if row[0] == '+1' else -1
            hypothesis_result = get_label (row[1:], w, b)
            if hypothesis_result * actual_label <= gamma:
                w = update_weight_vector (w, eta, actual_label, row[1:])
                b = update_bias (b, eta, actual_label)
    
    return [w,b]

def perceptron_test (testing, w, b):
    accurate = 0
    mistakes = [0]
    
    for i in range(len(testing)):
        row = testing[i]
        actual_label = 1 if row[0] == '+1' else -1
        hypothesis_result = get_label (row[1:], w, b)
        predicted_label = 1 if hypothesis_result >= 0 else -1
        if actual_label == predicted_label:
            accurate += 1
        if (i + 1) % 100 == 0:
            mistakes.append ((i + 1) - accurate)

    return mistakes

def perceptron_mistake_count (dataset, perceptron_params):
    w = perceptron_params.weight_vector
    b = perceptron_params.bias
    
    return perceptron_test (dataset, w ,b)
    
    
        
    
