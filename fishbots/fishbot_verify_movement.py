import pytest

from fishbots import StandardFishbot, RectangularOceanGrid, RandomWalkFishbot
from fishbots_visualize import FishbotVisualization


@pytest.mark.parametrize(
    'fishbot_type, grid_type', [(StandardFishbot, RectangularOceanGrid), (RandomWalkFishbot, RectangularOceanGrid)]
)
def testRobotMovement(fishbot_type, grid_type, delay=0.005):
    """
    Runs a simulation of a single fishbot of type fishbot_type in a 5x5 grid.
    """
    import fishbots_visualize
    grid = grid_type(10, 10)
    fidhbot = fishbot_type(grid, 1)
    anim = FishbotVisualization(3, 10, 10, delay)
    while grid.getNumCleanedTiles() < grid.getNumTiles():
        fidhbot.updatePositionAndClean()
        anim.update(grid, [fidhbot])

    anim.done()
