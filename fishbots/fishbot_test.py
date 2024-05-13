import unittest
from unittest.mock import patch, call
import fishbots


class TestShowPlot1(unittest.TestCase):
    @patch('fishbots.runSimulation')
    @patch('fishbots.pylab')
    def setUp(self, mock_pylab, mock_runSimulation):
        self.mock_pylab = mock_pylab
        self.mock_runSimulation = mock_runSimulation
        self.mock_runSimulation.return_value = 10  # or whatever value is appropriate

        self.title = "Fishbot Performance"
        self.x_label = "Number of Robots"
        self.y_label = "Time Taken"
        fishbots.showPlot1(self.title, self.x_label, self.y_label)

    def test_runSimulation_call_count(self):
        msg = "runSimulation should be called 10 times for each strategy"
        self.assertEqual(20, self.mock_runSimulation.call_count, msg)

    def test_runSimulation_arguments(self):
        msg = "runSimulation should be called with correct arguments"
        try:
            calls = [call(i, 1.0, 20, 20, 0.8, 20, fishbots.StandardFishbot) for i in range(1, 11)]
            calls += [call(i, 1.0, 20, 20, 0.8, 20, fishbots.RandomWalkFishbot) for i in range(1, 11)]
            self.mock_runSimulation.assert_has_calls(calls, any_order=True)
        except AssertionError:
            raise AssertionError(msg)

    def test_pylab_plot_arguments(self):
        msg = "pylab.plot should be called with correct arguments for StandardFishbot and RandomWalkFishbot"
        try:
            calls = [call(range(1, 11), [10] * 10), call(range(1, 11), [10] * 10)]
            self.mock_pylab.plot.assert_has_calls(calls, any_order=True)
        except AssertionError:
            raise AssertionError(msg)

    def test_pylab_title_arguments(self):
        msg = "pylab.title should be called once with correct argument"
        try:
            self.mock_pylab.title.assert_called_once_with(self.title)
        except AssertionError:
            raise AssertionError(msg)

    def test_pylab_legend_arguments(self):
        msg = "pylab.legend should be called with correct arguments: StandardFishbot and RandomWalkFishbot"
        try:
            self.mock_pylab.legend.assert_called_once_with(('StandardFishbot', 'RandomWalkFishbot'))
        except AssertionError:
            raise AssertionError(msg)

    def test_pylab_xlabel_arguments(self):
        msg = "pylab.xlabel should be called once with correct argument"
        try:
            self.mock_pylab.xlabel.assert_called_once_with(self.x_label)
        except AssertionError:
            raise AssertionError(msg)

    def test_pylab_ylabel_arguments(self):
        msg = "pylab.ylabel should be called once with correct argument"
        try:
            self.mock_pylab.ylabel.assert_called_once_with(self.y_label)
        except AssertionError:
            raise AssertionError(msg)

    def test_pylab_show_call_count(self):
        msg = "pylab.show should be called once"
        try:
            self.mock_pylab.show.assert_called_once()
        except AssertionError:
            raise AssertionError(msg)


class TestShowPlot2(unittest.TestCase):
    @patch('fishbots.runSimulation')
    @patch('fishbots.pylab')
    def setUp(self, mock_pylab, mock_runSimulation):
        self.mock_pylab = mock_pylab
        self.mock_runSimulation = mock_runSimulation
        self.mock_runSimulation.return_value = 10  # or whatever value is appropriate

        self.title = "Fishbot Performance"
        self.x_label = "Ocean Grid Size"
        self.y_label = "Time Taken"
        fishbots.showPlot2(self.title, self.x_label, self.y_label)

    def test_runSimulation_call_count(self):
        msg = ("runSimulation should be called 12 times (6 for each ocean grid size: 20x20, 25x16, 40x10, 50x8, 80x5, "
               "100x4) for each strategy")

        self.assertEqual(12, self.mock_runSimulation.call_count, msg)

    def test_runSimulation_arguments(self):
        msg = "runSimulation should be called with correct arguments"
        try:
            ocean_grid_sizes = [(20, 20), (25, 16), (40, 10), (50, 8), (80, 5), (100, 4)]
            calls = [call(2, 1.0, x, y, 0.8, 20, fishbots.StandardFishbot) for x, y in ocean_grid_sizes]
            calls += [call(2, 1.0, x, y, 0.8, 20, fishbots.RandomWalkFishbot) for x, y in ocean_grid_sizes]
            self.mock_runSimulation.assert_has_calls(calls, any_order=True)
        except AssertionError:
            raise AssertionError(msg)

    def test_pylab_plot_arguments(self):
        msg = "pylab.plot should be called with correct arguments for StandardFishbot and RandomWalkFishbot"
        try:
            ocean_grid_aspect_ratios = ["x".join([str(x), str(y)]) for x, y in
                                        [(20, 20), (25, 16), (40, 10), (50, 8), (80, 5), (100, 4)]]
            calls = [call(ocean_grid_aspect_ratios, [10] * 6), call(ocean_grid_aspect_ratios, [10] * 6)]
            self.mock_pylab.plot.assert_has_calls(calls, any_order=True)
        except AssertionError:
            raise AssertionError(msg)

    def test_pylab_title_arguments(self):
        msg = "pylab.title should be called once with correct argument"
        try:
            self.mock_pylab.title.assert_called_once_with(self.title)
        except AssertionError:
            raise AssertionError(msg)

    def test_pylab_legend_arguments(self):
        msg = "pylab.legend should be called with correct arguments: StandardFishbot and RandomWalkFishbot"
        try:
            self.mock_pylab.legend.assert_called_once_with(('StandardFishbot', 'RandomWalkFishbot'))
        except AssertionError:
            raise AssertionError(msg)

    def test_pylab_xlabel_arguments(self):
        msg = "pylab.xlabel should be called once with correct argument"
        try:
            self.mock_pylab.xlabel.assert_called_once_with(self.x_label)
        except AssertionError:
            raise AssertionError(msg)

    def test_pylab_ylabel_arguments(self):
        msg = "pylab.ylabel should be called once with correct argument"
        try:
            self.mock_pylab.ylabel.assert_called_once_with(self.y_label)
        except AssertionError:
            raise AssertionError(msg)

    def test_pylab_show_call_count(self):
        msg = "pylab.show should be called once"
        try:
            self.mock_pylab.show.assert_called_once()
        except AssertionError:
            raise AssertionError(msg)


if __name__ == '__main__':
    unittest.main()
