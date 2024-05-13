#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# -*- Imports -*-

import os, sys, csv
import math
import random
import fishbots_visualize
from matplotlib import pylab
from matplotlib import pyplot as plt



__author__ = "Rodrigo Sastré Villaseñor"



class Position(object):
    """
    A Position represents a location in a two-dimensional ocean_grid.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).

        x: a real number indicating the x-coordinate
        y: a real number indicating the y-coordinate
        """
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the ocean_grid.

        angle: integer representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

# === Exercises 1 and 2


class RectangularOceanGrid(object):
    """
    A RectangularOceanGrid represents a rectangular region containing clean or dirty
    tiles.

    A ocean_grid has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width:int, height:int):
        """
        Initializes a rectangular ocean_grid with the specified width and height.
        Initially, no tiles in the ocean_grid have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        if (width <= 0) or (height <= 0):
            raise ValueError("Width and height must be greater than 0!")
        self._width = width
        self._height = height
        self._cleaned_tiles = set()

    def cleanTileAtPosition(self, pos:Position):
        """
        Mark the tile under the position POS as cleaned.
        Assumes that POS represents a valid position inside this ocean_grid.

        pos: a Position
        """
        self._cleaned_tiles.add((int(pos.getX()), int(pos.getY())))

    def isTileCleaned(self, m:int, n:int) -> bool:
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the ocean_grid.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return (m, n) in self._cleaned_tiles

    def getNumTiles(self):
        """
        Return the total number of tiles in the ocean_grid.

        returns: an integer
        """
        return self._width * self._height


    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the ocean_grid.

        returns: an integer
        """
        return len(self._cleaned_tiles)

    def getRandomPosition(self) -> Position:
        """
        Return a random position inside the ocean_grid.

        returns: a Position object.
        """
        return Position(random.randint(0, self._width - 1), random.randint(0, self._height - 1))

    def isPositionInOceanGrid(self, pos:Position) -> bool:
        """
        Return True if POS is inside the ocean_grid.

        pos: a Position object.
        returns: True if POS is in the ocean_grid, False otherwise.
        """
        return (0 <= pos.getX() < self._width) and (0 <= pos.getY() < self._height)

    def PercentageCleaned(self):
        return len(self._cleaned_tiles) / self.getNumTiles()



class BaseFishbot(object):
    """
    Represents a fishbot cleaning a particular ocean_grid.

    At all times the fishbot has a particular position and direction in
    the ocean_grid.  The fishbot also has a fixed speed.

    Subclasses of BaseFishbot should provide movement strategies by
    implementing updatePositionAndClean(), which simulates a single
    time-step.
    """

    def __init__(self, ocean_grid:RectangularOceanGrid, speed:float):
        """
        Initializes a Fishbot with the given speed in the specified
        ocean_grid. The fishbot initially has a random direction d and a
        random position p in the ocean_grid.

        The direction d is an integer satisfying 0 <= d < 360; it
        specifies an angle in degrees.

        p is a Position object giving the fishbot's position.

        ocean_grid:  a RectangularOceanGrid object.
        speed: a float (speed > 0)
        """
        if speed <= 0:
            raise ValueError("Speed must be greater than 0!")
        self._ocean_grid = ocean_grid
        self._speed = speed
        self._direction = random.randint(0, 359)
        self._position = self._ocean_grid.getRandomPosition()

    def getFishbotPosition(self):
        """
        Return the position of the fishbot.

        returns: a Position object giving the fishbot's position.
        """
        return self._position

    def getFishbotDirection(self):
        """
        Return the direction of the fishbot.

        returns: an integer d giving the direction of the fishbot as an angle in
        degrees, 0 <= d < 360.
        """
        return self._direction

    def setFishbotPosition(self, position:Position):
        """
        Set the position of the fishbot to POSITION.

        position: a Position object.
        """
        self._position = position

    def setFishbotDirection(self, direction:int):
        """
        Set the direction of the fishbot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        if 0 <= direction < 360:
            self._direction = direction
        else:
            raise ValueError("Direction should be between 0 and 359 inclusive.")


class StandardFishbot(BaseFishbot):
    """
    A StandardFishbot is a BaseFishbot with the standard movement strategy.

    At each time-step, a StandardFishbot attempts to move in its current
    direction; when it hits a wall, it chooses a new direction
    randomly.
    """

    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the fishbot to a new position and mark the tile it is on as having
        been cleaned.
        """
        # first I compute new position using current direction and speed
        new_position = self.getFishbotPosition().getNewPosition(self.getFishbotDirection(), self._speed)
        # then I check if new position is inside the grid and update accordingly
        while not self._ocean_grid.isPositionInOceanGrid(new_position):
            # depending on where the fishbot would be out of bounds, we update its direction
            # using function defined above _newDirection
            self.setFishbotDirection(self._newDirection(new_position))
            new_position = self.getFishbotPosition().getNewPosition(self.getFishbotDirection(), self._speed)
        #set the new valid position and clean tile
        self.setFishbotPosition(new_position)
        self._ocean_grid.cleanTileAtPosition(new_position)

    def _newDirection(self, position:Position) -> int:
        x,y = position.getX(), position.getY()
        if x < 0:
            return random.randint(0, 179)
        elif x >= self._ocean_grid._width:
            return random.randint(180, 359)
        elif y < 0:
            return random.randint(90, 269)
        elif y >= self._ocean_grid._height:
            return random.randint(270, 359)



# === Exercise 3

def runSimulation(num_fishbots, speed, width, height, min_coverage, num_trials, fishbot_type, visualize):
    """
    Runs NUM_TRIALS trials of the simulation and returns a list of
    lists, one per trial. The list for a trial has an element for each
    timestep of that trial, the value of which is the percentage of
    the ocean_grid that is clean after that timestep. Each trial stops when
    MIN_COVERAGE of the ocean_grid is clean.

    The simulation is run with NUM_FISHBOTS fishbots of type FISHBOT_TYPE,
    each with speed SPEED, in a ocean_grid of dimensions WIDTH x HEIGHT.

    Visualization is turned on when boolean VISUALIZE is set to True.

    num_fishbots: an int (num_fishbots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    fishbot_type: class of fishbot to be instantiated (e.g. StandardFishbot or
                RandomWalkFishbot)
    visualize: a boolean (True to turn on visualization)

    test case:
    avg = runSimulation(10, 1.0, 15, 20, 0.8, 30, StandardFishbot, False)

    """
    def run_trial():
        ocean_grid = RectangularOceanGrid(width, height)
        fishbots = []
        for _ in range(num_fishbots):
            fishbots.append(fishbot_type(ocean_grid, speed))
        cleaned_percentages = []

        while ocean_grid.PercentageCleaned() < min_coverage:
            for fishbot in fishbots:
                fishbot.updatePositionAndClean()
            cleaned_percentages.append(ocean_grid.PercentageCleaned())

        return cleaned_percentages
    all_trials_results = [run_trial() for _ in range(num_trials)]
    return all_trials_results

#
# # === Provided functions
def computeMeans(list_of_lists):
    """
    Returns a list as long as the longest list in LIST_OF_LISTS, where
    the value at index i is the average of the values at index i in
    all of LIST_OF_LISTS' lists.

    Lists shorter than the longest list are padded with their final
    value to be the same length.
    """
    # Find length of longest list
    longest = 0
    for lst in list_of_lists:
        if len(lst) > longest:
           longest = len(lst)
    # Get totals
    tots = [0]*(longest)
    for lst in list_of_lists:
        for i in range(longest):
            if i < len(lst):
                tots[i] += lst[i]
            else:
                tots[i] += lst[-1]
    # Convert tots to an array to make averaging across each index easier
    tots = pylab.array(tots)
    # Compute means
    means = tots/float(len(list_of_lists))
    return means

def calcAvgLengthList(listOfLists):
    """
    Takes a list of lists and then calculates the average length of the lists
    """
    sumOfLengths = 0
    averageLength = 0
    for eachList in listOfLists:
        sumOfLengths += len(eachList)
    averageLength = sumOfLengths / len(listOfLists)
    # print(averageLength)
    return averageLength

def write_lists_csv(block_list,file_name, headers):
    """
    Takes a list or list of lists, a files location//name, and a list of headers
    Writes the itemsof the lists as rows in a CSV file.  Each item of the list is a comma-separated value.
    Returns the location of the CSV file.
    """
    # fileWriter = csv.writer(open(file_name, 'w'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # fileWriter.writerow(headers)
    # for each in block_list:
    #     fileWriter.writerow(each)

    fileWriter = open(file_name, 'w')
    fileWriter.writelines(headers)
    for item in block_list:
      fileWriter.write("%s\n" % item)

# === Exercise 4

class RandomWalkFishbot(BaseFishbot):
    """
    A RandomWalkFishbot is a fishbot with the "random walk" movement
    strategy: it chooses a new direction at random after each
    time-step.
    """

    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the fishbot to a new position and mark the tile it is on as having
        been cleaned.
        """
        # set a new random direction
        self.setFishbotDirection(random.randint(0, 359))
        # compute new position using current direction and speed
        new_position = self.getFishbotPosition().getNewPosition(self.getFishbotDirection(), self._speed)
        # then I check if new position is inside the grid and update accordingly
        while not self._ocean_grid.isPositionInOceanGrid(new_position):
            self.setFishbotDirection(self._newDirection(new_position))
            new_position = self.getFishbotPosition().getNewPosition(self.getFishbotDirection(), self._speed)
        # Set the new valid position and clean tile
        self.setFishbotPosition(new_position)
        self._ocean_grid.cleanTileAtPosition(new_position)

    #function to get a new, valid, random direction depending on the location of the fishbot
    def _newDirection(self, position: Position) -> int:
        x, y = position.getX(), position.getY()
        if x < 0:
            return random.randint(0, 179)
        elif x >= self._ocean_grid._width:
            return random.randint(180, 359)
        elif y < 0:
            return random.randint(90, 269)
        elif y >= self._ocean_grid._height:
            return random.randint(270, 359)


# ==================== #
# === fishbots.1 === #
# ==================== #
def showPlot1(title, x_label, y_label):
    """
    Produces a plot comparing the two fishbot strategies in a 20x20 ocean grid with each of 1-10 fishbots and an 80%
    minimum coverage in 20 trials.
    """
    fishrange = range(1,11)
    stdfishbot = []
    randomfishbot = []
    for num_fish in fishrange:
        std_results = runSimulation(num_fish, 1.0, 20, 20, 0.8, 20, StandardFishbot, False)
        avg_std_result = sum(len(trial) for trial in std_results) / 20
        stdfishbot.append(avg_std_result)
        random_results = runSimulation(num_fish, 1.0, 20, 20, 0.8, 20, RandomWalkFishbot, False)
        avg_random_result = sum(len(trial) for trial in random_results) / 20
        randomfishbot.append(avg_random_result)
    plt.figure()
    plt.plot(fishrange, stdfishbot, label = "StandardFishbot")
    plt.plot(fishrange, randomfishbot, label = "RandomWalkFishbot")
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.show()


# ==================== #
# === fishbots.2 === #
# ==================== #
def showPlot2(title, x_label, y_label):
    """
    Produces a plot showing dependence of cleaning time on ocean grid shape.
    How long does it take two fishbots to clean 80% of rooms with the following dimensions:
        20x20,
        25x16,
        40x10,
        50x8,
        80x5,
        100x4?
    (Notice that the rooms have the same area.)
    Output a figure that plots the mean time (on the Y-axis) against the ratio of width to height.
    """
    dimensions = [(20, 20), (25, 16), (40, 10), (50, 8), (80, 5), (100, 4)]
    std_fishbot_results = []
    random_fishbot_results = []
    for (width, height) in dimensions:
        # Run simulations for StandardFishbot
        std_trials = runSimulation(2, 1.0, width, height, 0.8, 1, StandardFishbot, False)
        std_fishbot_results.append(sum(len(trial) for trial in std_trials)/1)
        # Run simulations for RandomWalkFishbot
        random_trials = runSimulation(2, 1.0, width, height, 0.8, 1, RandomWalkFishbot, False)
        random_fishbot_results.append(sum(len(trial) for trial in random_trials)/1)
    labels = ["20x20", "25x16", "40x10", "50x8", "80x5", "100x4"]
    plt.figure()
    plt.plot(labels, std_fishbot_results, label = "StandardFishbot")
    plt.plot(labels, random_fishbot_results, label = "RandomWalkFishbot")
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    # # === Run code

    showPlot1("Time It Takes 1 - 10 Fishbots To Clean 80% Of A Room", "Number of Fishbots", "Time-steps")
    showPlot2("Time It Takes Two Fishbots To Clean 80% Of Variously Shaped Ocean Grids", "Ocean Grid Aspect Ratio",
              "Time-steps")



