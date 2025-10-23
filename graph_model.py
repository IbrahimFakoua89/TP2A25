from PyQt6.QtCore import QAbstractListModel, QModelIndex, Qt, QObject, pyqtSignal
import sympy as sp
import numpy as np

class Model(QObject):
    function_parameters_changed = pyqtSignal()
    rectangle_parameters_changed = pyqtSignal(str)


    def __init__(self):
        super().__init__()
        self.xdata = None
        self.ydata = None
        self._radioButton_state = None
        self._nombre_de_rectangle = None
        self._borne_sup = None
        self._borne_inf = None
        self._function = ""
        self._title = ""

    @property
    def function(self):
        return self._function

    @function.setter
    def function(self, func):


        self._function = func
        self.xdata = np.linspace(self._borne_inf, self._borne_sup, 200)

        self.ydata = func(self.xdata)

        self.function_parameters_changed.emit()

    @property
    def borne_inf(self):
        return self._borne_inf

    @borne_inf.setter
    def borne_inf(self, value):
        self._borne_inf = value
        self.function_parameters_changed.emit()

    @property
    def borne_sup(self):
        return self._borne_sup

    @borne_sup.setter
    def borne_sup(self, value):
        self._borne_sup = value
        self.function_parameters_changed.emit()

    @property
    def nombre_de_rectangle(self):
        return self._nombre_de_rectangle

    @nombre_de_rectangle.setter
    def nombre_de_rectangle(self, value):
        self._nombre_de_rectangle = value
        self.rectangle_parameters_changed.emit()

    @property
    def radioButton_state(self):
        return self._radioButton_state

    @radioButton_state.setter
    def radioButton_state(self, value):
        self._radioButton_state = value
        self.rectangle_parameters_changed.emit()


