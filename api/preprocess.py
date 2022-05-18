# preprocess: preprocess dataframe(s)

import const
import misc
import numpy as np
import pandas as pd

from sklearn.preprocessing import OneHotEncoder, LabelBinarizer
from scipy.sparse import bsr_array

# creates dict object describing statisitcs relevant to a dataframe column
def create_column_info_dict(column: pd.DataFrame, id_mapping: dict) -> dict:
    is_numerical = pd.api.types.is_numeric_dtype(column) and not column.name.endswith("id")
    if is_numerical:
        return {
            "name": column.name,
            "type": "numerical",
            "max": column.max(),
            "min": column.min(),
            "mean": column.mean(),
            "std": column.std(),
        }

    is_nominal_id = column.name.endswith("id")
    is_nominal = pd.api.types.is_string_dtype(column) or is_nominal_id
    if is_nominal:
        counts: pd.Series = pd.Series(column.value_counts())
        freqs: pd.Series = pd.Series(column.value_counts(normalize=True))
        values = list()
        for category, count in counts.items():
            freq = freqs[category]
            if is_nominal_id:
                values.append({
                    "value": id_mapping[column.name][category],
                    "id": category,
                    "count": count,
                    "normalized_count": freq,
                })
            else:
                values.append({
                    "value": category,
                    "count": count,
                    "normalized_count": freq,
                })

        values.sort(key=lambda x: "" if x["value"] == None else x["value"])

        return {
            "name": column.name,
            "type": "nominal",
            "values": values,
        }

    # was neither, which is bad :(
    assert(False) ; pass

# removes specified columns from dataframe
def filter_df(df: pd.DataFrame, columns_to_exclude: list[str]) -> pd.DataFrame:
    return pd.DataFrame(df.drop(columns=columns_to_exclude))

# performs lavel-attribute split of a dataframe
def x_y_split(df: pd.DataFrame):
    _, w = df.shape
    x = df.iloc[:, 0:w - 1]
    y = df.iloc[:, w - 1].values.reshape(1, -1).transpose()
    return x, y

def crop_y_to_binary(y: pd.Series):
    y[y == "<30"] = "EARLY READMISSION"
    y[y == ">30"] = "NO EARLY READMISSION"
    y[y == "NO"] = "NO EARLY READMISSION"
    return y

def make_dataset(df: pd.DataFrame, version):
    if version == 1:
        return make_dataset_v1(df)
    if version == 2:
        return make_dataset_v2(df)
    if version == 3:
        return make_dataset_v3(df)
    return None

def make_encoders_v3() -> tuple[OneHotEncoder, LabelBinarizer]:
    df = misc.make_df(const.FULL_DATASET_PATH)
    x, y = x_y_split(df)
    y = crop_y_to_binary(y)
    nominal_cols = [
        "race",
        "gender",
        "age",
        "weight",
        "admission_type_id",
        "discharge_disposition_id",
        "admission_source_id",
        "payer_code",
        "medical_specialty",
        "diag_1",
        "diag_2",
        "diag_3",
    ]
    x_nominal = x[nominal_cols];
    x_nominal_encoder = OneHotEncoder()
    y_encoder = LabelBinarizer()
    x_nominal_encoder.fit(x_nominal)
    y_encoder.fit(y)
    return x_nominal_encoder, y_encoder

    

def make_dataset_v1(df: pd.DataFrame):
    x_encoder = OneHotEncoder()
    y_encoder = LabelBinarizer()
    x, y = x_y_split(df)
    y = crop_y_to_binary(y)

    attr_info = misc.import_json("./attr_info.json")
    nominal = [s["name"] for s in attr_info if s["type"] == "nominal" and s["name"] in x.columns]
    numeric = [s["name"] for s in attr_info if s["type"] == "numerical" and s["name"] in x.columns]
    nominal_indicies = [i for i in range(len(nominal))]
    x_nominal = x[nominal]
    x_numeric = np.array(x[numeric])
    x_encoded = x_encoder.fit_transform(x_nominal).toarray()
    y_encoded = y_encoder.fit_transform(y)

    x_merged = np.hstack((x_encoded, x_numeric))

    return {
        "x": x_merged,
        "y": y_encoded,
        "x_nominal_indicies": nominal_indicies,
        "x_nominal_encoder": x_encoder,
        "y_encoder": y_encoder,
        "version": 1,
    }

def make_dataset_v2(df: pd.DataFrame):
    df = misc.make_df("../datasets/ds2_train.csv")
    x_encoder = OneHotEncoder()
    y_encoder = OneHotEncoder()
    x, y = x_y_split(df)

    attr_info = misc.import_json("./attr_info.json")
    nominal = [s["name"] for s in attr_info if s["type"] == "nominal" and s["name"] in x.columns]
    numeric = [s["name"] for s in attr_info if s["type"] == "numerical" and s["name"] in x.columns]
    nominal_indicies = [i for i in range(len(nominal))]
    x_nominal = x[nominal]
    x_numeric = np.array(x[numeric])
    x_encoded = x_encoder.fit_transform(x_nominal).toarray()

    x_merged = np.hstack((x_encoded, x_numeric))

    return {
        "x": bsr_array(x_merged).todense(),
        #"y": bsr_array(y[0]).todense(),
        "y": y,
        "x_nominal_indicies": nominal_indicies,
        "x_nominal_encoder": x_encoder,
        "y_encoder": y_encoder,
        "version": 2,
    }

def make_dataset_v3(df: pd.DataFrame):

    discard = [
        "max_glu_serum",
        "A1Cresult",
        "metformin",
        "repaglinide",
        "nateglinide",
        "chlorpropamide",
        "glimepiride",
        "acetohexamide",
        "glipizide",
        "glyburide",
        "tolbutamide",
        "pioglitazone",
        "rosiglitazone",
        "acarbose",
        "miglitol",
        "troglitazone",
        "tolazamide",
        "insulin",
        "glyburide-metformin",
        "glipizide-metformin",
        "glimepiride-pioglitazone",
        "metformin-rosiglitazone",
        "metformin-pioglitazone",
        "change",
        "diabetesMed",
    ]

    x_encoder, y_encoder = make_encoders_v3()
    # filter here
    df = filter_df(df, discard)
    x, y = x_y_split(df)
    y = crop_y_to_binary(y)

    attr_info = misc.import_json("./attr_info.json")
    nominal = [s["name"] for s in attr_info if s["type"] == "nominal" and s["name"] in x.columns]
    numeric = [s["name"] for s in attr_info if s["type"] == "numerical" and s["name"] in x.columns]
    # filter here
    nominal = [n for n in nominal if n not in discard]
    nominal_indicies = [i for i in range(len(nominal))]
    x_nominal = x[nominal]
    x_numeric = np.array(x[numeric])
    x_encoded = x_encoder.transform(x_nominal).toarray()
    y_encoded = y_encoder.transform(y)

    x_merged = np.hstack((x_encoded, x_numeric))

    return {
        "x": x_merged,
        "y": y_encoded,
        "x_nominal_indicies": nominal_indicies,
        "x_nominal_encoder": x_encoder,
        "y_encoder": y_encoder,
        "version": 3,
    }
