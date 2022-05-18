# const: various constants used throughout

FULL_DATASET_PATH: str = "./data/diabetic_data.csv"

BLACKLISTED_COLUMNS: list[str] = [
    "encounter_id",
    "patient_nbr",
]

# These all have a 100% belonging into one of their available categories
TRAIN_EVAL_BLACKLISTED_COLUMNS: list[str] = [
    "citoglipton",
    "examide",
]

# only used if not using k-fold
TEST_SIZE_FACTOR: float = 0.1

RANDOM_STATE: int = 32

#K_FOLD_SPLITS: int = 1
K_FOLD_SPLITS: int = 10
#K_FOLD_SPLITS: int = 100
