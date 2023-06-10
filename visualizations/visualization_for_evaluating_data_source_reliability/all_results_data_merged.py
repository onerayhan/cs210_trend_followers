import json

# Load data from results_data.jsons
with open('results_data.json', 'r') as json_file:
    results_data = json.load(json_file)

# Load data from tumsonuçlar.txt
with open('tumsonuçlar.txt', 'r') as txt_file:
    tumsonuclar_data = txt_file.readlines()

# Parse the dictionaries in tumsonuçlar.txt
parsed_tumsonuclar = []
for line in tumsonuclar_data:
    if line.strip() == '--------------------':
        continue  # Skip the separator line
    dictionary = eval(line)  # Safely evaluate the string as a dictionary
    parsed_tumsonuclar.append(dictionary)

# Update the dictionaries with the predicted values
for result in results_data:
    file_name = result['File Name']
    predicted_value = result['Predicted Value']
    for dictionary in parsed_tumsonuclar:
        if dictionary['File Name'] == file_name:
            dictionary['Predicted Value'] = predicted_value
            break

# Write the updated dictionaries to tumsonuçlar.txt
with open('tumsonuçlar.txt', 'w') as txt_file:
    for dictionary in parsed_tumsonuclar:
        txt_file.write(str(dictionary) + '\n')
