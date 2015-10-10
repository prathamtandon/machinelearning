from attributeDescriptor import AttributeType
from math import sqrt

class kNNOutput:
    def __init__(self, distance, label):
        self.distance = distance
        self.label = label

    def __repr__(self):
        return '(' + str(self.distance) + ',' + str(self.label) + ')\n'

class kNNClassifier:
    def __init__(self, k, training_set, attribute_descriptors):
        self.k = k
        self.training_set = training_set
        self.attribute_descriptors = attribute_descriptors

    def get_label(self, training_example):
        return training_example[len(training_example)-1]

    def get_nominal_distance(self, training_attr_val, testing_attr_val):
        return 0 if training_attr_val == testing_attr_val else 1

    def get_continuous_distance(self, training_attr_val, testing_attr_val):
        return float(training_attr_val) - float(testing_attr_val)

    def get_distance(self, training, testing):
        if len(training) != len(testing):
            raise ValueError('Training and testing must have same number of attributes')
        sum_value = 0.0
        count = 0
        for i in range(len(training)-1):
            count += 1
            if self.attribute_descriptors[i].get_attribute_type() == AttributeType.NOMINAL:
                sum_value += self.get_nominal_distance(training[i],testing[i])
            else:
                sum_value += pow(self.get_continuous_distance(training[i], testing[i]), 2)

        return sqrt(sum_value)

    def find_most_common_label(self, first_k):
        hash_map = {}
        labels = map(lambda x: x.label, first_k)
        for label in labels:
            if label in hash_map:
                hash_map[label] += 1
            else:
                hash_map[label] = 1

        max_count = -1
        predicted_label = ''
        for label in hash_map:
            if hash_map[label] > max_count:
                predicted_label = label
                max_count = hash_map[label]

        return predicted_label

    def get_labeled(self, testing_example):
        if len(self.training_set) == 0 or testing_example is None:
            return
        result = []
        for training_example in self.training_set:
            dist = self.get_distance(training_example, testing_example)
            label = self.get_label(training_example)
            output = kNNOutput(dist, label)
            result.append(output)
        result = sorted(result, key=lambda x: x.distance)
        k = int(self.k)
        testing_label = self.find_most_common_label(result[:k+1])
        testing_example.append(testing_label)
        return testing_example



