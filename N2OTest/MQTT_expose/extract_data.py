from line_processor import *
from path_helper import PathHelper
from field_writer import FieldWriter

class Extractor(object):
    
    def __init__(self):
        self._path_helper = PathHelper()
        self._field_writer = FieldWriter()

    def extract_data_to_csv_from_folder(self, path):
        self._extract_from_path(path)
        self._field_writer.write_data_to_files()

    def _extract_from_path(self, path):
        if self._path_helper.is_file(path):
            self._extract_from_file(path)
        else: 
            self._extract_from_folder(path)

    def _extract_from_file(self, path):
        key = self._path_helper.get_dictionary_key(path) 
        file_path = self._path_helper.get_absolute_path(path)
        lines = self._path_helper.get_lines_from_file(file_path)
        self._write_data(lines, key)

    def _extract_from_folder(self, folderPath):
        for named_file in self._path_helper.get_files_under_path(folderPath):
            new_path = self._path_helper.join_path(folderPath, named_file)
            self._extract_from_path(new_path)

    def _write_data(self, lines, key):
        LineProcessor.process_lines(lines)
        self._field_writer.set_field(key)
        LineProcessor.reset_line_processors()

def main():
    extractor = Extractor()
    print('[INFO] start extracting...')
    extractor.extract_data_to_csv_from_folder('log')
    print('[INFO] done')
    

if __name__ == '__main__':
    main()
