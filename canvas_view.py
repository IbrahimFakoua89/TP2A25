import sys
import random
import matplotlib
import numpy as np

matplotlib.use('QtAgg')
import sympy as sp
from PyQt6 import QtCore, QtWidgets

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):
    def __init__(self, canvas_model, the_parent):
        self.the_parent = the_parent
        fig = Figure(figsize=(200, 200))
        super().__init__(fig)

        self.canvas_model = canvas_model
        self.axes = fig.add_subplot(111)

        self.figure.set_facecolor("#262626")  # figure background
        self.axes.set_facecolor("#262626")  # plot background

        for spine in self.axes.spines.values():
            spine.set_color("white")  # hex color
            # spine.set_linewidth(2)  # thickness in points

        self.axes.tick_params(axis='x', colors='white')  # green x-axis ticks
        self.axes.tick_params(axis='y', colors='white')  # blue y-axis ticks

    def update_plot(self):
        equation = self.canvas_model.function
        self.axes.clear()

        self.axes.plot(self.canvas_model.xdata, self.canvas_model.ydata, 'r')

        self.draw()
