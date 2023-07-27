import os.path
import pandas as pd
def save_csv(dataframe, filepath_name, save=False):
    if save:
        if os.path.exists(filepath_name):
            overwrite = input("File Exist overwrite the file? [S/N]")
            if overwrite == "S":
                dataframe.to_csv(filepath_name, index=False)
            else:
                return
        else:
            dataframe.to_csv(filepath_name, index=False)

def append_column_names(dataframe, sufix_text=None, prefix_text=None):
    columns = []
    for column in dataframe.columns:
        columns.append(f'{prefix_text}_{column}_{sufix_text}')
    dataframe.columns = columns
    return dataframe

def many_to_one(df, index_columns):
    many_one_index = 'index'
    index_values = list(zip(*[df[col] for col in index_columns]))
    df[many_one_index] = pd.factorize(index_values)[0]
    many_to_one_relation = df[index_columns]
    many_to_one_relation[many_one_index] = df[many_one_index]
    df = df.drop(columns=index_columns)
    df = df.set_index(many_one_index)
    return df, many_to_one_relation
