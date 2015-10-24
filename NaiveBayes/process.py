# Provides an API to compute the size of training corpus, optionally,
# labeled by a particular class.

from FileProcessor import FileProcessor
from constants import training_metadata_filepath, label_mappings, training_template_filepath, training_filepath_placeholder

corpus_sizes = {}
corpus = {}


def get_training_filepath(label):
    return training_template_filepath.replace(training_filepath_placeholder, label)


def get_total_corpus_size():
    total_size = 0
    for label in corpus_sizes:
        total_size += corpus_sizes[label]
    return total_size

def init_corpus_sizes():
    fp = FileProcessor(training_metadata_filepath, '/')
    parsed_lines = fp.get_lines_as_array()
    for row in parsed_lines:
        label = row[0]
        if label in corpus_sizes:
            corpus_sizes[label] += 1
        else:
            corpus_sizes[label] = 1

# Returns the # of training documents labeled with label.
# If label is None, returns the total number of training documents.
def get_corpus_size(label=None):
    if len(corpus_sizes) == 0:
        init_corpus_sizes()

    if label is None:
        return get_total_corpus_size()
    elif label in corpus_sizes:
        return corpus_sizes[label]
    else:
        return 0

def init_corpus():
    for label in label_mappings:
        training_filepath = get_training_filepath(label)
        fp = FileProcessor(training_filepath, ' ')
        parsed_lines = fp.get_lines_as_array()
        label_map = {}
        for row in parsed_lines:
            word = row[0]
            frequency = row[1]
            label_map[word] = frequency
        corpus[label] = label_map


# Returns a dictionary of words and their frequencies for a given
# class label.
def get_corpus(label):
    if len(corpus) == 0:
        init_corpus()
    if label in corpus:
        return corpus[label]
    else:
        raise ValueError('get_corpus::Invalid label')

# Returns the count of all words observed across all documents for a 
# given class label
def get_words_count(label):
	if len(corpus) == 0:
		init_corpus()
	count = 0
	for word in corpus[label]:
		count += int(corpus[label][word])
	
	return count
