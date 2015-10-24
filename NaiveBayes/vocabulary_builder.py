# Builds the vocabulary of words used by Naive Bayes learner using
# the information provided in processed/vocabulary.txt

from FileProcessor import FileProcessor
from constants import vocabulary_filepath

vocabulary = {}
delimiter = ' '

def create_vocabulary():
    fp = FileProcessor(vocabulary_filepath, delimiter)
    parsed_data = fp.get_lines_as_array()
    for row in parsed_data:
        word = row[0]
        frequency = row[1]
        vocabulary[word] = frequency

create_vocabulary()

