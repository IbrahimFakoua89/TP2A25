from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog

from canvas_model import Model
from canvas_view import MplCanvas
from custom_comboBox import CustomComboBox
from function_list_model import FunctionListModel
from function_list_view import FunctionViewList
from latex_delegate import LatexDelegate

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_view import MainView

CALC_ROLE = Qt.ItemDataRole.UserRole + 1
SYMPY_CALC_ROLE = Qt.ItemDataRole.UserRole + 2
view : "MainView"


custom_comboBox: CustomComboBox
function_list_view: FunctionViewList
canvas: MplCanvas
canvas_model: Model
latex_delegate: LatexDelegate
list_model: FunctionListModel
class MainController:
    def __init__(self, view : "MainView"):
        self.__view = view
        self.__canvas_model = Model()
        self.__canvas = MplCanvas(self.__canvas_model, self)
        self.__list_model = FunctionListModel()
        self.__latex_delegate = LatexDelegate()
        self.__function_list_view = FunctionViewList(self.__list_model, self.__view, self.__latex_delegate)
        self.__custom_comboBox = CustomComboBox(self.__latex_delegate, self.__list_model, self.__view)


        self.setup_canvas()
        self.setup_list_model()
        self.setup_comboBox()
        self.setup_integration()
        self.exporter()


    def setup_integration(self):
        self.__view.droite_radioButton.toggled.connect(
            lambda state: setattr(self.__canvas_model, "radioButton_state", "droite") if state is True else None)
        self.__view.gauche_radioButton.toggled.connect(
            lambda state: setattr(self.__canvas_model, "radioButton_state", "gauche") if state is True else None)

        self.__view.horizontalSlider.valueChanged.connect(
            lambda number: setattr(self.__canvas_model, "nombre_de_rectangle", number))
        self.__canvas_model.rectangle_parameters_changed.connect(
            lambda rectangles: self.__canvas.draw_rectangles(rectangles))
        self.__canvas_model.integral_result_changed.connect(lambda result: self.__view.integral_lineEdit.setText(result))
        self.__canvas_model.riemann_result_changed.connect(lambda result: self.__view.somme_lineEdit.setText(result))
        self.__view.calculer_pushButton.clicked.connect(self.__canvas_model.on_clicked_integral)
        self.__canvas_model.clear_rectangles.connect(lambda: self.__canvas.update_plot(clear=True))

    def setup_canvas(self):
        self.__canvas_model.function_parameters_changed.connect(self.__canvas.update_plot)
        self.__view.borne_inf_lineEdit.textChanged.connect(lambda text: setattr(self.__canvas_model, "borne_inf", text))
        self.__view.borne_sup_lineEdit.textChanged.connect(lambda text: setattr(self.__canvas_model, "borne_sup", text))
        self.__canvas_model.show_warning.connect(lambda message, type: self.__view.show_warning(message, type))
        self.__view.exporter_action.triggered.connect(self.on_export_clicked)

    def setup_list_model(self):
        self.__view.ajouter_pushButton.clicked.connect(lambda: self.__list_model.add_function(self.__view.dock_lineEdit.text()))
        self.__view.supprimer_pushButton.clicked.connect(
            lambda: self.__list_model.remove_function(self.__function_list_view.selectedIndexes()))
        self.__view.dock_lineEdit.returnPressed.connect(self.__view.ajouter_pushButton.click)
        self.__list_model.error_statusBar.connect(lambda message: self.__view.show_warning(message, "statusBar"))
        self.__view.dock_lineEdit.style().polish(self.__view.dock_lineEdit)

    def setup_comboBox(self):
        self.__custom_comboBox.currentIndexChanged.connect(self.comboxBox_currenctIndexChanged)

        self.__list_model.function_added.connect(
            lambda: self.__custom_comboBox.setCurrentIndex(self.__list_model.rowCount() - 1))
        self.comboxBox_currenctIndexChanged(self.__custom_comboBox.currentIndex())

    def comboxBox_currenctIndexChanged(self, index):
        self.__canvas_model.function = self.__custom_comboBox.model().index(index, self.__custom_comboBox.modelColumn()).data(
            CALC_ROLE)
        self.__canvas_model.sympy_function = self.__custom_comboBox.model().index(index,
                                                                                  self.__custom_comboBox.modelColumn()).data(
            SYMPY_CALC_ROLE)
    def exporter(self):
        self.__view.enregistrer_pushButton.clicked.connect(self.__list_model.enregister)

    def on_export_clicked(self):
        fig = self.__canvas.figure


        file_filter = "PNG Files (*.png);;All Files (*)"

        filename, _ = QFileDialog.getSaveFileName(self.__view, "Enregistrer l'image PNG", str(Path.home() / "plot.png"),
                                                  file_filter)  # chatgpt
        if not filename:
            return

        try:
            fig.savefig(filename)
        except Exception as exc:
            self.__view.show_warning(f"Erreur d'exportation:\n{exc}", "critique", "Erreur")
            return

        self.__view.show_warning("L'image a été enregistrée avec succès ", "information", "Exporté")




