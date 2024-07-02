from challenge.pipeline.training_pipeline import train_n_save_linear_model, train_n_save_xgb_model

CSV_PATH =\
    "https://raw.githubusercontent.com/xtreamsrl/xtream-ai-assignment-engineer/main/datasets/diamonds/diamonds.csv"

if __name__ == '__main__':
    train_n_save_linear_model(CSV_PATH)
    train_n_save_xgb_model(CSV_PATH)
