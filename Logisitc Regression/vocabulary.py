from constants import vocabulary_filepath, labels_filepath
from FileProcessor import FileProcessor

def get_vocabulary_size():
        fp = FileProcessor(vocabulary_filepath, ' ')
        lines = fp.parse_input_file()
        return len(lines)

def get_labels():
        fp = FileProcessor(labels_filepath, ' ')
        lines = fp.parse_input_file()
        return [float(lines[0][1]), float(lines[1][1])]
