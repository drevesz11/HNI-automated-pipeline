import csv
import os

# Define the range of cells to multiply (e.g., A1 to C10)
start_row = 1  # Replace with the actual start row index
end_row = 150  # Replace with the actual end row index
start_col = 1  # Replace with the actual start column index
end_col = 117  # Replace with the actual end column index

# Original file path and name
original_file = '/home/drevesz/Desktop/Random_Forest/Training_test_validation_data/training_data_encoded.csv'

# Output directory and new file name
output_dir = os.path.dirname(original_file)
new_filename = 'volupdated_training_data_encoded.csv'

# Open the CSV file for reading and writing
with open(original_file, 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)

    # Iterate over the specified range of cells
    for row in rows[start_row:end_row + 1]:
        for i in range(start_col, end_col + 1):
            # Check if the cell is not empty
            if row[i] != '':
                # Multiply each non-empty cell value by 1.2
                cell_value = float(row[i])  # Convert to float if necessary
                updated_value = cell_value * 1.2
                row[i] = updated_value

# Write the updated values to the new file
output_file = os.path.join(output_dir, new_filename)
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)

print("Multiplication complete. Output file:", output_file)