#!/usr/bin/python

import sys,csv
from attributeDescriptor import get_attribute_descriptors
from kNNProcess import KNNProcess
from FileProcessor import FileProcessor

def process_data(input_file, output_file, attribute_descriptors):
    delimiter = ','
    file_processor = FileProcessor(input_file, delimiter)
    parsed_lines = file_processor.get_lines_as_array()
    knn_processor = KNNProcess(parsed_lines, attribute_descriptors)
    line_no = 0
    for line in parsed_lines:
        imputed_line = knn_processor.replace_missing_line(line_no)
        file_processor.set_line(line_no, imputed_line)
        line_no += 1
    if file_processor.generate_output(output_file):
        print 'Success!'

def main(argv):
    training_file = argv[0]
    testing_file = argv[1]
    training_output = 'crx.training.processed'
    testing_output = 'crx.testing.processed'
    attribute_descriptors = get_attribute_descriptors()
    process_data(training_file, training_output, attribute_descriptors)
    process_data(testing_file, testing_output, attribute_descriptors)

if __name__ == '__main__':
    main(sys.argv[1:])
