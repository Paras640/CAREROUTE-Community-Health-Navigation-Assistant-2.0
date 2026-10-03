# CareRoute Python API

CareRoute is a Python-only FastAPI service for disease prediction from symptom
indicators. It no longer includes or requires a Next.js frontend.

## Requirements

- Python 3.10 or newer
- The training dataset
  `Final_Augmented_dataset_Diseases_and_Symptoms.csv` in the repository root

The dataset and generated model files are not committed to this repository.
The dataset is ignored by Git, and the generated model artifacts are too large
to include. Obtain the dataset separately before training.

## Setup

From the repository root, create and activate a virtual environment, then
install the Python dependencies:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Train the model and create its local artifacts:

```powershell
python ml\train_model.py
```

This creates `ml\model.pkl`, `ml\label_encoder.pkl`, and
`ml\feature_names.pkl`. These files are ignored by Git and must be generated
again on each machine.

Start the API:

```powershell
python -m uvicorn ml.api:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/docs` for interactive API documentation.

## API

- `GET /` reports that the service is running.
- `POST /predict` accepts a JSON object whose keys are symptom feature names
  from the training dataset and whose values are `1` (present) or `0` (absent).
  Unspecified features are treated as absent.

Example:

```json
{
  "headache": 1,
  "fever": 1
}
```

The response contains the predicted disease label and the number of submitted
symptoms that matched model features. Prediction is only available after the
model artifacts have been generated.

This service provides informational predictions, not a medical diagnosis or
substitute for professional care. Seek emergency help for urgent symptoms.
