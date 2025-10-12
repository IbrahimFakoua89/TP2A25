import sys
import traceback

from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMainWindow, QLineEdit, QCheckBox, QPushButton, QLabel, QWidget, QVBoxLayout, QComboBox, \
    QGroupBox, QSlider, QRadioButton, QMenuBar, QMenu, QHBoxLayout

from canvas_view import MplCanvas
from function_model import Model


class MainView(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("ui/mainwindow.ui", self)
        self.MainWindow: QMainWindow
        self.centralwidget: QWidget
        self.main_verticalLayout : QVBoxLayout
        self.function_label: QLabel
        self.comboBox: QComboBox
        self.borne_inf_label: QLabel
        self.borne_inf_lineEdit: QLineEdit
        self.borne_sup_label: QLabel
        self.borne_sup_lineEdit: QLineEdit
        self.groupBox: QGroupBox
        self.nombre_label: QLabel
        self.label_7: QLabel
        self.horizontalSlider: QSlider
        self.gauche_radioButton: QRadioButton
        self.droite_radioButton: QRadioButton
        self.calculer_pushButton: QPushButton
        self.exporter_pushButton: QPushButton
        self.somme_label: QLabel
        self.somme_lineEdit: QLineEdit
        self.integral_label: QLabel
        self.integral_lineEdit: QLineEdit
        self.menubar: QMenuBar
        self.file_menu: QMenu
        self.fonctions_menu: QMenu
        self.verticalLayout_4: QVBoxLayout
        self.function_and_born_verticalLayout: QVBoxLayout
        self.function_horizontalLa: QHBoxLayout
        self.bornes_horizontalLayout: QHBoxLayout
        self.verticalLayout_2: QVBoxLayout
        self.options_horizontalLayout: QHBoxLayout
        self.slider_verticalLayout: QVBoxLayout
        self.outputs_horizontalLayout: QHBoxLayout
        model = Model()
        canvas = MplCanvas(model)
        self.main_verticalLayout.insertWidget(1,canvas)
        self.borne_inf_lineEdit.textChanged.connect(lambda text: setattr(model, "borne_inf", text))
        self.borne_sup_lineEdit.textChanged.connect(lambda text: setattr(model, "borne_sup", text))

    def connections(self):
        pass





if __name__ == "__main__":
    def qt_exception_hook(exctype, value, tb):
        traceback.print_exception(exctype, value, tb)


    sys.excepthook = qt_exception_hook

    app = QtWidgets.QApplication(sys.argv)
    window = MainView()
    window.show()
    app.exec()