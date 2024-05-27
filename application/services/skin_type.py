import pandas as pd
import numpy as np
from sklearn.manifold import TSNE

from .repository_service import get_skin_types

class SkinTypeAnalyzer:
    def __init__(self):
        self.df = None
        self.N = 0
        self.M = 0
        self.ingredient_idx = {}
        self.A = None
        self.model = None
        pass

    def edit_data(self, path):
        dataset = pd.read_csv(path, sep=';', header=0, names=None, encoding="utf-8")
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

    def load_data(self):
        skin_types = get_skin_types()
        self.df = pd.DataFrame(skin_types)
        self.df = self.df.reset_index(drop=True)

    def get_data(self):
        corpus = []
        idx = 0

        # For loop for tokenization
        for i in range(len(self.df)):
            ingredients = self.df['ingredients'][i]
            tokens = ingredients.split(', ')
            # ingredients_lower = ingredients.lower()
            # tokens = ingredients_lower.split(', ')
            corpus.append(tokens)
            for ingredient in tokens:
                if ingredient not in self.ingredient_idx:
                    self.ingredient_idx[ingredient] = idx
                    idx += 1
            # Get the number of items and tokens
            self.M = len(self.df)
            self.N = len(self.ingredient_idx)

            # Initialize a matrix of zeros
            self.A = np.zeros([self.M, self.N])

            i = 0
            for tokens in corpus:
                self.A[i, :] = self.oh_encoder(tokens)
                i += 1

            self.model = TSNE(n_components=2, learning_rate=200, random_state=42)
            tsne_features = self.model.fit_transform(self.A)

            # Make X, Y columns
            self.df['X'] = tsne_features[:, 0]
            self.df['Y'] = tsne_features[:, 1]

    def oh_encoder(self, tokens):
        x = np.zeros(self.N)
        for ingredient in tokens:
            # Get the index for each ingredient
            idx = self.ingredient_idx[ingredient]
            # Put 1 at the corresponding indices
            x[idx] = 1
        return x

if __name__ == '__main__':
    skin_analyzer = SkinTypeAnalyzer()
    # skin_analyzer.get_data()


