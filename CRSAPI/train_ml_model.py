import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import sys
from pathlib import Path


def train_model(data_path, output_model_path):
    # Load the dataset
    dataset = pd.read_csv(data_path)
    print(f"Dataset loaded from {data_path}. Here are the first 5 rows:")
    print(dataset.head())

    # Split dataset into features and labels
    X = dataset.drop(columns='label')
    y = dataset['label']

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Initialize RandomForestClassifier
    model = RandomForestClassifier()

    # Hyperparameter tuning using GridSearchCV
    param_grid = {
        'n_estimators': [10, 50, 100],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }

    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
    grid_search.fit(X_train, y_train)

    # Best model after GridSearchCV
    best_model = grid_search.best_estimator_

    # Evaluate the model
    y_pred = best_model.predict(X_test)
    print("Classification Report:\n", classification_report(y_test, y_pred))
    print("Accuracy:", accuracy_score(y_test, y_pred))

    # Save the trained model
    joblib.dump(best_model, output_model_path)
    print(f"Model saved to {output_model_path}")


def validate_paths(data_path, output_model_path):
    # Check if input path is a valid file
    if not Path(data_path).is_file():
        print(f"Error: '{data_path}' is not a valid file path.")
        sys.exit(1)

    # Check if output path's parent directory exists
    output_parent = Path(output_model_path).parent
    if not output_parent.exists():
        print(f"Error: The directory '{output_parent}' for the output path does not exist.")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python train_model.py <data_path> <output_model_path>")
        sys.exit(1)

    # ask for input and output paths
    print("Enter the path of the dataset file:")
    input_path = input()
    print("Enter the path of the output model file:")
    output_path = input()

    # check if input and output paths are valid paths
    if not Path(input_path).is_file():
        print(f"Error: {input_path} is not a valid file path")
        sys.exit(1)

    if not Path(output_path).parent.exists():
        print(f"Error: {output_path} is not a valid output path")
        sys.exit(1)

    # train the model
    train_model(input_path, output_path)
