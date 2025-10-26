
import matplotlib
from matplotlib.patches import Rectangle
matplotlib.use('QtAgg')


from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):
    def __init__(self, canvas_model, the_parent):
        self.the_parent = the_parent
        fig = Figure(figsize=(200, 200))
        super().__init__(fig)

        self.canvas_model = canvas_model
        self.axes = fig.add_subplot(111)

        self.figure.set_facecolor("#262626")  #
        self.axes.set_facecolor("#262626")

        for spine in self.axes.spines.values():
            spine.set_color("white")
            # spine.set_linewidth(2)

        self.axes.tick_params(axis='x', colors='white')
        self.axes.tick_params(axis='y', colors='white')

    def update_plot(self, clear = True):

        if clear :  self.axes.clear()
        self.axes.plot(self.canvas_model.xdata, self.canvas_model.ydata, 'r')
        self.draw()

    def draw_rectangles(self, rectangles : list[list[int]]):
        self.axes.clear()
        for rec in rectangles:
            rect = Rectangle((rec[0], rec[1]), rec[2], rec[3], fill= False,  color= "#ABAB2C")
            self.axes.add_patch(rect)

        self.update_plot(clear=False)


