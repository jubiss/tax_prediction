import sys,os
sys.path.append(os.getcwd())
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
from src.features import build_features
import src.models as models
from src.utils import utils


model_type = 'classification'

datapath = r'data\processed\nfe_das_data.csv'
df = pd.read_csv(datapath)

df, many_to_one_relation = utils.many_to_one(df, index_columns=['CNPJ_CPF', 'NUMERO'])

target = 'ICMS DEVIDO'
X, y = df.drop(columns=target), df[target]

pivot = build_features.PivotPipeline(index=['index', 'UF', 'FRETE'],
                                     columns = 'CODIGONCM',
                                     values = 'TOTAL COM IMPOSTOS',
                                     aggfunc = 'sum',
                                     fill_value=  0,
                                     prefix_text= 'NCM',
                                     sufix_text= 'VALUE')

enc = OneHotEncoder(handle_unknown='ignore')
categorical_features = ['UF']

transform_categorical = ColumnTransformer(
    transformers=[
        ('OneHotEncoder', enc, categorical_features)
    ]
)

X, y = pivot.fit_transform(X, y)


breakpoint()


"""target = None
validation, df = df[:len(df)*0.2], df[len(df)*0.2:]

X_val, y_val = validation.drop(columns=target), df[target]

model, param_grid = models.models.xgboost()

#boruta_selector = BorutaPy(model_, n_estimators='auto', verbose=2, random_state=1)

pipeline = ["Pre process features", features.PreProcessingFeatures(),
            "Feature Engineering", features.BuildFeatures(),
            "Feature Engineering CV", features.BuildFeaturesCV(),
            "Model", model,
            #"Feature Selection", boruta_selector
            ]

cv_result = GridSearchCV(pipeline, param_grid, cv=5)
cv_result.fit(X, y)

predict = cv_result.predict(X_val, y_val)
if model_type == 'classification':
    models.model_evaluation(model_type=model_type, y_true=y_val, y_pred=predict)


# Save Model
model_name = 'last_model'
joblib.dump(cv_result, f'models\{model_name}')"""