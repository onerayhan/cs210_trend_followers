import re
import ast
import matplotlib.pyplot as plt
from datetime import datetime
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

# Sort data by Date
sorted_data = sorted(data, key=lambda x: datetime.strptime(x['Date'], '%d.%m.%Y'))

# Calculate the total points for each Source category
source_points = {}
source_directions = {}
for item in sorted_data:
    source = item['Source']
    point = item['point']
    direction = item['direction']
    if source in source_points:
        source_points[source] += point
        source_directions[source] += direction
    else:
        source_points[source] = point
        source_directions[source] = direction

# Plot the points by Source category
sources = source_points.keys()
points = source_points.values()
directions = source_directions.values()

colors = ['blue', 'green', 'red']  # Specify the colors for each bar

plt.bar(sources, points, color=colors)  # Use colors for the bars
plt.xlabel('Source')
plt.ylabel('Total Points')
plt.title('Total Points by Source Category')
plt.show()

plt.bar(sources, directions, color=colors)  # Use colors for the bars
plt.xlabel('Source')
plt.ylabel('Total Direction')
plt.title('Total Direction by Source Category')
plt.show()

# Plot for each source
for source in sources:
    # Filter data for the current source
    source_data = [item for item in sorted_data if item['Source'] == source]

    # Filter data within the specified date range
    filtered_data = [item for item in source_data if datetime(2023, 1, 1) <= datetime.strptime(item['Date'], '%d.%m.%Y') <= datetime(2023, 4, 28)]

    # Extract dates, points, and directions for the current source
    dates = [item['Date'] for item in filtered_data]
    points = [item['point'] for item in filtered_data]
    directions = [item['direction'] for item in filtered_data]

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
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from matplotlib import cm

# Convert date strings to datetime objects
for item in data:
    item['Date'] = datetime.strptime(item['Date'], '%d.%m.%Y').date()

# Sort data by Date
sorted_data = sorted(data, key=lambda x: x['Date'])

# Define the sources
sources = ['akbank', 'yapikredi', 'gedik', 'garanti', 'haberler']

# Create a colormap for sources
colors = cm.get_cmap('tab10', len(sources))

# Create a figure
fig, ax1 = plt.subplots(figsize=(10, 6))
ax2 = ax1.twinx()

# Plot for each source
for i, source in enumerate(sources):
    # Filter data for the current source
    source_data = [item for item in sorted_data if item['Source'] == source]

    # Filter data within the specified date range
    filtered_data = [item for item in source_data if datetime(2023, 1, 1).date() <= item['Date'] <= datetime(2023, 4, 28).date()]

    # Extract dates, points, and directions for the current source
    dates = [item['Date'] for item in filtered_data]
    points = [item['point'] for item in filtered_data]
    directions = [item['direction'] for item in filtered_data]

    # Calculate cumulative points and directions
    cumulative_points = [sum(points[:j+1]) for j in range(len(points))]
    cumulative_directions = [sum(directions[:j+1]) for j in range(len(directions))]

    # Plot the cumulative points
    ax1.plot(dates, cumulative_points, marker='o', label=f'{source} - Points', color=colors(i))
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Cumulative Points')
    ax1.set_title('Cumulative Points for All Sources')



# Show the legends
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.show()

# Create a colorbar for the sources
fig, ax = plt.subplots(figsize=(6, 1))
fig.subplots_adjust(bottom=0.5)
cmap = cm.get_cmap('tab10', len(sources))
norm = plt.Normalize(vmin=0, vmax=len(sources) - 1)
cb = plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap),
                  cax=ax, orientation='horizontal', ticks=np.arange(len(sources)))
cb.set_label('Sources')
cb.set_ticklabels(sources)
plt.show()


