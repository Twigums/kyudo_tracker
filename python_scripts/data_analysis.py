import sys
from data_functions import *

# sample mato (target) data in the image
coord_center = [903, 542]
coord_edge = [1151, 551]
pixel_radius = calculate_distance(coord_center, coord_edge)

# trash area
trash_corner1 = [24, 1231]
trash_corner2 = [91, 1320]

# type of mato
real_diameter = 36 # in centimeters
real_radius = real_diameter / 2

# normalization factor changes pixel to cm
normalization_factor = real_radius / pixel_radius

# apply the normalization to the center
real_center = [coord * normalization_factor for coord in coord_center]

# calls all functions to generate marker plot and formats to send file to client
def generate_marker_plot(input_filename):
    formatted_data = format_data(input_filename)
    data_dict = make_dict(formatted_data, normalization_factor, trash_corner1, trash_corner2)
    plot_data(input_filename, data_dict, real_center, real_radius)


# calls all functions to generate MA plot and formats to send file to client
def generate_ma_plot(input_filename):
    formatted_data = format_data(input_filename)
    data_dict = make_dict(formatted_data, normalization_factor, trash_corner1, trash_corner2)
    plot_ma_distance(input_filename, data_dict, real_center, 10)

# calls all functions to generate KMeans plot and formats to send file to client
def generate_kmeans_plot(input_filename):
    formatted_data = format_data(input_filename)
    data_dict = make_dict(formatted_data, normalization_factor, trash_corner1, trash_corner2)
    plot_kmeans(input_filename, data_dict, real_center, real_radius)

if __name__ == "__main__":
    args = sys.argv
    globals()[args[1]](*args[2:])
