from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, pyqtSignal
from matplotlib import mathtext
import sympy as sp
import re
from sympy.parsing.latex import parse_latex
from sympy import symbols



class FunctionListModel(QAbstractListModel):
    error_statusBar = pyqtSignal(str)
    def __init__(self, list_of_function=None):
        super().__init__()

        self._functionsList = list_of_function or []



    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._functionsList)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._functionsList[index.row()]
        return None

    def add_function(self, function: str):
        func = sp.sympify(function)
        latex_func = sp.latex(func)
        print(latex_func)
        if not self.function_verification(latex_func):
            return
        if not is_only_x_variable(latex_func): return
        row = len(self._functionsList)
        self.beginInsertRows(QModelIndex(), row, row)
        self._functionsList.append(latex_func)
        self.endInsertRows()
    def function_verification(self,function) -> bool:
        if function in self._functionsList: return False
        # if any(ch.isalpha() and ch.lower() != 'x' for ch in function):
        #     self.error_statusBar.emit("Erreur : seule la variable « x » est autorisée.")
        #     return False  #Contains letters other than x
        # else:
        #     return True


        return True

    def remove_function(self, row: int): #todo the case if no sellection is made error
        if 0 <= row < len(self._functionsList):
            self.beginRemoveRows(QModelIndex(), row, row)
            del self._functionsList[row]
            self.endRemoveRows()

