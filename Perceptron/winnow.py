from constants import num_rounds
from constants import winnow_params_with_margin
from constants import winnow_params_without_margin
from constants import count_mistakes_dimensions

class WinnowParams:
    def __init__(self):
        self.gamma = 0
        self.eta = 0
        self.weight_vector = []

class WinnowResult:
    def __init__ (self):
        self.params_without_margin = WinnowParams()
        self.params_with_margin = WinnowParams()
    
    def get_params (self, index):
        if index == 0:
            return self.params_without_margin
        else:
            return self.params_with_margin

def get_params_helper (dimensions, training_set, testing_set, gamma_range, eta_range):    
    cur_best = WinnowParams ()
    cur_best_mistakes = float('inf')
    
    for gamma in gamma_range:
        for eta in eta_range:
            print 'gamma: ' + str(gamma) + ' eta: ' + str(eta)
            result = winnow_train (dimensions, training_set, gamma, eta)
            weights = result
            mistakes_so_far = winnow_test (testing_set, weights)
            if mistakes_so_far[len(mistakes_so_far)-1] < cur_best_mistakes:
                print 'UPDATING CUR BEST'
                cur_best_mistakes = mistakes_so_far[len(mistakes_so_far)-1]
                cur_best.gamma = gamma
                cur_best.eta = eta
                cur_best.weight_vector = list (weights)
    
    return cur_best
    
    

def winnow_get_params (n_val, D1, D2):
    dimensions = count_mistakes_dimensions[n_val]
    
    print 'Running winnow without margin...'
    gamma_range = winnow_params_without_margin[0]
    eta_range = winnow_params_without_margin[1]
    params_without_margin = get_params_helper (dimensions, D1, D2, gamma_range, eta_range)
    
    print '\nbest gamma: ' + str(params_without_margin.gamma)
    print 'best eta: ' + str(params_without_margin.eta)
    
    print '\n\nRunning winnow with margin...'
    gamma_range = winnow_params_with_margin[0]
    eta_range = winnow_params_with_margin[1]
    params_with_margin = get_params_helper (dimensions, D1, D2, gamma_range, eta_range)
    
    print 'best gamma: ' + str(params_with_margin.gamma)
    print 'best eta: ' + str(params_with_margin.eta)
    
    return_val = WinnowResult ()
    return_val.params_without_margin = params_without_margin
    return_val.params_with_margin = params_with_margin
    
    return return_val


def get_label (x, w, threshold):
    sum_val = -threshold
    for xi in x:
        pos = xi.split(':')[0]
        pos = int(pos)
        sum_val += w[pos]
    
    return sum_val

def update_weight_vector (w, eta, y, x):
    for xi in x:
        pos = xi.split(':')[0]
        pos = int(pos)
        w[pos] *= pow(eta,y)
    
    return w

def winnow_train (dimensions, training, gamma, eta):
    w = [1.0] * (dimensions + 1)
    t = 0
    threshold = dimensions / 2
    
    for t in range(1, num_rounds + 1):
        for row in training:
            actual_label = 1 if row[0] == '+1' else -1
            hypothesis_result = get_label (row[1:], w, threshold)
            if hypothesis_result * actual_label <= gamma:
                w = update_weight_vector (w, eta, actual_label, row[1:])
    return w

def winnow_test (testing, w):
    accurate = 0
    threshold = len(w) / 2
    instance_count = 0
    mistakes = [0]
    
    for row in testing:
        actual_label = 1 if row[0] == '+1' else -1
        hypothesis_result = get_label (row[1:], w, threshold)
        predicted_label = 1 if hypothesis_result >= 0 else -1
        if actual_label == predicted_label:
            accurate += 1
        instance_count += 1
        if instance_count % 100 == 0:
            mistakes.append (instance_count - accurate)
            
    return mistakes
        
def winnow_mistake_count (dataset, winnow_params):
    w = winnow_params.weight_vector
    gamma = winnow_params.gamma
    
    return winnow_test (dataset, w)

