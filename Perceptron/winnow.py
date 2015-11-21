from constants import num_rounds, winnow_threshold

def get_label (x, w):
    sum_val = -winnow_threshold
    for xi in x:
        pos = xi.split(':')[0]
        pos = int(pos)
        sum_val += w[pos]
    
    if sum_val >= 0:
        return 1
    else:
        return -1

def update_weight_vector (w, eta, y, x):
    for xi in x:
        pos = xi.split(':')[0]
        pos = int(pos)
        w[pos] *= pow(eta,y)
    
    return w

def learn_perceptron (dimensions, training, gamma, eta):
    w = [1] * dimensions
    t = 0
    
    for t in range(1, num_rounds + 1):
        for row in training:
            predicted_label = get_label (row[1:], w)
            if predicted_label <= gamma:
                w = update_weight_vector (w, eta, predicted_label, row[1:])
                
    return w

def train_winnow (testing, w, gamma, eta):
    accurate = 0
    
    for row in testing:
        actual = 1 if row[0] == '+1' else -1
        predicted_label = get_label (row[1:], w)
        if predicted_label == actual:
            accurate += 1
    
    return accurate
        
    

