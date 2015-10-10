import csv

class FileProcessor:

    def __init__(self, filepath, delimiter):
        self.filepath = filepath
        self.delimiter = delimiter
        self.lines = []

    def parse_input_file(self):
        if self.filepath == [] or self.delimiter == '':
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
