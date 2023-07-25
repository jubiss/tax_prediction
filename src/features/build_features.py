from sklearn.base import BaseEstimator, TransformerMixin

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
        return X
    
    