from data_functions import *

# which file we want to use
INPUT_FILENAME = "../coordinates_2024-1-23_17-0-12"

# sample mato (target) data in the image
coord_center = [903, 542]
coord_edge = [1151, 551]
pixel_radius = calculate_distance(coord_center, coord_edge)

# type of mato
real_diameter = 36 # in centimeters
real_radius = real_diameter / 2

# normalization factor changes pixel to cm
normalization_factor = real_radius / pixel_radius

# apply the normalization to the center
real_center = [coord * normalization_factor for coord in coord_center]

# applying functions
formatted_data = format_data(INPUT_FILENAME)
data_dict = make_dict(formatted_data, normalization_factor)
plot_data(INPUT_FILENAME, data_dict, real_center, real_radius) # should automatically save the plot as "INPUT_FILENAME".png
