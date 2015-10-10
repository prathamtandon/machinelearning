import math
from attributeDescriptor import AttributeType

def get_z_scaling(raw_value, mean, standard_dev):
    return (raw_value - mean) / standard_dev

def get_standard_deviation(N, raw_values, mean):
    sum_value = 0.0
    for i in range(0, N):
        sum_value += pow(raw_values[i] - mean, 2)
    return math.sqrt(sum_value/N)

class KNNProcess:

    def __init__(self, examples=[], attribute_descriptors=[]):
        self.examples = examples
        self.attribute_descriptors = attribute_descriptors
        self.missing_identifier = '?'
        self.medians = None
        self.means = None
        self.standard_deviations = None

    def get_mean(self, attribute_index, label=None):
        if self.means is None:
            self.set_means()
        if label is not None:
            return self.means[attribute_index][label]
        else:
            return self.means[attribute_index]['overall']

    def get_attribute_indices(self, attr_type):
        return [i for i in range(0, len(self.attribute_descriptors)) if self.attribute_descriptors[i].get_attribute_type() == attr_type]

    def set_means(self):
        if len(self.examples) == 0:
            return
        continuous_indices = self.get_attribute_indices(AttributeType.CONTINUOUS)
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
        nominal_indices = self.get_attribute_indices(AttributeType.NOMINAL)
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


    def set_standard_deviations(self):
        if len(self.examples) == 0:
            return
        continuous_indices = self.get_attribute_indices(AttributeType.CONTINUOUS)
        self.standard_deviations = {}
        for index in continuous_indices:
            # Assumption: No missing values in data.
            # Assumption: Means are pre-computed.
            attribute_values = map(lambda x: float(x[index]), self.examples)
            self.standard_deviations[index] = get_standard_deviation(len(self.examples), attribute_values, self.means[index]['overall'])

    def get_normalized_value(self, attribute_index, raw_value):
        if self.means is None:
            self.set_means()
        if self.standard_deviations is None:
            self.set_standard_deviations()
        return get_z_scaling(float(raw_value), self.means[attribute_index]['overall'], self.standard_deviations[attribute_index])

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

    def normalize_line(self, line):
        normalized_line = []
        for i in range(0, len(line)):
            attribute_descriptor = self.attribute_descriptors[i]
            if attribute_descriptor.get_attribute_type() == AttributeType.CONTINUOUS:
                normalized_line.append(self.get_normalized_value(i, line[i]))
            else:
                normalized_line.append(line[i])

        return normalized_line

    def replace_missing_line(self, line_no):
        if line_no < 0 or line_no > len(self.examples) - 1:
            raise ValueError('Invalid line number')
        line = self.examples[line_no]
        if len(line) != len(self.attribute_descriptors):
            raise Exception('Invalid number of attributes in example')
        self.examples[line_no] = self.replace_missing_value(line)
        return self.examples[line_no]
