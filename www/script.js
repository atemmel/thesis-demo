const API_URL = "http://127.0.0.1:5000/predict" 

const getFormRaw = () => {
	const get = (name) => {
		return document.getElementById(name).value;
	};
	
	return {
		race: get("race"),
		gender: get("gender"),
		age: get("age"),
		weight: get("weight"),
		admission_type_id: get("admission_type_id"),
		discharge_disposition_id: get("discharge_disposition_id"),
		admission_source_id: get("admission_source_id"),
		payer_code: get("payer_code"),
		medical_specialty: get("medical_specialty"),
		diag_1: get("diag_1"),
		diag_2: get("diag_2"),
		diag_3: get("diag_3"),
		time_in_hospital: get("time_in_hospital"),
		num_lab_procedures: get("num_lab_procedures"),
		num_procedures: get("num_procedures"),
		num_medications: get("num_medications"),
		number_outpatient: get("number_outpatient"),
		number_emergency: get("number_emergency"),
		number_inpatient: get("number_inpatient"),
		number_diagnoses: get("number_diagnoses"),
	};
};

const processAge = (age) => {
	const within = (max, min, value) => value < max && value >= min;

	const ranges = {
		"[0-10)": {
			max: 10,
			min: 0,
		},
		"[10-20)": {
			max: 20,
			min: 10,
		},
		"[20-30)": {
			max: 30,
			min: 20,
		},
		"[30-40)": {
			max: 40,
			min: 30,
		},
		"[40-50)": {
			max: 50,
			min: 40,
		},
		"[50-60)": {
			max: 60,
			min: 50,
		},
		"[70-80)": {
			max: 80,
			min: 70,
		},
		"[90-100)": {
			max: 100,
			min: 90,
		},
	};


	for (const [key, value] of Object.entries(ranges)) {
		if(within(value.max, value.min, age)) {
			return key;
		}
	}

	return "[90-100)";
};

const processWeight = (weight) => {
	const within = (max, min, value) => value < max && value >= min;

	const ranges = {
		">200": {
			max: Math.Inf,
			min: 200,
		},
		"[0-25)": {
			max: 25,
			min: 0,
		},
		"[100-125)": {
			max: 125,
			min: 100,
		},
		"[125-150)": {
			max: 150,
			min: 125,
		},
		"[150-175)": {
			max: 175,
			min: 150,
		},
		"[25-50)": {
			max: 50,
			min: 25,
		},
		"[50-75)": {
			max: 75,
			min: 50,
		},
		"[75-100)": {
			max: 100,
			min: 75,
		},
	};

	for (const [key, value] of Object.entries(ranges)) {
		if(within(value.max, value.min, weight)) {
			return key;
		}
	}

	return "?";
};

const formatFormData = (formData) => {
	const tryInt = (p) => parseInt(p) || p;
	var f = formData;
	f.age = processAge(f.age);
	f.weight = processWeight(f.weight);
	f.admission_type_id = tryInt(f.admission_type_id);
	f.discharge_disposition_id = tryInt(f.discharge_disposition_id);
	f.admission_source_id = tryInt(f.admission_source_id);
	return f;
};

const getForm = () => {
	return formatFormData(getFormRaw());
};

const sendPatient = (patient) => {
	postData(API_URL, {patient: patient})
		.then(result => {
			var predResult = document.getElementById("prediction-result");
			var confResult = document.getElementById("confidence-result");
			predResult.innerHTML = "Prediction: <span id='prediction-inner'>" + result.prediction + "</span>";
			confResult.innerHTML = "Confidence: " + result.confidence;

			var predInner = document.getElementById("prediction-inner");
			if(result.prediction === "EARLY READMISSION") {
				predInner.style.background = "#F00";	// bad
			} else {
				predInner.style.background = "#0F0";	// good
			}
		});
};

async function postData(url, data) {
	const response = await fetch(url, {
		method: "POST",
		//mode: 'cors',
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify(data),
	});
	return response.json();
}

const doPrediction = () => {
	const patient = getForm();
	sendPatient(patient);
};
