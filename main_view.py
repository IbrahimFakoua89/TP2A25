import sys
import traceback

from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QLineEdit, QCheckBox, QPushButton, QLabel, QWidget, QVBoxLayout, QComboBox, \
    QGroupBox, QSlider, QRadioButton, QMenuBar, QMenu, QHBoxLayout, QListView, QDockWidget, QMessageBox, QStatusBar
from sympy.strategies.core import switch

from canvas_view import MplCanvas
from custom_comboBox import CustomComboBox
from function_list_model import FunctionListModel
from canvas_model import Model
from function_list_view import FunctionViewList
from latex_delegate import LatexDelegate

CALC_ROLE = Qt.ItemDataRole.UserRole + 1
class MainView(QMainWindow):

    def __init__(self):
        super().__init__()
        self.function_list_view = None
        self.canvas = None
        self.latex_delegate = None
        self.custom_comboBox = None
        self.list_model = None
        self.canvas_model = None
        uic.loadUi("ui/mainwindow.ui", self)
        self.MainWindow: QMainWindow
        self.centralwidget: QWidget
        self.main_verticalLayout: QVBoxLayout
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

        self.statusBar : QStatusBar
        self.enregistrer_pushButton: QPushButton
        self.ajouter_pushButton: QPushButton
        self.supprimer_pushButton: QPushButton
        self.dock_label: QLabel
        self.dock_lineEdit: QLineEdit

        self.dockWidget.hide()
        self.setup_models_and_delegates()
        self.setup_canvas()
        self.setup_list_model()
        self.setup_comboBox()
        self.function_horizontalLayout: QHBoxLayout
        self.setup_layout()


    def setup_models_and_delegates(self):
        self.list_model = FunctionListModel()
        self.latex_delegate = LatexDelegate()
        self.canvas_model = Model()
        self.list_model = FunctionListModel()
        self.latex_delegate = LatexDelegate()

    def setup_canvas(self):
        self.canvas = MplCanvas(self.canvas_model, self)

        self.canvas_model.function_parameters_changed.connect(self.canvas.update_plot)
        self.borne_inf_lineEdit.textChanged.connect(lambda text: setattr(self.canvas_model, "borne_inf", text))
        self.borne_sup_lineEdit.textChanged.connect(lambda text: setattr(self.canvas_model, "borne_sup", text))
        self.canvas_model.show_warning.connect(lambda message, type: self.show_warning(message, type))

    def setup_list_model(self):
        self.function_list_view = FunctionViewList(self.list_model, self, self.latex_delegate)

        self.ajouter_pushButton.clicked.connect( lambda: self.list_model.add_function(self.dock_lineEdit.text()))
        self.supprimer_pushButton.clicked.connect(lambda: self.list_model.remove_function(self.function_list_view.selectedIndexes()))
        self.dock_lineEdit.returnPressed.connect(self.ajouter_pushButton.click)
        self.list_model.error_statusBar.connect(lambda message : self.show_warning(message,"statusBar"))
        # self.dock_lineEdit.setProperty("invalid", False)
        self.dock_lineEdit.style().polish(self.dock_lineEdit)



    def setup_comboBox(self):
        self.custom_comboBox = CustomComboBox(self.latex_delegate, self.list_model, self)
        self.custom_comboBox.currentIndexChanged.connect(lambda index: setattr(self.canvas_model, "function", self.custom_comboBox.model().index(index, self.custom_comboBox.modelColumn()).data( CALC_ROLE)))

        self.list_model.function_added.connect(lambda : self.custom_comboBox.setCurrentIndex(self.list_model.rowCount() - 1))

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
        self.main_verticalLayout.insertWidget(1, self.canvas)
        self.function_horizontalLayout.insertWidget(1, self.custom_comboBox)
        self.function_horizontalLayout.setStretch(1, 9)
        self.dock_verticalLayout.insertWidget(0,self.function_list_view)
if __name__ == "__main__":
    def qt_exception_hook(exctype, value, tb):
        traceback.print_exception(exctype, value, tb)


    sys.excepthook = qt_exception_hook

    app = QtWidgets.QApplication(sys.argv)
    window = MainView()
    window.show()
    app.exec()
