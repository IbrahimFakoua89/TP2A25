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

    def __init__(self,model ,parent=None):
        fig = Figure(figsize=(200, 200))
        super().__init__(fig)
        self.model = model

        self.axes = fig.add_subplot(111)

        self.figure.set_facecolor("#262626")  # figure background
        self.axes.set_facecolor("#262626")  # plot background



        for spine in self.axes.spines.values():
            spine.set_color("white")  # hex color
            # spine.set_linewidth(2)  # thickness in points

        self.axes.tick_params(axis='x', colors='white')  # green x-axis ticks
        self.axes.tick_params(axis='y', colors='white')  # blue y-axis ticks

    def update_plot(self):

        equation = self.model.function
        print(equation)

        print(self.model.ydata)
        self.axes.clear()
        self.axes.plot(self.model.xdata, self.model.ydata, 'r')
        self.draw()


