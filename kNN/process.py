#!/usr/bin/python

import sys,csv
from attributeDescriptor import get_ca_attribute_descriptors
from kNNProcess import KNNProcess
from FileProcessor import FileProcessor

def process_data(training_file, testing_file, training_output, testing_output, attribute_descriptors):
    delimiter = ','
    training_file_processor = FileProcessor(training_file, delimiter)
    testing_file_processor = FileProcessor(testing_file, delimiter)
    training_lines = training_file_processor.get_lines_as_array()
    testing_lines = testing_file_processor.get_lines_as_array()
    all_lines = training_lines + testing_lines
    knn_processor = KNNProcess(all_lines, attribute_descriptors)
    imputed_lines = map(lambda line_no: knn_processor.replace_missing_line(line_no), range(0, len(all_lines)))
    normalized_lines = map(lambda line: knn_processor.normalize_line(line), imputed_lines)
    for line_no, line in enumerate(normalized_lines[:len(training_lines)]):
        training_file_processor.set_line(line_no, line)
    for line_no, line in enumerate(normalized_lines[len(training_lines):]):
        testing_file_processor.set_line(line_no, line)
    if training_file_processor.generate_output(training_output) and testing_file_processor.generate_output(testing_output):
        print 'Success!'

def main(argv):
    training_file = argv[0]
    testing_file = argv[1]
    training_output = 'crx.training.processed'
    testing_output = 'crx.testing.processed'
    attribute_descriptors = get_ca_attribute_descriptors()
    process_data(training_file, testing_file, training_output, testing_output, attribute_descriptors)

if __name__ == '__main__':
    main(sys.argv[1:])
