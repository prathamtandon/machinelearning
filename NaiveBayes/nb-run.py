#!/usr/bin/python

# The Naive Bayer learner.

from constants import label_mappings
from vocabulary_builder import vocabulary
from process import get_corpus_size, get_corpus, get_words_count
from EmailLabel import EmailLabel
from test_nb import test_naive_bayes

learned = {}

def get_prior(label):
    return (float(get_corpus_size(label)) / get_corpus_size())

def get_class_conditioned_density(word_count, corpus_word_count):
    return (float(word_count + 1) / (corpus_word_count + len(vocabulary)))

def learn_naive_bayes():
    for label in label_mappings:
        label_instance = EmailLabel(label)
        label_instance.prior = get_prior(label)
        label_corpus = get_corpus(label)
        label_words_count = get_words_count(label)
        for word in vocabulary:
            word_count = 0
            if word in label_corpus:
                word_count = int(label_corpus[word])
            label_instance.densities[word] = get_class_conditioned_density(word_count, label_words_count)

        learned[label] = label_instance

def main():
    learn_naive_bayes()
    test_naive_bayes(learned)

if __name__ == '__main__':
    main()
