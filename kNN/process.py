#!/usr/bin/python

import sys,csv
from enum import Enum

class AttributeType(Enum):
    NOMINAL = 1
    CONTINUOUS = 2
    LABEL = 3

class AttributeDescriptor:

    def __init__(self, attribute_type, attribute_values=None):
        self.attribute_type = attribute_type
        self.attribute_values = attribute_values

    def get_attribute_type(self):
        return self.attribute_type

    def get_attribute_values(self):
        return self.attribute_values

class KNNProcess:

    def __init__(self, examples=[], attribute_descriptors=[]):
        self.examples = examples
        self.attribute_descriptors = attribute_descriptors
        self.missing_identifier = '?'
        self.medians = None
        self.means = None

    def get_mean(self, attribute_index, label=None):
        if self.means is None:
            self.set_means()
        if label is not None:
            return self.means[attribute_index][label]
        else:
            return self.means[attribute_index]['overall']

    def set_means(self):
        if len(self.examples) == 0:
            return
        continuous_indices = [i for i in range(0,len(self.attribute_descriptors)) if self.attribute_descriptors[i].get_attribute_type() == AttributeType.CONTINUOUS]
        self.means = {}
        for index in continuous_indices:
            non_missing = filter(lambda x: x[index] != self.missing_identifier, self.examples)
            attribute_values = map(lambda x: x[index], non_missing)
            label_values = map(lambda x: x[len(x)-1], non_missing)
            positive_labels = []
            negative_labels = []
            for j in range(0, len(label_values)):
                if label_values[j] == '+':
                    positive_labels.append(float(attribute_values[j]))
                else:
                    negative_labels.append(float(attribute_values[j]))
            self.means[index] = {}
            positive_sum = sum(positive_labels)
            negative_sum = sum(negative_labels)
            self.means[index]['+'] = positive_sum/len(positive_labels)
            self.means[index]['-'] = negative_sum/len(negative_labels)
            self.means[index]['overall'] = (positive_sum + negative_sum)/len(attribute_values)

    def set_medians(self):
        if len(self.examples) == 0:
            return
        nominal_indices = [i for i in range(0,len(self.attribute_descriptors)) if self.attribute_descriptors[i].get_attribute_type() == AttributeType.NOMINAL]
        self.medians = {}
        for index in nominal_indices:
            attribute_values = map(lambda x: x[index], self.examples)
            non_missing = filter(lambda x: x != self.missing_identifier, attribute_values)
            sorted_values = sorted(non_missing)
            self.medians[index] = sorted_values[len(sorted_values)/2]

    def get_median(self, attribute_index):
        if self.medians is None:
            self.set_medians()
        return self.medians[attribute_index]

    def get_standard_deviation(self, attr):
        return None

    def get_normalized_value(self, raw_value):
        return None

    def get_missing_nominal_value(self, attribute_index, example_value):
        if example_value != self.missing_identifier:
            return example_value
        return self.get_median(attribute_index)

    def get_missing_continuous_value(self, attribute_index, example_value, label):
        if example_value != self.missing_identifier:
            return example_value
        return self.get_mean(attribute_index, label)

    def replace_missing_value(self, line):
        imputed_line = []
        for i in range(0, len(line)):
            attribute_descriptor = self.attribute_descriptors[i]
            if attribute_descriptor.get_attribute_type() == AttributeType.NOMINAL:
                imputed_line.append(self.get_missing_nominal_value(i, line[i]))
            elif attribute_descriptor.get_attribute_type() == AttributeType.CONTINUOUS:
                imputed_line.append(self.get_missing_continuous_value(i, line[i], line[len(line)-1]))
            else:
                imputed_line.append(line[i])

        return imputed_line

    def replace_missing_line(self, line_no):
        if line_no < 0 or line_no > len(self.examples) - 1:
            raise ValueError('Invalid line number')
        line = self.examples[line_no]
        if len(line) != len(self.attribute_descriptors):
            raise Exception('Invalid number of attributes in example')
        return self.replace_missing_value(line)

class FileProcessor:

    def __init__(self, filepath, delimiter):
        self.filepath = filepath
        self.delimiter = delimiter
        self.lines = []

    def parse_input_file(self):
        if self.filepath == '' or self.delimiter == '':
            raise ValueError('File path not specified')
        with open(self.filepath, 'rb') as examples_file:
            examples_reader = csv.reader(examples_file, delimiter = self.delimiter)
            for row in examples_reader:
                self.lines.append(row)

        return self.lines

    def get_lines_as_array(self):
        if len(self.lines) > 0:
            return self.lines
        else:
            return self.parse_input_file()

    def set_line(self, line_number, line):
        if line_number < 0 or line_number > len(self.lines):
            raise ValueError('Invalid line number')
        self.lines[line_number] = line

    def generate_output(self, outfile=''):
        if outfile == '':
            raise ValueError('Invalid output file')
        with open(outfile, 'wb+') as processed_file:
            processed_writer = csv.writer(processed_file, delimiter = self.delimiter)
            for line in self.lines:
                processed_writer.writerow(line)
            return True

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

def get_attribute_descriptors():
    attributes = []

    attribute = AttributeDescriptor(AttributeType.NOMINAL, ['b', 'a'])
    attributes.append(attribute)
    attribute = AttributeDescriptor(AttributeType.CONTINUOUS)
    attributes.append(attribute)
    attribute = AttributeDescriptor(AttributeType.CONTINUOUS)
    attributes.append(attribute)
    attribute = AttributeDescriptor(AttributeType.NOMINAL, ['u','y','l','t'])
    attributes.append(attribute)
    attribute = AttributeDescriptor(AttributeType.NOMINAL, ['g','p','gg'])
    attributes.append(attribute)
    attribute = AttributeDescriptor(AttributeType.NOMINAL, ['c', 'd', 'cc', 'i', 'j', 'k', 'm', 'r', 'q', 'w', 'x', 'e', 'aa', 'ff'])
    attributes.append(attribute)
    attribute = AttributeDescriptor(AttributeType.NOMINAL, ['v', 'h', 'bb', 'j', 'n', 'z', 'dd', 'ff', 'o'])
    attributes.append(attribute)
    attribute = AttributeDescriptor(AttributeType.CONTINUOUS)
    attributes.append(attribute)
    attribute = AttributeDescriptor(AttributeType.NOMINAL, ['t','f'])
    attributes.append(attribute)
    attribute = AttributeDescriptor(AttributeType.NOMINAL, ['t','f'])
    attributes.append(attribute)
    attribute = AttributeDescriptor(AttributeType.CONTINUOUS)
    attributes.append(attribute)
    attribute = AttributeDescriptor(AttributeType.NOMINAL, ['t','f'])
    attributes.append(attribute)
    attribute = AttributeDescriptor(AttributeType.NOMINAL, ['g','p','s'])
    attributes.append(attribute)
    attribute = AttributeDescriptor(AttributeType.CONTINUOUS)
    attributes.append(attribute)
    attribute = AttributeDescriptor(AttributeType.CONTINUOUS)
    attributes.append(attribute)
    attribute = AttributeDescriptor(AttributeType.LABEL, ['+','-'])
    attributes.append(attribute)

    return attributes

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
