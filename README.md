# Ocean-Cleaning-Fishbots-Simulation

**Needs cleaning and restructuring**

This Python program simulates cleaning tasks in ocean grids using autonomous fishbots. The program models fishbots with different movement strategies in various grid configurations to determine the efficiency of cleaning operations. It includes visualization capabilities to compare performance metrics across different scenarios.

Overview
The Python project is designed to model and simulate the efficiency of autonomous fishbots in cleaning a predefined ocean grid area. The simulation assesses how quickly fishbots can clean a certain percentage of the ocean grid, influenced by the number of fishbots, their movement strategies, and the grid's dimensions. Visualization functions are included to illustrate the performance differences between standard movement strategies and random walks.


Key Components
Classes and Basic Functionality:

Position: Manages coordinates within the ocean grid.
RectangularOceanGrid: Represents the ocean grid environment, tracking clean and dirty tiles.
BaseFishbot: Abstract base class for fishbots with methods to manage and update their positions.
StandardFishbot: Implements a standard movement strategy where the fishbot moves straight until it encounters a boundary.
RandomWalkFishbot: Implements a random movement strategy, changing direction randomly at each step.

Simulation Control:
runSimulation: Manages simulation trials, accepting parameters such as the number of fishbots, grid size, and minimum cleaning coverage to determine the performance of cleaning strategies over multiple runs.

Data Analysis and Visualization:
computeMeans, calcAvgLengthList: Analytical functions to process simulation data, calculating averages and other statistics.
write_lists_csv: Outputs simulation results to CSV files for further analysis.
showPlot1, showPlot2: Visualization functions that generate plots to compare the efficiency of different fishbot configurations and strategies.

Usage
To run a simulation or generate a plot, call the appropriate function in the if __name__ == "__main__" block at the end of the script. Here’s how you might call a function to simulate and visualize:

num_fishbots = 5
speed = 1.0
width = 20
height = 20
min_coverage = 0.8
num_trials = 30
fishbot_type = StandardFishbot
visualize = False

# Run a simulation
avg_cleaning_times = runSimulation(num_fishbots, speed, width, height, min_coverage, num_trials, fishbot_type, visualize)

# Generate a plot
showPlot1("Efficiency of Fishbots", "Number of Fishbots", "Time-steps to Clean 80% of Grid")

Conclusion
This program provides a useful tool for researching and understanding the dynamics of autonomous cleaning bots in maritime environments. It could be applied in academic research, robotic development, and simulations to optimize cleaning strategies and bot designs for environmental maintenance tasks.
