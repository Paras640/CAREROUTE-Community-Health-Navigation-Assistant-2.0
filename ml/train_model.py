import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR.parent / "Final_Augmented_dataset_Diseases_and_Symptoms.csv"


def load_data(filepath=DATASET_PATH):
    print(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    return df


def train_model():
    print("Starting Decision Tree model training pipeline...")

    # 1. Load Data
    if not DATASET_PATH.is_file():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}. "
            "Place the CSV in the repository root before training."
        )
    df = load_data()

    # 2. Preprocess Data
    print("Preprocessing data...")
    # Target column is 'diseases'
    target_col = 'diseases'

    # Separate features and target
    X = df.drop(columns=[target_col])
    y_raw = df[target_col]

    # Encode target labels
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y_raw)

    # Save the feature names exactly as they appear during training
    feature_names = list(X.columns)

    # 3. Train/Test Split
    print("Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. Initialize and train Decision Tree
    # Decision tree is fast and interpretible
    dt_model = DecisionTreeClassifier(random_state=42)
    print("Training Decision Tree Classifier...")
    dt_model.fit(X_train, y_train)

    # 5. Evaluate
    print("Evaluating model...")
    from sklearn.metrics import accuracy_score
    predictions = dt_model.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    print("\nModel Evaluation:")
    print(f"Accuracy: {acc * 100:.2f}%")

    # 6. Save model and artifacts
    print("Saving artifacts to the ml/ folder...")
    joblib.dump(dt_model, BASE_DIR / 'model.pkl')
    joblib.dump(label_encoder, BASE_DIR / 'label_encoder.pkl')
    joblib.dump(feature_names, BASE_DIR / 'feature_names.pkl')
    print("Saved model.pkl, label_encoder.pkl, and feature_names.pkl!")


if __name__ == "__main__":
    train_model()
