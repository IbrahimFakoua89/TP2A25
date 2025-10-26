

import numpy as np
import sympy as sp
from PyQt6.QtCore import QObject, pyqtSignal




class Model(QObject):
    function_parameters_changed = pyqtSignal()
    rectangle_parameters_changed = pyqtSignal(object)
    show_warning = pyqtSignal(str, str)
    riemann_result_changed = pyqtSignal(str)
    integral_result_changed = pyqtSignal(str)
    clear_rectangles = pyqtSignal()
    def __init__(self):
        super().__init__()

        self._mydict_integral = {
            "radioButton_state": None,
            "nombre_de_rectangle": None,
            "riemann_result": None,
            "integral_result": None
        }
        self._plot_params: dict[str, int | None] = {
            "xdata": None,
            "ydata": None,
            "borne_sup": None,
            "borne_inf": None,
            "function": None,
            "sympy_function": "",
        }
        self._mydict_function_optional = {
            "title": ""

        }

    def on_clicked_integral(self):
        self.send_signal_if_valid_integral()

    def riemann(self, method):
        f = self.function

        x = np.linspace(self.borne_inf, self.borne_sup, self.nombre_de_rectangle + 1)
        dx = (self.borne_sup - self.borne_inf) / self.nombre_de_rectangle


        if method == "gauche":
            self.riemann_result =np.sum(f(x[:-1])) * dx
        elif method == "droite":
            self.riemann_result = np.sum(f(x[1:])) * dx


    def integral(self):
        x = sp.symbols('x')

        self.integral_result = (sp.integrate(self.sympy_function, (x, self.borne_inf, self.borne_sup))).evalf()


    def verify(self):


        if self.nombre_de_rectangle == 0:
            self.clear_rectangles.emit()
            return False
        if (self._mydict_integral["radioButton_state"] is None) or (
                self._mydict_integral["nombre_de_rectangle"] is None):
            return False

        if any(value is None for value in self._plot_params.values()): return False

        return True

    def send_signal_if_valid_integral(self):
        if not self.verify(): return


        self.integral()
        rectangles: list[list[float]] = []
        width = (self.borne_sup - self.borne_inf) / self.nombre_de_rectangle
        func = self.function
        if self.radioButton_state == "droite":
            self.riemann("droite")
            width_offset = width
        else:
            self.riemann("gauche")
            width_offset = 0

        for i in range(self.nombre_de_rectangle):
            x = self.borne_inf + (width * i)
            height = func(x + width_offset)
            rectangles.append([x, 0, width, height])
        self.rectangle_parameters_changed.emit(rectangles)


    def is_borne_valid(self, value: str):
        new_value = value.removeprefix('-')
        if new_value == "": return False
        if not new_value.isdigit():
            self.show_warning.emit("Borne invalid" , "warning")
            return False

        if abs(int(new_value)) > 1000000000000000000: return False
        return True

    def send_signal_if_valid_fucntion(self):
        if self._plot_params["borne_sup"] is None: return
        if self._plot_params["borne_inf"] is None: return
        if self._plot_params["function"] is None: return
        if not self.calculations_for_graph(): return
        self.function_parameters_changed.emit()

    def calculations_for_graph(self):
        self._plot_params["xdata"] = np.linspace(self.borne_inf, self.borne_sup,
                                                 int(np.log(abs(self.borne_sup - self.borne_inf) + 1) * 100))
        try:
            self._plot_params["ydata"] = self.function(self.xdata)
        except Exception:
            self.show_warning.emit("Function too large to compute or is invalid", "warning")

        if not (isinstance(self._plot_params["ydata"], np.ndarray)):
            self.show_warning.emit("ydata is not an array", "warning")
            return False
        return True

    @property
    def function(self):
        return self._plot_params["function"]

    @function.setter
    def function(self, func):

        self._plot_params["function"] = func
        self.send_signal_if_valid_fucntion()

    @property
    def borne_inf(self):
        return self._plot_params["borne_inf"]

    @borne_inf.setter
    def borne_inf(self, value):
        if self.is_borne_valid(value):
            self._plot_params["borne_inf"] = int(value)
            self.send_signal_if_valid_fucntion()

    @property
    def borne_sup(self):

        return self._plot_params["borne_sup"]

    @borne_sup.setter
    def borne_sup(self, value):
        if self.is_borne_valid(value):
            self._plot_params["borne_sup"] = int(value)
            self.send_signal_if_valid_fucntion()

    @property
    def nombre_de_rectangle(self) -> int:
        return self._mydict_integral["nombre_de_rectangle"]

    @nombre_de_rectangle.setter
    def nombre_de_rectangle(self, value):
        self._mydict_integral["nombre_de_rectangle"] = value
        # self.send_signal_if_valid_integral()

    @property
    def radioButton_state(self):
        return self._mydict_integral["radioButton_state"]

    @radioButton_state.setter
    def radioButton_state(self, value):

        self._mydict_integral["radioButton_state"] = value
        # self.send_signal_if_valid_integral()

    @property
    def xdata(self):
        return self._plot_params["xdata"]

    @property
    def ydata(self):
        return self._plot_params["ydata"]

    @property
    def integral_result(self):
        return self._integral_result

    @integral_result.setter
    def integral_result(self, value ):
        self._mydict_integral["integral_result"] = value

        self.integral_result_changed.emit(str(value))
    @property
    def riemann_result(self):
        return self._riemann_result

    @riemann_result.setter
    def riemann_result(self, value):
        self._mydict_integral["riemann_result"] = value
        self.riemann_result_changed.emit(str(value))


    @property
    def sympy_function(self):
        return self._plot_params["_sympy_function"]

    @sympy_function.setter
    def sympy_function(self, value):
        self._plot_params["_sympy_function"] = value


