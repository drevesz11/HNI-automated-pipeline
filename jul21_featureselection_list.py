import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
import optuna

# File paths    
data_file = '/home/drevesz/Desktop/Random_Forest/RF_final_july18/feature_selection_data/training_data.csv'
labels_file = '/home/drevesz/Desktop/Random_Forest/RF_final_july18/feature_selection_data/training_labels.csv'

# Headers to extract
headers_to_extract = [
    '51', '52', '53', '54', '101', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112',
    '113', '114', '115', '116', '117', '118', '119', '120', '121', '122', '123', '124', '125', '126', '127', '128',
    '129', '130', '131', '132', '133', '134', '135', '136', '137', '138', '139', '140', '141', '142', '143', '144',
    '201', '202', '203', '204', '205', '206', '207', '208', '209', '210', '211', '212', '213', '214', '215', '216',
    '217', '218', '219', '220', '221', '222', '223', '224', '225', '226', '227', '228', '229', '230', '231', '232',
    '233', '234', '235', '236', '237', '238', '239', '240', '241', '242', '243', '244', '301', '302', '303', '304',
    '305', '306', '307', '308', '309', '310', '311', '312', '401', '402', '403', '404', '405', '406', '407', '408',
    '409', '410', '411', '412'
]

# Load the neuroanatomical data
data = pd.read_csv(data_file, usecols=headers_to_extract)

# Load the mRS labels
labels = pd.read_csv(labels_file, usecols=[1])['mRS_score_at_Day_90_(LOCF)']
labels = labels.apply(lambda x: 1 if x > 2 else 0)  # Dichotomize the outcome to either good outcome mRS <= 2 or poor outcome > 2

# Merge the data and labels based on the index
merged_data = data.merge(labels, left_index=True, right_index=True)

# Extract the mRS labels
labels = merged_data['mRS_score_at_Day_90_(LOCF)']

# Extract the features
features = merged_data.iloc[:, :-1]  # Exclude the target variable

# Define the objective function for Optuna optimization
def objective(trial):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 500),
        'max_depth': trial.suggest_int('max_depth', 5, 15),
        'min_samples_split': trial.suggest_int('min_samples_split', 2, 10),
        'random_state': 42
    }

    # Create the random forest classifier
    rf = RandomForestClassifier(**params)

    # Perform cross-validation
    scores = cross_val_score(rf, features, labels, cv=5, scoring='accuracy')

    return scores.mean()

# Create an Optuna study
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)

# Get the best parameters and best score
best_params = study.best_params
best_score = study.best_value

print("Best Parameters:")
print(best_params)
print("Best Score:")
print(best_score)

# Create the random forest classifier with the best parameters
rf_final = RandomForestClassifier(**best_params)

# Fit the final model on the full training data
rf_final.fit(features, labels)

# Get the feature importance scores
importance_scores = rf_final.feature_importances_

# Associate importance scores with headers
header_importance = dict(zip(headers_to_extract, importance_scores))

# Sort headers based on importance scores
sorted_headers = sorted(header_importance, key=header_importance.get, reverse=True)

# Feature selection - Print relative importance and rank order for each header
print("Feature Importance:")
for i, header in enumerate(sorted_headers):
    importance_score = header_importance[header]
    rank = i + 1
    print(f"Rank {rank}: Header {header} (Importance Score: {importance_score})")

# Save feature selection results to CSV file
output_file = '/home/drevesz/Desktop/Random_Forest/RF_final_july18/feature_selection_data/feature_selection_results.csv'

# Create a list to store the feature selection results
feature_selection_results = []

# Iterate through the sorted headers and save the results to the list
for i, header in enumerate(sorted_headers):
    importance_score = header_importance[header]
    rank = i + 1
    feature_selection_results.append([rank, header, importance_score])

# Convert the list to a DataFrame
feature_selection_df = pd.DataFrame(feature_selection_results, columns=['Rank', 'Header', 'Importance Score'])

# Save the DataFrame to a CSV file
feature_selection_df.to_csv(output_file, index=False)

# Print a message indicating the feature selection results have been saved
print("Feature selection results saved to:", output_file)
