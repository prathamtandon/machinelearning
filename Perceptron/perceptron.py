from constants import num_rounds

def get_label (x, w, b):
    sum_val = b
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
        w[pos] += eta * y
    
    return w

def update_bias (b, eta, predicted_label):
    b += eta * predicted_label
    return b

def learn_perceptron (dimensions, training, gamma, eta):
    w = [0] * dimensions
    b = 0
    t = 0
    
    for t in range(1, num_rounds + 1):
        for row in training:
            predicted_label = get_label (row[1:], w, b)
            if predicted_label <= gamma:
                w = update_weight_vector (w, eta, predicted_label, row[1:])
                b = update_bias (b, eta, predicted_label)
                
    return w

def train_perceptron (testing, w, gamma, eta):
    accurate = 0
    b = 0
    
    for row in testing:
        actual = 1 if row[0] == '+1' else -1
        predicted_label = get_label (row[1:], w, b)
        if predicted_label == actual:
            accurate += 1
    
    return accurate
    
    
        
    
