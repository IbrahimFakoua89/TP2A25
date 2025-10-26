
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
    QFileDialog,
)


from canvas_model import Model
from canvas_view import MplCanvas
from custom_comboBox import CustomComboBox
from function_list_model import FunctionListModel
from function_list_view import FunctionViewList
from latex_delegate import LatexDelegate

CALC_ROLE = Qt.ItemDataRole.UserRole + 1
SYMPY_CALC_ROLE = Qt.ItemDataRole.UserRole + 2


class MainView(QMainWindow):
    exporter_action: QAction
    canvas_model: Model
    enregistrer_pushButton: QPushButton
    statusBar: QStatusBar
    ajouter_pushButton: QPushButton
    supprimer_pushButton: QPushButton
    dock_lineEdit: QLineEdit
    function_horizontalLayout: QHBoxLayout
    horizontalSlider: QSlider
    dock_verticalLayout: QVBoxLayout
    main_verticalLayout: QVBoxLayout
    custom_comboBox: CustomComboBox
    function_list_view: FunctionViewList
    canvas: MplCanvas
    latex_delegate: LatexDelegate
    borne_inf_lineEdit: QLineEdit
    borne_sup_lineEdit: QLineEdit
    calculer_pushButton: QPushButton
    droite_radioButton: QRadioButton
    gauche_radioButton: QRadioButton
    list_model: FunctionListModel


    def __init__(self):
        super().__init__()


        uic.loadUi("ui/mainwindow.ui", self)

        self.dockWidget.hide()
        self.setup_models_and_delegates()
        self.setup_canvas()
        self.setup_list_model()
        self.setup_comboBox()
        self.setup_integration()
        self.exporter()
        self.setup_layout()

    def on_export_clicked(self):
        fig = self.canvas.figure

        file_filter = "PNG Files (*.png);;All Files (*)"

        filename, _ = QFileDialog.getSaveFileName(self, "Enregistrer l'image PNG", str(Path.home() / "plot.png"),
                                                  file_filter)  # chatgpt
        if not filename:
            return

        try:
            fig.savefig(filename)
        except Exception as exc:
            QMessageBox.critical(self, "Erreur", f"Erreur d'exportation:\n{exc}")
            return

        QMessageBox.information(self, "Exporté", "L'image a été enregistrée avec succès ")

    def exporter(self):
        self.enregistrer_pushButton.clicked.connect(self.list_model.enregister)

    def setup_integration(self):

        self.droite_radioButton.toggled.connect(
            lambda state: setattr(self.canvas_model, "radioButton_state", "droite") if state is True else None)
        self.gauche_radioButton.toggled.connect(
            lambda state: setattr(self.canvas_model, "radioButton_state", "gauche") if state is True else None)

        self.horizontalSlider.valueChanged.connect(
            lambda number: setattr(self.canvas_model, "nombre_de_rectangle", number))
        self.canvas_model.rectangle_parameters_changed.connect(
            lambda rectangles: self.canvas.draw_rectangles(rectangles))
        self.canvas_model.integral_result_changed.connect(lambda result: self.integral_lineEdit.setText(result))
        self.canvas_model.riemann_result_changed.connect(lambda result: self.somme_lineEdit.setText(result))
        self.calculer_pushButton.clicked.connect(self.canvas_model.on_clicked_integral)
        self.canvas_model.clear_rectangles.connect(lambda: self.canvas.update_plot(clear=True))

    def setup_models_and_delegates(self):
        self.canvas_model = Model()
        self.list_model = FunctionListModel()
        self.latex_delegate = LatexDelegate()

    def setup_canvas(self):
        self.canvas = MplCanvas(self.canvas_model, self)

        self.canvas_model.function_parameters_changed.connect(self.canvas.update_plot)
        self.borne_inf_lineEdit.textChanged.connect(lambda text: setattr(self.canvas_model, "borne_inf", text))
        self.borne_sup_lineEdit.textChanged.connect(lambda text: setattr(self.canvas_model, "borne_sup", text))
        self.canvas_model.show_warning.connect(lambda message, type: self.show_warning(message, type))
        self.exporter_action.triggered.connect(self.on_export_clicked)

    def setup_list_model(self):
        self.function_list_view = FunctionViewList(self.list_model, self, self.latex_delegate)

        self.ajouter_pushButton.clicked.connect(lambda: self.list_model.add_function(self.dock_lineEdit.text()))
        self.supprimer_pushButton.clicked.connect(
            lambda: self.list_model.remove_function(self.function_list_view.selectedIndexes()))
        self.dock_lineEdit.returnPressed.connect(self.ajouter_pushButton.click)
        self.list_model.error_statusBar.connect(lambda message: self.show_warning(message, "statusBar"))
        self.dock_lineEdit.style().polish(self.dock_lineEdit)

    def setup_comboBox(self):
        self.custom_comboBox = CustomComboBox(self.latex_delegate, self.list_model, self)
        self.custom_comboBox.currentIndexChanged.connect(self.comboxBox_currenctIndexChanged)

        self.list_model.function_added.connect(
            lambda: self.custom_comboBox.setCurrentIndex(self.list_model.rowCount() - 1))
        self.comboxBox_currenctIndexChanged(self.custom_comboBox.currentIndex())

    def comboxBox_currenctIndexChanged(self, index):
        self.canvas_model.function = self.custom_comboBox.model().index(index, self.custom_comboBox.modelColumn()).data(
            CALC_ROLE)
        self.canvas_model.sympy_function = self.custom_comboBox.model().index(index,
                                                                              self.custom_comboBox.modelColumn()).data(
            SYMPY_CALC_ROLE)

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
        self.dock_verticalLayout.insertWidget(0, self.function_list_view)


if __name__ == "__main__":
    def qt_exception_hook(exctype, value, tb):
        traceback.print_exception(exctype, value, tb)


    sys.excepthook = qt_exception_hook

    app = QtWidgets.QApplication(sys.argv)
    window = MainView()
    window.show()
    app.exec()
