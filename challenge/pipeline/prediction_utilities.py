import os
import json
import pandas as pd
import pickle
from sklearn.neighbors import NearestNeighbors
from challenge.pipeline.training_pipeline import OUT_DIR

def choose_model_from_df(path):
    df = pd.read_csv(path)
    min_mae_row = df.loc[df['mae'].idxmin()]
    return min_mae_row

def construct_input_df(data):
    out_dict = {}
    dummy_cols_filename = "dummyfied_data_columns.json"
    dummy_cols_path = os.path.join(OUT_DIR, dummy_cols_filename)
    with open(dummy_cols_path, "r") as input_file:
        columns = json.load(input_file)["dummy_columns"]
    for col in columns:
        if any(s in col for s in ['cut', 'color', 'clarity']):
            col_name_split = col.split("_")
            out_dict[col] = col_name_split[1] == data[col_name_split[0]]
        elif col != "price":
            out_dict[col] = float(data[col])
    return pd.DataFrame(data=[out_dict])


def predict_with_minimum_mae_model(data):
    min_mae_row = choose_model_from_df(os.path.join(OUT_DIR, "models.csv"))
    model_name = min_mae_row["model_name"]
    x = construct_input_df(data)
    model_path = os.path.join(OUT_DIR, "{}.pkl".format(model_name))
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
        prediction = model.predict(x)
    return str(prediction[0])

