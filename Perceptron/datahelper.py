from file_processor import FileProcessor
from random import sample
from constants import training_size, testing_size

class PartitionResult:
    def __init__(self):
        self.training = []
        self.testing = []

def get_difference(d1, d2):
    if len(d1) < len(d2):
        return get_difference(d2,d1)
    return list(set(d1) - set(d2))

def file_read (filename):
    fp = FileProcessor (filename, ' ')
    return fp.get_lines_as_array ()


def partition_data (dataset):
    training_pool = [i for i in range(0,len(dataset))]
    training_pos = sample(training_pool, training_size)
    
    testing_pool = get_difference(training_pool, training_pos)
    testing_pos = sample(testing_pool, testing_size)
    
    return_val = PartitionResult ()
    
    for i in training_pos:
        return_val.training.append(dataset[i])
    
    for i in testing_pos:
        return_val.testing.append(dataset[i])
    
    return return_val
    
    
    
    
    
        
