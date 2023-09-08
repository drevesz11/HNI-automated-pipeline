import pandas as pd

# Read the CSV file
input_file = '/home/drevesz/Desktop/Random_Forest/intensity_counts_trial5.csv'
data = pd.read_csv(input_file)

# Remove 'Subject' prefix from the first column
data['SubjectID'] = data['SubjectID'].str.replace('Subject', '')

# Convert the first column to numeric
data['SubjectID'] = pd.to_numeric(data['SubjectID'], errors='coerce')

# Save the modified data to a new CSV file
output_file = '/home/drevesz/Desktop/Random_Forest/intensity_counts_trial5_modified.csv'
data.to_csv(output_file, index=False)

print("Prefix 'Subject' removed from the first column.")
print("Modified data saved to:", output_file)
