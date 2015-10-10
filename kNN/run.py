#!/usr/bin/python

import sys
import attributeDescriptor
from kNN import kNNClassifier
from FileProcessor import FileProcessor

def get_data_set(filename):
    delimiter = ','
    fp = FileProcessor(filename, delimiter)
    return fp.get_lines_as_array()

def main(argv):
    k = argv[0]
    training_file_name = argv[1]
    testing_file_name = argv[2]
    training_set = get_data_set(training_file_name)
    testing_set = get_data_set(testing_file_name)
    classifier = kNNClassifier(k, training_set, attributeDescriptor.get_lenses_attribute_descriptors() if len(training_set[0]) == 5 else attributeDescriptor.get_ca_attribute_descriptors())
    result = []
    for testing_example in testing_set:
        result.append(classifier.get_labeled(testing_example))

    string_result = map(lambda x: str(x).replace(" ","").replace("[","").replace("]",""), result)
    sys.stdout.write("\n".join(string_result))
    sys.exit(0)

if __name__ == '__main__':
    main(sys.argv[1:])
