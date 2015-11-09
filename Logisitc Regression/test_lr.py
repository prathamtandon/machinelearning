from constants import testing_data_filepath, output_filepath, labels_output_filepath
from FileProcessor import FileProcessor
from vocabulary import get_labels
from utils import sigmoid


def generate_labels():
        fp = FileProcessor(testing_data_filepath, ' ')
        rows = fp.parse_input_file()
        expected = []
        for row in rows:
                expected.append(row[0])
        
        if fp.generate_output(labels_output_filepath, expected):
                return True

def test_logistic_regression(w):
        if not generate_labels():
                return
        fp = FileProcessor(testing_data_filepath, ' ')
        rows = fp.parse_input_file()
        output = []
        expected = []
        labels = get_labels()
        
        for row in rows:
             expected.append(row[0])
             row = row[1:]
             sum_val = w[0]
             for feature in row:
                     feature_id = int(feature.split(':')[0])
                     sum_val += w[feature_id]
             
             if sigmoid(sum_val) >= 0.5:
                     output.append(labels[0])
             else:
                     output.append(labels[1])
        
        if fp.generate_output(output_filepath, output):
                print 'Successfully generated predictions.lr'
                
                     
                     
