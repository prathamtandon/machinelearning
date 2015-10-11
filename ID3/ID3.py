#!/usr/bin/python

import math
from collections import Counter

class Node:
    def __init__(self, key):
        # key is a label if node is leaf, an attribute otherwise
        self.key = key
        # Children are of the form <value,Node>
        self.children = []

def all_same(values):
    if len(values) == 0:
        return True
    first = values[0]
    for i in range(1, len(values)):
        if first != values[i]:
            return False

    return True


def most_common_target_value(records,target_attribute):
    cnt = Counter()
    for item in map(lambda x: x[target_attribute], records):
        cnt[item] += 1
    most_frequent = cnt.most_common(1)
    for key in most_frequent:
        most_frequent_val = key[0]
    return most_frequent_val

def get_target_value_counts(records, target_attribute):
    cnt = Counter()
    for record in records:
        cnt[record[target_attribute]] += 1

    most_common_vals = cnt.most_common()
    value_counts = []
    for key in most_common_vals:
        value_counts.append(key[1])

    return value_counts

def group_by_values(examples, attr):
    res = {}
    for example in examples:
        if not example[attr] in res:
            res[example[attr]] = []
        res[example[attr]].append(example)

    return res

def get_best_classifier_attr(examples, target_attr, attrs):
    inf_gains = {}
    entropy_all = entropy(len(examples), get_target_value_counts(examples, target_attr))
    for attr in attrs:
        grouped = group_by_values(examples, attr)
        entropies = []
        group_sizes = []
        for group in grouped:
            group_sizes.append(len(grouped[group]))
            entropies.append(entropy(len(grouped[group]), get_target_value_counts(grouped[group], target_attr)))
        inf_gains[attr] = inf_gain(entropy_all, len(examples), group_sizes, entropies)

    max_info_gain_attr = ''
    max_info_gain = -float('inf')

    for attr in inf_gains:
        if inf_gains[attr] > max_info_gain:
            max_info_gain_attr = attr
            max_info_gain = inf_gains[attr]



    return max_info_gain_attr

def ID3(examples, target_attribute, attributes):
    if all_same(map(lambda x: x[target_attribute], examples)):
        return Node(examples[0][target_attribute])
    if len(attributes) == 0:
        return Node(most_common_target_value(examples, target_attribute))
    best_attr = get_best_classifier_attr(examples, target_attribute, attributes)
    node_attr = Node(best_attr)
    grouped = group_by_values(examples, best_attr)
    for group in grouped:
        group_examples = grouped[group]
        cloned = list(attributes)
        cloned.remove(best_attr)
        node_attr.children.append({group: ID3(group_examples, target_attribute, cloned)})
    return node_attr


def entropy(training_set_size, label_sizes):
    res = 0.0
    for label_size in label_sizes:
        prob = float(label_size)/training_set_size
        if prob != 0:
            res += prob * math.log(prob,2)
    return -res

def inf_gain(ent, training_set_size, label_sizes, label_values):
    res = 0.0
    for i in range(0,len(label_sizes)):
        res += (label_sizes[i]/float(training_set_size)) * label_values[i]

    return ent-res

