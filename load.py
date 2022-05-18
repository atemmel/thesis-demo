import joblib
import numpy as np
import preprocess
import pandas as pd
import const

from sklearn.preprocessing import OneHotEncoder

NOMINAL_COLS = [
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

NUMERIC_COLS = [
    "time_in_hospital",
    "num_lab_procedures",
    "num_procedures",
    "num_medications",
    "number_outpatient",
    "number_emergency",
    "number_inpatient",
    "number_diagnoses",
]


def load_model_data() -> dict:
    x_enc, y_enc = preprocess.make_encoders_v3()
    return {
        "clf": joblib.load(const.MODEL_PATH),
        "x_nominal_encoder": x_enc,
        "y_encoder": y_enc,
    }

def do_prediction(obj: dict, admission_info: dict) -> dict:
    x_nominal_encoder = obj["x_nominal_encoder"]
    y_encoder = obj["y_encoder"]

    nominal = pd.DataFrame([
        [admission_info[col] for col in NOMINAL_COLS],
    ], columns=NOMINAL_COLS)

    numeric = pd.DataFrame([
        [admission_info[col] for col in NUMERIC_COLS],
    ], columns=NUMERIC_COLS)

    clf = obj["clf"]
    x_nominal_encoder = obj["x_nominal_encoder"]
    y_encoder = obj["y_encoder"]

    x_encoded = x_nominal_encoder.transform(nominal).toarray()
    x_numeric = np.array(numeric)
    x_merged = np.hstack((x_encoded, x_numeric))

    pred = clf.predict(x_merged)
    prob = clf.predict_proba(x_merged)[0]

    confidence = prob[pred[0]];

    return {
        "prediction": y_encoder.inverse_transform(pred)[0],
        "confidence": confidence,
    }
