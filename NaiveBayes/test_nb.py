# Take the learned nb hypothesis and applies it to testing examples.
from constants import test_filepath, label_mappings, output_filepath
from math import log
from FileProcessor import FileProcessor

def test_naive_bayes(hypothises):
    fp = FileProcessor(test_filepath, ' ')
    parsed_lines = fp.get_lines_as_array()
    results = []
    for row in parsed_lines:
        exclude_label = row[1:]
        max_sum = -float('Inf')
        max_label = -1

        for label in label_mappings:
            label_instance = hypothises[label]
            log_prior = log(label_instance.get_prior(), 2)
            densities = label_instance.get_densities()
            log_sum = 0

            for word in exclude_label:
                log_sum += log(densities[word], 2)
                    
            cur_sum = log_sum + log_prior
            if cur_sum > max_sum:
                max_sum = cur_sum
                max_label = label

        results.append(label_mappings[max_label])

    fp.generate_output(output_filepath, results)



