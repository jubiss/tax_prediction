import pandas as pd
import src.features as features
import src.models as models
from sklearn.model_selection import GridSearchCV
import joblib

model_type = 'classification'

datapath = '\data\raw\table.csv'
df = pd.read_csv(datapath)

target = None
validation, df = df[:len(df)*0.2], df[len(df)*0.2:]
X, y = df.drop(columns=target), df[target]

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
joblib.dump(cv_result, f'models\{model_name}')