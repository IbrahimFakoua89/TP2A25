
import re

import sympy as sp
from sympy import symbols
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, pyqtSignal

from function_json import save_list_to_json, load_list_from_json
CALC_ROLE = Qt.ItemDataRole.UserRole + 1
SYMPY_CALC_ROLE = Qt.ItemDataRole.UserRole + 2
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
    def __init__(self):
        super().__init__()
        self._list_of_function_strings : list[str] =  []
        self._python_functionsList : list[str] = []
        self._simpy_functionDict  = {}
        list_of_function_from_json = load_list_from_json()

        if len(list_of_function_from_json) > 0:
            for function_string in list_of_function_from_json:
                self.add_function(function_string)





    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._python_functionsList)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        x = symbols("x")
        if role == Qt.ItemDataRole.DisplayRole:
            return self._python_functionsList[index.row()]
        if role == CALC_ROLE:

            return sp.lambdify(x, self._simpy_functionDict[self._python_functionsList[index.row()]], "numpy")
        if role == SYMPY_CALC_ROLE:
            return self._simpy_functionDict[self._python_functionsList[index.row()]]
        return None

    def add_function(self, function: str):

        try:

            func = parse_expr(function,
                          transformations=standard_transformations + (implicit_multiplication_application,),             # chatgpt aide
                          local_dict={"e": sp.E, "E": sp.E})
            latex_func = sp.latex(func)
        except:
            self.error_statusBar.emit("la fonction est invalide")
            return

        if latex_func in self._python_functionsList:
            self.error_statusBar.emit("la fonction est déja dans la liste")
            return
        if not is_only_x_variable(latex_func):
            self.error_statusBar.emit("la fonction est invalide")
            return
        self.list_of_function_strings.append(function)
        self._simpy_functionDict[latex_func] = func
        row = len(self._python_functionsList)
        self.beginInsertRows(QModelIndex(), row, row)
        self._python_functionsList.append(latex_func)
        self.endInsertRows()
        self.function_added.emit()


    def remove_function(self, selected_indexes : list[QModelIndex]):

        try:
            row =selected_indexes[0].row()
        except Exception:
            return
        if 0 <= row < len(self._python_functionsList):
            del self._simpy_functionDict[self._python_functionsList[row]]
            del self.list_of_function_strings[row]
            self.beginRemoveRows(QModelIndex(), row, row)
            del self._python_functionsList[row]
            self.endRemoveRows()
        pass


    @property
    def list_of_function_strings(self):
        return self._list_of_function_strings

    def enregister(self):
        try:
            save_list_to_json(self.list_of_function_strings, "json_file/functions.json", indent=2, ensure_ascii=False)
        except Exception as exc:
            self.error_statusBar.emit ( f" error d'enregistrement:\n{exc}")
            return
        self.error_statusBar.emit(f"Enregistré")