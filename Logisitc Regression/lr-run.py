#!/usr/bin/python

# Usage:
# command line: ./lr-run.py
# generates 'predictions.lr' inside output folder
# To generate confusion matrix:
# /output>perl evaluate.pl labels.txt predictions.lr

from learner import learn_logistic_regression
from test_lr import test_logistic_regression

def main():
        w = learn_logistic_regression()
        test_logistic_regression(w)

if __name__ == '__main__':
        main()

