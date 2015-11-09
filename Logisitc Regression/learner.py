from constants import training_data_filepath, convergence_threshold, learning_rate, max_iters
from FileProcessor import FileProcessor
from vocabulary import get_vocabulary_size, get_labels
from utils import sigmoid, get_norm, get_l1_norm
from random import shuffle

def get_prediction(feature_vector, w):
        sum_val = w[0]
        for feature in feature_vector:
                feature_id = int(feature.split(':')[0])
                # strength of each feature is 1.0 so we skip multiplying it.
                sum_val += w[feature_id]
        return sigmoid(sum_val)

def update_weights(feature_vector, w, delta):
        w[0] = w[0] + delta
        for feature in feature_vector:
                feature_id =  feature.split(':')[0]
                w[int(feature_id)] += learning_rate * delta
                
def learn_lr_classifier(training_corpus):
        D = get_vocabulary_size()
        labels = get_labels()
        w = [0] * (D + 1)
        norm = 1.0
        num_iters = 0
        while norm > convergence_threshold:
                num_iters += 1
                if num_iters > max_iters:
                        break
                old_w = list(w)
                shuffled = list(training_corpus)
                shuffle(shuffled)
                for vector in shuffled:
                        label = 1.0 if float(vector[0]) == labels[0] else 0.0
                        prediction = get_prediction(vector[1:], w)
                        delta = label - prediction
                        update_weights(vector[1:], w, delta)
                norm = get_norm(w,old_w)
        return w

def learn_logistic_regression():
        fp = FileProcessor(training_data_filepath, ' ')
        training_corpus = fp.parse_input_file()
        return learn_lr_classifier(training_corpus)
