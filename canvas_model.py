from pydoc import source_synopsis

from PyQt6.QtCore import QAbstractListModel, QModelIndex, Qt, QObject, pyqtSignal
import sympy as sp
import numpy as np
from PyQt6.QtWidgets import QMessageBox


def is_borne_valid(value: str):
    new_value = value.removeprefix('-')

    if not new_value.isdigit(): return False
    if new_value == "": return False

    if abs(int(new_value)) > 1000000000000000000  : return False
    return True


class Model(QObject):
    function_parameters_changed = pyqtSignal()
    rectangle_parameters_changed = pyqtSignal(str)
    show_warning = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._mydict_integral = {
            "radioButton_state": None,
            "nombre_de_rectangle": None,
        }
        self._mydict_function: dict[str, int | None] = {
            "xdata": None,
            "ydata": None,
            "borne_sup": None,
            "borne_inf": None,
            "function": "",
        }
        self._mydict_function_optional = {
            "title": ""

        }

    def send_signal_if_valid(self):
        if self._mydict_function["borne_sup"] is None: return
        if self._mydict_function["borne_inf"] is None: return
        if self._mydict_function["function"] == "": return
        if not self.calculations_for_graph() : return
        self.function_parameters_changed.emit()

    def calculations_for_graph(self):
        self._mydict_function["xdata"] = np.linspace(self.borne_inf, self.borne_sup, int( np.log(abs(self.borne_sup - self.borne_inf ) + 1) * 100))
        try:
            self._mydict_function["ydata"] = self._mydict_function["function"](self._mydict_function["xdata"])
        except Exception:
            print("hi")

        if not (isinstance(self._mydict_function["ydata"],np.ndarray)):
            self.show_warning.emit("ydata is not an array")
            return False
        return True



    @property
    def function(self):
        return self._mydict_function["function"]

    @function.setter
    def function(self, func):

        self._mydict_function["function"] = func
        self.send_signal_if_valid()

    @property
    def borne_inf(self):
        return self._mydict_function["borne_inf"]

    @borne_inf.setter
    def borne_inf(self, value):
        if is_borne_valid(value): # todo show error
            self._mydict_function["borne_inf"] = int(value)
            self.send_signal_if_valid()

    @property
    def borne_sup(self):

        return self._mydict_function["borne_sup"]

    @borne_sup.setter
    def borne_sup(self, value):
        if is_borne_valid(value): # todo show error
            self._mydict_function["borne_sup"] = int(value)  # todo if not int
            self.send_signal_if_valid()


    @property
    def nombre_de_rectangle(self):
        return self._mydict_integral["nombre_de_rectangle"]

    @nombre_de_rectangle.setter
    def nombre_de_rectangle(self, value):
        self._mydict_integral["nombre_de_rectangle"] = value
        self.rectangle_parameters_changed.emit()

    @property
    def radioButton_state(self):
        return self._mydict_integral["radioButton_state"]

    @radioButton_state.setter
    def radioButton_state(self, value):
        self._mydict_integral["radioButton_state"] = value
        self.rectangle_parameters_changed.emit()

    @property
    def xdata(self):
        return self._mydict_function["xdata"]

    @property
    def ydata(self):
        return self._mydict_function["ydata"]
