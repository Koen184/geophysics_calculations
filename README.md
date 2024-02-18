# geophysics_calculations
A script for performing more difficult calculations (terrain reduction calculation)
Part of the Fundamentals of Geophysics course.

Explanation of the code operation:
1. Data loading: The code begins by loading data from an Excel file (Geofizyka.xlsx). It reads data from two sheets: 'Data' and 'NMT' into respective data structures. The 'Data' sheet contains necessary information about measurement points, while the 'NMT' sheet contains information about nodal points of the numerical terrain model.
2. Constants and function definitions: Constants such as density (p_density), gravitational constant (G), and functions are defined, which are later used for calculations. Since calculations have repetitive forms, automation of this process was possible by defining functions executing parts of operations based on appropriately input variables (data from loaded sheets).
3. Iterations and calculations: The code iterates through measurement points and grid points, calculating distances between them (distance_check). Then, depending on conditions (here: if the distance is less than or equal to 1200 meters), certain point values are calculated based on previously defined functions (equation) and values from data loaded from the Excel file.
4. Plotting the graph: Graphs are generated based on calculated points and values from individual iterations. Around points on the graph, areas in the form of squares and circles are marked. Squares denote parallelepipeds with centers at nodal points of the numerical terrain model. Circles represent buffer areas for measurement points, where nodal points are sought, based on which the integral value for a given point is calculated.
5. Terrain reduction: Calculations related to terrain reduction are conducted based on calculations from previous steps. Terrain corrections are calculated for each point, and units are converted to mGal.
6. Displaying results: Results are displayed in the console and saved to a text file (results.txt), from which they can be copied to an Excel file and loaded into ArcGIS Pro for visualization.
