# const: various constants used throughout

FULL_DATASET_PATH: str = "./data/diabetic_data.csv"
MODEL_PATH = "data/model_2022-05-17 20:09:06.651002.dat"

BLACKLISTED_COLUMNS: list[str] = [
    "encounter_id",
    "patient_nbr",
]

# These all have a 100% belonging into one of their available categories
TRAIN_EVAL_BLACKLISTED_COLUMNS: list[str] = [
    "citoglipton",
    "examide",
]
