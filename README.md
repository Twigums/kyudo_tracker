# kyudo_tracker

A plain website to track where your arrows went. The data is automatically saved every time you click end set, and at the end of the session, the data can be parsed using the functions in the python_scripts directory.

On the website:

- clear markers: clears the markers from the set
- end set: saves the current markers into a text file and hides the shown markers
- show all: shows all markers (hits) from all sets
- hide all: hides all markers (hits) from all sets

Python script:

all implementations will use colors from ibm design (https://carbondesignsystem.com/data-visualization/color-palettes/)

- `plot_data`: plots where the arrows landed in relation to the target
- `plot_ma_distance`: plots the moving average of the distance between the arrow to the center of the target
- `plot_kmeans`: plots result of clustering k-NN with clusters from [1, 4]
