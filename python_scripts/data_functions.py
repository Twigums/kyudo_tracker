import numpy as np
import matplotlib.pyplot as plt

from matplotlib.patches import Circle
from sklearn.cluster import KMeans

colors = ["#6929c4", # purple 70
          "#1192e8", # cyan 50
          "#005d5d", # teal 70
          "#9f1853", # magenta 70
          "#fa4d56", # red 50
          "#570408", # red 90
          "#198038", # green 60
          "#002d9c", # blue 80
          "#ee538b", # magenta 50
          "#b28600", # yellow 50
          "#009d9a", # teal 50
          "#012749", # cyan 90
          "#8a3800", # orange 70
          "#a56eff", # purple 50
          ] # color blind friendly colors from ibm design (https://carbondesignsystem.com/data-visualization/color-palettes/)

# This function formats the data from a text file into a list of lists
def format_data(input_filename):
    with open(f"./data/txt/{input_filename}.txt", "r") as file:
        data = file.read().split("\n")

    formatted_data = []

    # use mapping to format data into a list and append
    for line in data:
        if line != "":
            line_data = line.split(", ")
            formatted_data.append(line_data)

    return formatted_data

# This function converts the formatted data into a dictionary
def make_dict(data, normalization_factor, trash_corner1, trash_corner2):
    data_dict = {} # empty dictionary

    # we normalize the data points to change pixel values into centimeters
    for point in data:
        set_value, x, y, arrow_idx = point
        set_value = int(set_value)
        x = int(x)
        y = int(y)
        arrow_idx = int(arrow_idx[-1]) - 1

        if x >= trash_corner1[0] and x <= trash_corner2[0] and y >= trash_corner1[1] and y <= trash_corner2[1]:
            continue

        if set_value not in data_dict:
            data_dict[set_value] = [[x * normalization_factor, y * normalization_factor, arrow_idx]]

        else:
            data_dict[set_value].append([x * normalization_factor, y * normalization_factor, arrow_idx])

    return data_dict

# gets euclidean distance
def calculate_distance(coord1, coord2):
    coord1 = np.array(coord1)
    coord2 = np.array(coord2)

    # definition of Euclidean distance
    dist = np.sqrt(np.sum((coord1 - coord2) ** 2))

    return dist

# plots arrows on x y with a transparent target
def plot_data(input_filename, dictionary, center, radius):
    fig, ax = plt.subplots() # Create a figure and a set of subplots

    # plot each set as a different opacity on the same plot
    for i in range(1, len(dictionary) + 1):
        coordinates = dictionary[i]

        x_values = [coord[0] for coord in coordinates]
        y_values = [coord[1] for coord in coordinates]
        color_idx = [coord[2] for coord in coordinates]

        # opacity is scaled for how many keys in the dictionary (how many sets)
        opacity = i / len(dictionary)

        # Plot the points with the calculated opacity
        for j in range(len(x_values)):
            x = x_values[j]
            y = y_values[j]
            color = colors[color_idx[j]]

            ax.scatter(x, y, alpha = opacity, color = color)

    # plot target
    circle = Circle(center, radius, fill = True, alpha = 0.2, color = colors[4])
    ax.add_patch(circle)

    # plot details
    x_center, y_center = center
    ax.set_xlabel("x [cm]")
    ax.set_ylabel("y [cm]")
    ax.set_title("Hits on Mato")
    ax.grid(False)
    ax.xaxis.set_ticks(np.arange(0, x_center * 2, 10))
    ax.yaxis.set_ticks(np.arange(0, y_center * 2, 10))
    ax.set_aspect("equal", "box") # we want equal aspect ratio to ensure the circle shows up as a circle
    ax.invert_yaxis() # due to js coord, we should invert y axis to be consistent

    # Save the plot as a PNG file 
    plt.savefig(f"./data/images/{input_filename}.png")

# plots moving average distance of arrows over iteration
def plot_ma_distance(input_filename, dictionary, center, conv_width):
    fig, ax = plt.subplots()  # Create a figure and a set of subplots
    distances = [] # to store distances for each arrow

    # stores the distances for each arrow in all sets
    for i in range(1, len(dictionary) + 1):
        coordinates = dictionary[i]

        for x, y, _ in coordinates:
            distances.append(calculate_distance([x, y], center))

    # list of arrows as a list (1, 2, ..., n)
    arrow_vec = [val for val in range(1, len(distances) + 1)]

    # list of arrows for moving average (same length list but remove conv_width on upper bound)
    ma_arrow_vec = [val for val in range(1, len(distances) + 1 - conv_width + 1)]

    # get MA using numpy's cumsum and average calculation
    cumsum_vec = np.cumsum(np.insert(distances, 0, 0))
    ma_vec = (cumsum_vec[conv_width: ] - cumsum_vec[: -conv_width]) / conv_width

    # plots distances and MA
    ax.scatter(arrow_vec, distances, color = colors[0])
    ax.plot(ma_arrow_vec, ma_vec, color = colors[1], marker='.', linestyle=':')

    # plot details
    ax.set_xlabel("Arrow No.")
    ax.set_ylabel("Distance from Center [cm]")
    ax.set_title("Distance from Center for Increasing Arrow Count")
    ax.grid(False)

    # save plot
    plt.savefig(f"./data/images/{input_filename}-ma.png")

def plot_kmeans(input_filename, dictionary, center, radius):

    # we want 4 plots formatted 2x2
    fig, axs = plt.subplots(2, 2, figsize = (13, 8), sharex = True, sharey = True)

    # run KMeans for 1, 2, 3, 4 clusters
    for k in range(0, 4):
        kmeans = KMeans(n_clusters = k + 1)
        xy_values = []
        t_values = []

        # store correct info for each point in dictionary
        for i in range(1, len(dictionary) + 1):
            coordinates = dictionary[i]

            x_values = [coord[0] for coord in coordinates]
            y_values = [coord[1] for coord in coordinates]
            color_idx = [coord[2] for coord in coordinates]

            for j in range(len(x_values)):
                x = x_values[j]
                y = y_values[j]
                t = color_idx[j]

                xy_values.append([x, y])
                t_values.append(t)

        # lets format this into array for kmeans
        xy_values = np.array(xy_values)

        # kmeans info
        kmeans.fit(xy_values)
        y_kmeans = kmeans.predict(xy_values)
        centers = kmeans.cluster_centers_

        # get the right plot in the figure
        ax = axs[k // 2, k % 2]

        # plot number of arrow in each set and color that number with the predicted cluster
        for xy, t, pred in zip(xy_values, t_values, y_kmeans):
            ax.text(xy[0], xy[1], t, color = colors[pred], fontsize = 10)

        # plot clusters
        ax.scatter(centers[:, 0], centers[:, 1], color = colors[:k + 1], alpha = 0.5)

        # plot target
        circle = Circle(center, radius, fill = True, alpha = 0.2, color = colors[4])
        ax.add_patch(circle)

        # plot details
        x_center, y_center = center
        ax.set_xlabel("x [cm]")
        ax.set_ylabel("y [cm]")
        ax.set_title(f"K-Means (k = {k + 1})")
        ax.grid(False)
        ax.xaxis.set_ticks(np.arange(0, x_center * 2, 10))
        ax.yaxis.set_ticks(np.arange(0, y_center * 2, 10))
        ax.set_aspect("equal", "box") # we want equal aspect ratio to ensure the circle shows up as a circle

    axs[0, 0].invert_yaxis() # due to js coord, we should invert y axis to be consistent

    # save figure of 4 plots
    plt.savefig(f"./data/images/{input_filename}-kmeans.png")
