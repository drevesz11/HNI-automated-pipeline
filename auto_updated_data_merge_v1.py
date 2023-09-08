import pandas as pd

# File paths
neuroanatomical_file = '/home/drevesz/Desktop/Random_Forest/RF_feature_selection_automated/neuro_auto_intensity_counts.csv'
clinical_file = '/home/drevesz/Desktop/Random_Forest/RF_manualsegmentation/data_clinical_ax2000.xls'
output_file = '/home/drevesz/Desktop/Random_Forest/RF_feature_selection_automated/auto_merged_neuroclinicaldata.csv'

# Read neuroanatomical data
neuroanatomical_data = pd.read_csv(neuroanatomical_file)

# Read clinical data
clinical_data = pd.read_excel(clinical_file)

# Convert 'ID' column to string in both dataframes
neuroanatomical_data['ID'] = neuroanatomical_data['ID'].astype(str)
clinical_data['ID'] = clinical_data['ID'].astype(str)

# Merge data based on ID using inner join
merged_data = pd.merge(clinical_data, neuroanatomical_data, on='ID', how='inner')

# Save merged data to a new file
merged_data.to_csv(output_file, index=False)

print('Data merged successfully and saved to', output_file)

