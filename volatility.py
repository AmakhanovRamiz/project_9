
class TikVolatility:

    def __init__(self, file_name):
        self.file_name = file_name
        self.tik_list = []
        self.tik_null_list = []  # для хранения нулевых трекеров

    def unzip(self):
        try:
            zfile = zipfile.ZipFile(self.file_name, 'r')
            for filename in zfile.namelist():
                zfile.extract(filename)
            self.file_name = self.file_name.rsplit(".", 1)[0]
            self.file_path = os.path.join(os.path.dirname(__file__), self.file_name)
        except FileNotFoundError:
            print('Указанный файл не существует. Пожалуйста, проверьте наличие файла или его название')
            return

    def run(self):
        for dirpath, dirnames, filenames in os.walk(self.file_path):
            for file in filenames:
                self._csv_handler(dirpath, file)
        self._sort_tik_list()
        self._catch_null_csv()

    def _csv_handler(self, dirpath, file):
        full_path = os.path.join(dirpath, file)
        with open(full_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            csv_list = []
            for row in csv_reader:
                csv_list.append(row)
        csv_list = sorted(csv_list, key=lambda x: float(x[2]))
        csv_min = csv_list[0]
        csv_max = csv_list[-1]
        half_sum = (float(csv_max[2]) + float(csv_min[2])) / 2
        volatylity = ((float(csv_max[2]) - float(csv_min[2])) / half_sum) * 100
        self.tik_list.append([csv_list[0][0], volatylity])

    def _catch_null_csv(self):
        while self.tik_list[0][1] == 0.0:
            self.tik_null_list.append(self.tik_list[0])
            self.tik_list.pop(0)

    def _sort_tik_list(self):
        self.tik_list = sorted(self.tik_list, key=lambda x: float(x[1]))

    def print_result(self):
        max_val = self.tik_list[-1]
        max_val2 = self.tik_list[-2]
        max_val3 = self.tik_list[-3]
        min_val = self.tik_list[0]
        min_val2 = self.tik_list[1]
        min_val3 = self.tik_list[2]
        print(
            'Максимальная волатильность:\n\t {} - {}% \n\t {} - {}% \n\t {} - {}%'.format(
                max_val[0], "{0:4.2f}".format(float(max_val[1])),
                max_val2[0], "{0:4.2f}".format(float(max_val2[1])),
                max_val3[0], "{0:4.2f}".format(float(max_val3[1]))))
        print(
            'Минимальная волатильность:\n\t {} - {}% \n\t {} - {}% \n\t {} - {}%'.format(
                min_val3[0], "{0:4.2f}".format(float(min_val3[1])),
                min_val2[0], "{0:4.2f}".format(float(min_val2[1])),
                min_val[0], "{0:4.2f}".format(float(min_val[1]))))
        print(
            'Нулевая волатильность:')
        for item in self.tik_null_list:
            print(item[0], end=', ')
        print('\n')


@time_track
def main():
    tik = TikVolatility('trades.zip')
    tik.unzip()
    tik.run()
    tik.print_result()

if __name__ == '__main__':
    main()


