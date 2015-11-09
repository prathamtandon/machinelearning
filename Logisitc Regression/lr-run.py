#!/usr/bin/python

from learner import learn_logistic_regression
from test_lr import test_logistic_regression

def main():
        w = learn_logistic_regression()
        test_logistic_regression(w)

if __name__ == '__main__':
        main()
