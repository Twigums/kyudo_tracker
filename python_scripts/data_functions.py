import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# This function formats the data from a text file into a list of lists
def format_data(input_filename):
    with open(f"{input_filename}.txt", "r") as file:
        data = file.read().split("\n")

    formatted_data = []

    # use mapping to format data into a list and append
    for line in data:
        if line != "":
            formatted_data.append(list(map(int, line.split(", "))))

    return formatted_data

# This function converts the formatted data into a dictionary
def make_dict(data, normalization_factor):
    data_dict = {} # empty dictionary

    # we normalize the data points to change pixel values into centimeters
    for point in data:
        set_value, x, y = point

        if set_value not in data_dict:
            data_dict[set_value] = [[x * normalization_factor, y * normalization_factor]]
        else:
            data_dict[set_value].append([x * normalization_factor, y * normalization_factor])

    return data_dict

# This function calculates the Euclidean distance between two points
def calculate_distance(coord1, coord2):
    coord1 = np.array(coord1)
    coord2 = np.array(coord2)

    # definition of Euclidean distance
    dist = np.sqrt(np.sum((coord1 - coord2) ** 2))

    return dist

# This function plots the data points and a circle on a 2D grid
def plot_data(input_filename, dictionary, center, radius):
    fig, ax = plt.subplots()  # Create a figure and a set of subplots

    for i in range(1, len(dictionary) + 1):

        coordinates = dictionary[i]

        x_values = [coord[0] for coord in coordinates]
        y_values = [coord[1] for coord in coordinates]

        # opacity is scaled for how many keys in the dictionary (how many sets)
        opacity = i / len(dictionary)

        # Plot the points with the calculated opacity
        ax.scatter(x_values, y_values, alpha = opacity)

    # Create a circle with the given center and radius
    circle = Circle(center, radius, fill=True, alpha = 0.2)
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

    # Save the plot as a PNG file
    plt.savefig(f"{input_filename}.png")
