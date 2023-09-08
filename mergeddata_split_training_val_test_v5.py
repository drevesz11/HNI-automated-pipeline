import pandas as pd
from sklearn.model_selection import train_test_split

# File paths
data_file = '/home/drevesz/Desktop/Random_Forest/merged_data.csv'
output_dir = '/home/drevesz/Desktop/Random_Forest/Training_test_validation_data'

# Load the merged data
data = pd.read_csv(data_file)

# Specify the target variable column name
target_variable_column_name = 'mRS_score_at_Day_90_(LOCF)'

# Split the data into training, validation, and test sets
train_data, remaining_data = train_test_split(data, train_size=0.7, random_state=42)
val_data, test_data = train_test_split(remaining_data, train_size=0.5, random_state=42)

# Separate the features and target variable
train_features = train_data.drop(columns=[target_variable_column_name])
val_features = val_data.drop(columns=[target_variable_column_name])
test_features = test_data.drop(columns=[target_variable_column_name])

train_labels = train_data[['ID', target_variable_column_name]]
val_labels = val_data[['ID', target_variable_column_name]]
test_labels = test_data[['ID', target_variable_column_name]]

# Remove rows with empty cells in 'ID' column
train_features = train_features.dropna(subset=['ID'])
train_labels = train_labels.dropna(subset=['ID'])
val_features = val_features.dropna(subset=['ID'])
val_labels = val_labels.dropna(subset=['ID'])
test_features = test_features.dropna(subset=['ID'])
test_labels = test_labels.dropna(subset=['ID'])

# Save the data and labels to separate CSV files
train_features.to_csv(output_dir + '/training_data.csv', index=False)
val_features.to_csv(output_dir + '/validation_data.csv', index=False)
test_features.to_csv(output_dir + '/test_data.csv', index=False)

train_labels.to_csv(output_dir + '/training_labels.csv', index=False)
val_labels.to_csv(output_dir + '/validation_labels.csv', index=False)
test_labels.to_csv(output_dir + '/test_labels.csv', index=False)

print('Data split into training, validation, and test sets successfully.')
