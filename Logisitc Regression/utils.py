from constants import overflow
from math import exp, sqrt

def sigmoid(x):
        if x > overflow:
                x = overflow
        elif x < -overflow:
                x = -overflow
        
        return 1.0/(1.0 + exp(-x))
        
def get_norm(vector1, vector2):
        sum_val = 0.0
        for i in range(len(vector1)):
                diff = vector1[i] - vector2[i]
                sum_val += (diff * diff)
        
        return sqrt(sum_val)

def get_l1_norm(vector):
        sum_val = 0.0
        for i in range(len(vector)):
                sum_val += abs(vector[i])
        
        return sum_val
