from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, pyqtSignal
from matplotlib import mathtext
import sympy as sp
import re
from sympy.parsing.latex import parse_latex
from sympy import symbols
from sympy.parsing.latex import parse_latex

CALC_ROLE = Qt.ItemDataRole.UserRole + 1
def is_only_x_variable(expr: str) -> bool:
    x = symbols('x')


    cleaned = re.sub(r'\\[A-Za-z]+', '', expr)


    letters = re.findall(r'[A-Za-z]', cleaned)


    for ch in letters:
        if ch.lower() != 'x' :

            return False


    return True

class FunctionListModel(QAbstractListModel):
    error_statusBar = pyqtSignal(str)
    function_added = pyqtSignal()
    def __init__(self, list_of_function=None):
        super().__init__()

        self._functionsList : list[str] = list_of_function or []




    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._functionsList)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        x = symbols('x')
        if role == Qt.ItemDataRole.DisplayRole:
            return self._functionsList[index.row()]
        if role == CALC_ROLE:
            print(self._functionsList[index.row()])
            return sp.lambdify(x, parse_latex(self._functionsList[index.row()]), modules="numpy")
        return None

    def add_function(self, function: str):

        func = sp.sympify(function)

        latex_func = sp.latex(func)

        if latex_func in self._functionsList: return
        if not is_only_x_variable(latex_func): return

        row = len(self._functionsList)
        self.beginInsertRows(QModelIndex(), row, row)
        self._functionsList.append(latex_func)
        self.endInsertRows()
        self.function_added.emit()


    def remove_function(self, row: int): #todo the case if no sellection is made error
        if 0 <= row < len(self._functionsList):
            self.beginRemoveRows(QModelIndex(), row, row)
            del self._functionsList[row]
            self.endRemoveRows()

