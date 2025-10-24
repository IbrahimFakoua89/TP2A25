
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, pyqtSignal
import sympy as sp
import re
from sympy import symbols
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

CALC_ROLE = Qt.ItemDataRole.UserRole + 1
def is_only_x_variable(expr: str) -> bool:
    x = symbols('x')


    cleaned = re.sub(r'\\[A-Za-z]+', '', expr)


    letters = re.findall(r'[A-DF-Za-df-z]', cleaned)

    x_is_found = False
    for ch in letters:
        if ch.lower() != 'x' :  return False
        if ch.lower() == 'x': x_is_found = True




    return True and x_is_found

class FunctionListModel(QAbstractListModel):
    error_statusBar = pyqtSignal(str)
    function_added = pyqtSignal()
    def __init__(self, list_of_function=None):
        super().__init__()

        self._functionsList : list[str] = list_of_function or []
        self._simpy_functionDict  = {}         # todo buth





    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._functionsList)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        x = symbols("x")
        if role == Qt.ItemDataRole.DisplayRole:
            return self._functionsList[index.row()]
        if role == CALC_ROLE:
            return sp.lambdify(x,self._simpy_functionDict[self._functionsList[index.row()]],"numpy")
        return None

    def add_function(self, function: str):

        func = parse_expr(function,
                          transformations=standard_transformations + (implicit_multiplication_application,),
                          local_dict={"e": sp.E, "E": sp.E})
        latex_func = sp.latex(func)
        # print(f"func {func}" , f"funcType {type(func)}")
        # print(f"latex_func  {latex_func}")
        if latex_func in self._functionsList: return
        if not is_only_x_variable(latex_func): return
        self._simpy_functionDict[latex_func] = func
        row = len(self._functionsList)
        self.beginInsertRows(QModelIndex(), row, row)
        self._functionsList.append(latex_func)
        self.endInsertRows()
        self.function_added.emit()


    def remove_function(self, selected_indexes : list[QModelIndex]):

        try:
            row =selected_indexes[0].row()
        except Exception:
            return
        if 0 <= row < len(self._functionsList):
            del self._simpy_functionDict[self._functionsList[row]]
            self.beginRemoveRows(QModelIndex(), row, row)
            del self._functionsList[row]
            self.endRemoveRows()
        pass
