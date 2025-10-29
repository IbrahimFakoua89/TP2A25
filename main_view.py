
import sys
import traceback
from pathlib import Path


from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QMainWindow,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QSlider,
    QRadioButton,
    QHBoxLayout,
    QMessageBox,
    QStatusBar,
    QFileDialog, QDockWidget,
)

from main_controller import MainController

CALC_ROLE = Qt.ItemDataRole.UserRole + 1
SYMPY_CALC_ROLE = Qt.ItemDataRole.UserRole + 2


class MainView(QMainWindow):

    exporter_action: QAction
    enregistrer_pushButton: QPushButton
    statusBar: QStatusBar
    ajouter_pushButton: QPushButton
    supprimer_pushButton: QPushButton
    dock_lineEdit: QLineEdit
    function_horizontalLayout: QHBoxLayout
    horizontalSlider: QSlider
    dock_verticalLayout: QVBoxLayout
    main_verticalLayout: QVBoxLayout
    borne_inf_lineEdit: QLineEdit
    borne_sup_lineEdit: QLineEdit
    calculer_pushButton: QPushButton
    droite_radioButton: QRadioButton
    gauche_radioButton: QRadioButton
    dockWidget : QDockWidget




    def __init__(self):
        super().__init__()

        self.main_controller = None
        uic.loadUi("ui/mainwindow.ui", self)


        self.setup_models_and_delegates_and_send_to_controller()
        self.dockWidget.hide()

        self.setup_layout()


    def setup_models_and_delegates_and_send_to_controller(self):
        self.main_controller = MainController(self)


    def show_warning(self, message, type, title="Error"):
        if type == "warning":
            QMessageBox.warning(self, title, message)
        elif type == "critical":
            QMessageBox.critical(self, title, message)
        elif type == "information":
            QMessageBox.information(self, title, message)
        elif type == "statusBar":
            self.statusBar.showMessage(message, 3000)

    def setup_layout(self):
        self.main_verticalLayout.insertWidget(1, self.main_controller.canvas)
        self.function_horizontalLayout.insertWidget(1, self.main_controller.custom_comboBox)
        self.function_horizontalLayout.setStretch(1, 9)
        self.dock_verticalLayout.insertWidget(0, self.main_controller.function_list_view)
if __name__ == "__main__":
    def qt_exception_hook(exctype, value, tb):
        traceback.print_exception(exctype, value, tb)


    sys.excepthook = qt_exception_hook

    app = QtWidgets.QApplication(sys.argv)
    window = MainView()
    window.show()
    app.exec()



















