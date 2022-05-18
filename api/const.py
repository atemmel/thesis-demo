# const: various constants used throughout

FULL_DATASET_PATH: str = "./../data/diabetes/diabetic_data.csv"
DATASET_PATH: str = "./../datasets/ds2_train.csv"
FINAL_DATASET_PATH: str = "./../datasets/ds2_finish.csv"

DATASET_ID_MAPPING_PATH: str = "./../data/diabetes/IDs_mapping.csv"

PLOTS_PATH: str = "./../plots/"
TEX_TABLES_PATH: str = "./../report/appendices/dataset_tables.tex"

BLACKLISTED_COLUMNS: list[str] = [
    "encounter_id",
    "patient_nbr",
]

TEX_BLACKLISTED_COLUMNS: list[str] = [
    "diag_1", 
    "diag_2", 
    "diag_3",
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
