# Check yellow brick for model evaluation and visualization
import pandas as pd
def evaluate_models(model_type, y_true, y_pred):
    if model_type == 'classification':
        from sklearn.metrics import classification_report
        report = classification_report(y_true, y_pred, output_dict=True)
        df = pd.DataFrame(report).transpose()
        df.to_html()
        



