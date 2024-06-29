from challenge.ml_pipeline import data_preparation_for_linear_regression

CSV_PATH =\
    "https://raw.githubusercontent.com/xtreamsrl/xtream-ai-assignment-engineer/main/datasets/diamonds/diamonds.csv"

if __name__ == '__main__':
    x_train, x_test, y_train, y_test = data_preparation_for_linear_regression(CSV_PATH)