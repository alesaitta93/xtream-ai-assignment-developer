import os
import pandas as pd
import pickle
import optuna
import xgboost
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
from datetime import datetime
from functools import partial

OUT_DIR = os.path.join(os.getcwd(), "models")
MODEL_INDEX_FILENAME = "models.csv"

# Model indipendent utilities

def train_n_evaluate_model(model, x_train, x_test, y_train, y_test):

    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    r2 = r2_score(y_test, pred)
    mae = mean_absolute_error(y_test, pred)

    return model, r2, mae

def save_model(model, r2, mae, csv_model_index_filename=MODEL_INDEX_FILENAME, out_dir=OUT_DIR):

    model_name = "{}_{}".format(type(model).__name__, datetime.now().strftime("%m_%d_%Y__%H_%M_%S"))
    new_row_data = [{
        "model_name": model_name,
        "r2": r2,
        "mae": mae
    }]

    # output directory verification
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    # model pickle save
    model_file_name = "{}.pkl".format(model_name)
    model_file_path = os.path.join(out_dir, model_file_name)
    pickle.dump(model, open(model_file_path, "wb"))

    # csv index update
    new_row_df = pd.DataFrame(data=new_row_data)
    new_row_df.reset_index(drop=True, inplace=True)
    new_row_df.set_index(["model_name"], inplace=True)
    model_index_path = os.path.join(out_dir, csv_model_index_filename)
    if os.path.isfile(model_index_path):
        model_df = pd.read_csv(model_index_path).reset_index(drop=True)
        model_df.set_index(["model_name"], inplace=True)
        out_df = pd.concat([model_df, new_row_df])
    else:
        out_df = new_row_df

    out_df.to_csv(model_index_path)

# Linear regression utilities

def data_preparation_for_linear_regression(path, test_size=0.2, random_state=42):

    diamonds = pd.read_csv(path)
    # Dropping features with low correlation with the label(price)
    diamonds_processed = diamonds.drop(columns=['depth', 'table', 'y', 'z'])
    # Data encoding
    diamonds_dummy = pd.get_dummies(diamonds_processed, columns=['cut', 'color', 'clarity'], drop_first=True)
    # Training set and test set creation
    x = diamonds_dummy.drop(columns='price')
    y = diamonds_dummy.price

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=random_state)
    return x_train, x_test, y_train, y_test


def train_n_evaluate_linear_model(path):
    x_train, x_test, y_train, y_test = data_preparation_for_linear_regression(path)
    return train_n_evaluate_model(LinearRegression(), x_train, x_test, y_train, y_test)


def train_n_save_linear_model(path):
    model, r2, mae = train_n_evaluate_linear_model(path)
    save_model(model, r2, mae)

# xgboost utilities

def data_preparation_for_xgb(path, test_size=0.2, random_state=42):
    diamonds = pd.read_csv(path)
    diamonds_processed_xgb = diamonds.copy()
    diamonds_processed_xgb['cut'] = pd.Categorical(diamonds_processed_xgb['cut'],
                                                   categories=['Fair', 'Good', 'Very Good', 'Ideal', 'Premium'],
                                                   ordered=True)
    diamonds_processed_xgb['color'] = pd.Categorical(diamonds_processed_xgb['color'],
                                                     categories=['D', 'E', 'F', 'G', 'H', 'I', 'J'], ordered=True)
    diamonds_processed_xgb['clarity'] = pd.Categorical(diamonds_processed_xgb['clarity'],
                                                       categories=['IF', 'VVS1', 'VVS2', 'VS1', 'VS2', 'SI1', 'SI2',
                                                                   'I1'], ordered=True)
    x_train_xbg, x_test_xbg, y_train_xbg, y_test_xbg = train_test_split(diamonds_processed_xgb.drop(columns='price'),
                                                                        diamonds_processed_xgb['price'],
                                                                        test_size=test_size,
                                                                        random_state=random_state)
    return x_train_xbg, x_test_xbg, y_train_xbg, y_test_xbg


def objective(x_train_xbg, y_train_xbg, trial: optuna.trial.Trial) -> float:
    # Define hyperparameters to tune
    param = {
        'lambda': trial.suggest_float('lambda', 1e-8, 1.0, log=True),
        'alpha': trial.suggest_float('alpha', 1e-8, 1.0, log=True),
        'colsample_bytree': trial.suggest_categorical('colsample_bytree', [0.3, 0.4, 0.5, 0.7]),
        'subsample': trial.suggest_categorical('subsample', [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]),
        'learning_rate': trial.suggest_float('learning_rate', 1e-8, 1.0, log=True),
        'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
        'max_depth': trial.suggest_int('max_depth', 3, 9),
        'random_state': 42,
        'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
        'enable_categorical': True
    }

    # Split the training data into training and validation sets
    x_train, x_val, y_train, y_val = train_test_split(x_train_xbg, y_train_xbg, test_size=0.2, random_state=42)

    # Train the model
    model = xgboost.XGBRegressor(**param)
    model.fit(x_train, y_train)

    # Make predictions
    preds = model.predict(x_val)

    # Calculate MAE
    mae = mean_absolute_error(y_val, preds)

    return mae

def optimize_xgboost_params(x_train_xgb, y_train_xgb):
    study = optuna.create_study(direction='minimize', study_name='Diamonds XGBoost')
    objective_f = partial(objective, x_train_xgb, y_train_xgb)
    study.optimize(objective_f, n_trials=100)
    return study.best_params


def optimize_train_n_evaluate_xgboost(path):
    x_train_xbg, x_test_xbg, y_train_xbg, y_test_xbg = data_preparation_for_xgb(path)
    params = optimize_xgboost_params(x_train_xbg, y_train_xbg)
    model = xgboost.XGBRegressor(**params, enable_categorical=True, random_state=42)
    return train_n_evaluate_model(model, x_train_xbg, x_test_xbg, y_train_xbg, y_test_xbg)

def train_n_save_xgb_model(path):
    model, r2, mae = optimize_train_n_evaluate_xgboost(path)
    save_model(model, r2, mae)


