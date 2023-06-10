import re
import ast
import matplotlib.pyplot as plt

file_path = 'tumsonuçlar.txt'  # Path to the file containing the example content

data = []
with open(file_path, 'r') as file:
    for line in file:
        dictionary = eval(line.strip())
        data.append(dictionary)

# Accessing the data
for item in data:
    file_name = item['File Name']
    folder = item['Folder']
    source = item['Source']
    date = item['Date']
    perf = item['Perf']
    predicted_value = item['Predicted Value']

    if predicted_value == 1 and perf > 0:
        item['direction'] = 1
        item['point'] = 1 * abs(perf)
    elif predicted_value == 1 and perf < 0:
        item['direction'] = -1
        item['point'] = -1 * abs(perf)
    elif predicted_value == 0 and perf < 0:
        item['direction'] = 1
        item['point'] = 1 * abs(perf)
    elif predicted_value == 0 and perf > 0:
        item['direction'] = -1
        item['point'] = -1 * abs(perf)

with open("pointlabel.txt", "w") as file:
    file.write(str(data))
import matplotlib.pyplot as plt


# Sort data by Date
sorted_data = sorted(data, key=lambda x: x['Date'])

# Calculate the total points for each Source category
source_points = {}
for item in sorted_data:
    source = item['Source']
    point = item['point']
    if source in source_points:
        source_points[source] += point
    else:
        source_points[source] = point
source_direction = {}
for item in sorted_data:
    source = item['Source']
    direction = item['direction']
    if source in source_direction:
        source_direction[source] += direction
    else:
        source_direction[source] = direction

# Plot the points by Source category
sources = source_points.keys()
points = source_points.values()
sourcesd = source_direction.keys()
directions = source_direction.values()

colors = ['blue', 'green', 'red']  # Specify the colors for each bar

plt.bar(sources, points, color=colors)  # Use colors for the bars
plt.xlabel('Source')
plt.ylabel('Total Points')
plt.title('Total Points by Source Category')
plt.show()


plt.bar(sourcesd, directions, color=colors)  # Use colors for the bars
plt.xlabel('Source')
plt.ylabel('Total Direction')
plt.title('Total Direction by Source Category')
plt.show()
import matplotlib.pyplot as plt
from datetime import datetime

# Convert date strings to datetime objects
for item in data:
    item['Date'] = datetime.strptime(item['Date'], '%d.%m.%Y')

# Sort data by Date
sorted_data = sorted(data, key=lambda x: x['Date'])

# Define the sources
sources = ['akbank', 'yapikredi', 'gedik', 'garanti', 'haberler']

# Plot for each source
for source in sources:
    # Filter data for the current source
    source_data = [item for item in sorted_data if item['Source'] == source]

    # Extract dates, points, and directions for the current source
    dates = [item['Date'] for item in source_data]
    points = [item['point'] for item in source_data]
    directions = [item['direction'] for item in source_data]

    # Calculate cumulative points and directions
    cumulative_points = [sum(points[:i+1]) for i in range(len(points))]
    cumulative_directions = [sum(directions[:i+1]) for i in range(len(directions))]

    # Plot the cumulative points
    plt.plot(dates, cumulative_points, marker='o', label='Cumulative Points')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Points')
    plt.title(f'Cumulative Points for {source}')
    plt.legend()

    # Set x-axis tick labels to show only the lowest and highest dates for the current source
    plt.xticks([dates[0], dates[-1]])

    plt.show()

    # Plot the cumulative directions
    plt.plot(dates, cumulative_directions, marker='o', label='Cumulative Direction')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Direction')
    plt.title(f'Cumulative Direction for {source}')
    plt.legend()

    # Set x-axis tick labels to show only the lowest and highest dates for the current source
    plt.xticks([dates[0], dates[-1]])

    plt.show()