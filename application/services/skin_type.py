import pandas

class SkinTypeAnalyzer:
    def __init__(self):
        # self.dataset = None
        pass

    def edit_data(self, path):
        dataset = pandas.read_csv(path, sep=';', header=0, names=None, encoding="utf-8")
        rows = dataset.shape[0]
        values = []
        valuemax = 0
        for row in range(0, rows-1):
            line = list(dataset.iloc[row, 0])
            # line = list(dataset[0].values[row])
            new_line = []
            flag_start = False
            flag_end = False
            flag_skip = False
            for char in line:
                if char != ' ':
                    flag_skip = False
                if char == '(':
                    # flag_start = True
                    flag_end = True
                elif char == ')':
                    flag_end = False
                    flag_skip = True
                if not flag_skip and not flag_end and char != '.':
                    new_line.append(char)
            dataset.iloc[row,0] = ''.join(list(new_line))
        dataset.to_csv(path, sep=';')


if __name__ == '__main__':
    skin_analyzer = SkinTypeAnalyzer()
    skin_analyzer.edit_data('D:\\hz.csv')


