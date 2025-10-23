import sys
import traceback

from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QLineEdit, QCheckBox, QPushButton, QLabel, QWidget, QVBoxLayout, QComboBox, \
    QGroupBox, QSlider, QRadioButton, QMenuBar, QMenu, QHBoxLayout, QListView, QDockWidget, QMessageBox

from canvas_view import MplCanvas
from custom_comboBox import CustomComboBox
from function_list_model import FunctionListModel
from graph_model import Model
from function_list_view import FunctionView
from latex_delegate import LatexDelegate

CALC_ROLE = Qt.ItemDataRole.UserRole + 1
class MainView(QMainWindow):

    def __init__(self):
        super().__init__()
        self.canvas = None
        self.latex_delegate = None
        self.custom_comboBox = None
        self.list_model = None
        self.canvas_model = None
        uic.loadUi("ui/mainwindow.ui", self)
        self.MainWindow: QMainWindow
        self.centralwidget: QWidget
        self.main_verticalLayout : QVBoxLayout
        self.function_label: QLabel
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
        self.dockWidget: QDockWidget
        self.dockWidgetContents: QWidget
        self.dock_verticalLayout: QVBoxLayout

        self.enregistrer_pushButton: QPushButton
        self.ajouter_pushButton: QPushButton
        self.supprimer_pushButton: QPushButton
        self.dock_label: QLabel
        self.dock_lineEdit: QLineEdit

        self.connections_model()
        self.connections_list_model()
        self.setup_comboBox()
        self.function_horizontalLayout : QHBoxLayout






    def connections_model(self):
        self.canvas_model = Model()
        self.canvas = MplCanvas(self.canvas_model)
        self.main_verticalLayout.insertWidget(1,self.canvas)
        self.canvas_model.function_parameters_changed.connect(self.canvas.update_plot)
        self.borne_inf_lineEdit.textChanged.connect(lambda text: setattr(self.canvas_model, "borne_inf", text))
        self.borne_sup_lineEdit.textChanged.connect(lambda text: setattr(self.canvas_model, "borne_sup", text))

    def connections_list_model(self):

        self.list_model = FunctionListModel()
        self.latex_delegate = LatexDelegate()
        function_view = FunctionView(self.list_model, self, self.latex_delegate)




    def setup_comboBox(self):
        self.custom_comboBox = CustomComboBox(self.latex_delegate)
        self.custom_comboBox.setModel(self.list_model)
        self.function_horizontalLayout.insertWidget(1,self.custom_comboBox)
        self.function_horizontalLayout.setStretch(1,9)

        self.custom_comboBox.currentIndexChanged.connect(lambda index: setattr(self.canvas_model, "function", self.custom_comboBox.model().index(index, self.custom_comboBox.modelColumn()).data( CALC_ROLE)))




        # QMessageBox.warning(self, "Invalid Input", "Function cannot be empty.")
        # # QMessageBox.critical(self, "Error", "Something went wrong.")
        # QMessageBox.information(self, "Done", "Function added successfully!")
        # self.statusBar().showMessage("Function already in list.", 3000)
        # self.feedback_label.setText("Already exists!")
        # self.feedback_label.setStyleSheet("color: orange;")


if __name__ == "__main__":
    def qt_exception_hook(exctype, value, tb):
        traceback.print_exception(exctype, value, tb)


    sys.excepthook = qt_exception_hook

    app = QtWidgets.QApplication(sys.argv)
    window = MainView()
    window.show()
    app.exec()