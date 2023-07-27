from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import sys,os
sys.path.append(os.getcwd())
from src.utils import utils

class PivotPipeline():
    def __init__(self, index, columns, values, aggfunc, fill_value=None, prefix_text=None, sufix_text=None):
        self.INDEXES = index
        self.COLUMNS = columns
        self.VALUES = values
        self.AGGFUNC = aggfunc
        self.FILL_VALUE = fill_value
        self.PREFIX_TEXT = prefix_text
        self.SUFIX_TEXT = sufix_text
        
    def fit(self, X, y):
        return self

    def transform(self, X, y):
        X = X.reset_index()
        X = X.pivot_table(index=self.INDEXES,
                        columns=self.COLUMNS,
                        values=self.VALUES,
                        aggfunc=self.AGGFUNC,
                        fill_value=self.FILL_VALUE,
                        )
        X = utils.append_column_names(X, prefix_text=self.PREFIX_TEXT, sufix_text=self.SUFIX_TEXT).reset_index()
        X = X.set_index('index').sort_index()
        y = y.drop_duplicates().sort_index()        
        return X, y
    
    def fit_transform(self, X, y):
        return self.fit(X, y).transform(X, y)

class BuildFeatures_CV(BaseEstimator, TransformerMixin):
    """"
    Class used to create features that need to be cross validated to prevent Data Leakage.
    """
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        return X
    
class BuildFeatures(BaseEstimator, TransformerMixin):
    """
    Class used to create features that not need to be cross validated to prevent Data Leakage
    """
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        return X, y
