from line_processor import *
from collections import defaultdict

class FieldWriter(object):

    def __init__(self):
        self._broadcast_time = defaultdict(list)
        self._file_loss_rate = defaultdict(list)
        self._mse = defaultdict(list)
        self._ssim = defaultdict(list)

    def set_field(self, key):
        self._set_broadcast(key)
        self._set_loss_rate(key)
        self._set_mse_ssim(key)

    def _set_broadcast(self, key):
        broadcast_numbers = self._get_broadcast_param()[1]
        if broadcast_numbers:
            self._write_broadcast_data(key)

    def _get_broadcast_param(self):
        line_processor = LineProcessorFactory.get_broadcast_line_processor()

        return (line_processor.total_broadcast_time, 
                line_processor.lines_processed)

    def _write_broadcast_data(self, key):
        total_broadcast_time, broadcast_numbers = self._get_broadcast_param()
        average_time = total_broadcast_time / broadcast_numbers
        self._broadcast_time[key].append(round(average_time, 5))
   
    def _set_mse_ssim(self, key):
        received_number = self._get_file_received_param()
        if received_number:
            self._write_mse_ssim_data(key)

    def _get_file_received_param(self):
        line_processor = LineProcessorFactory.get_file_received_line_processor()

        return line_processor.files_received

    def _write_mse_ssim_data(self, key):
        total_mse, total_ssim = self._get_mse_ssim_param()
        received_number = self._get_file_received_param()
        self._mse[key].append(total_mse / received_number)
        self._ssim[key].append(total_ssim / received_number)

    def _get_mse_ssim_param(self):
        line_processor = LineProcessorFactory.get_mse_ssim_line_processor()

        return (line_processor.total_mse, line_processor.total_ssim)

    def _set_loss_rate(self, key):
        lost_number = self._get_file_loss_param()
        received_number = self._get_file_received_param()
        desired_number = lost_number + received_number
        if desired_number:
            self._write_loss_rate_data(key)

    def _get_file_loss_param(self):
        line_processor = LineProcessorFactory.get_file_loss_line_processor()

        return line_processor.files_lost

    def _write_loss_rate_data(self, key):
        lost_number = self._get_file_loss_param()
        received_number = self._get_file_received_param()
        desired_number = lost_number + received_number
        loss_rate = lost_number / desired_number
        self._file_loss_rate[key].append(round(loss_rate, 3))

    def write_data_to_files(self):
        self._write_log('broadcast_time.csv', self._broadcast_time)
        self._write_log('file_loss_rate.csv', self._file_loss_rate)
        self._write_log('mse.csv', self._mse)
        self._write_log('ssim.csv', self._ssim)

    def _write_log(self, filename, dictionary):
        columns = self._get_columns(dictionary)
        if columns:
            self._write_header(filename, columns)
            self._write_body(filename, dictionary)

    def _get_columns(self, dictionary):
        columns = ''
        if dictionary:
            columns = list(dictionary.keys())
            columns = ','.join(columns)

        return columns

    def _write_header(self, filename, columns):
        with open(filename, 'w') as f:
            f.write("%s\n"%(columns))

    def _write_body(self, filename, dictionary):
        values = self._get_values(dictionary)
        for index_of_value in range(len(values[0])):
            data = self._get_prepared_data(values, index_of_value)
            self._write_prepared_data(filename, data)

    def _get_values(self, dictionary):
        values = list(dictionary.values())

        return values

    def _get_prepared_data(self, values, index_of_value):
        data = []
        for value in values:
            try:
                data.append(str(value[index_of_value]))
                data.append(',')
            except:
                data.append('N/A')
                data.append(',')

        del data[-1]
        data = ''.join(data)

        return data

    def _write_prepared_data(self, filename, data):
        with open(filename, 'a') as f:
            f.write("%s\n"%(data))

