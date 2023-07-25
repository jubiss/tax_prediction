from sklearn.base import BaseEstimator, TransformerMixin

class PreProcessingFeatures(BaseEstimator, TransformerMixin):
    """Class used to make all the preprocessing steps for the model to work properly"""
    def __init__(self):
        pass

    def fit(self,X, y=None):
        pass

    def transform(self,X, y=None):
        pass

    def missing_values(self, X, y):
        # Dealing with missing values
        pass

    def transforming_data(self, X, y):
        # Transforming data
        pass

    def scaling_data(self, X, y):
        pass

    def enconding_data(self, X, y):
        pass

    def outliers(self, X, y):
        pass