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
        self.view = view
        self.canvas_model = Model()
        self.canvas = MplCanvas(self.canvas_model, self)
        self.list_model = FunctionListModel()
        self.latex_delegate = LatexDelegate()
        self.function_list_view = FunctionViewList(self.list_model, self.view, self.latex_delegate)
        self.custom_comboBox = CustomComboBox(self.latex_delegate, self.list_model, self.view)


        self.setup_canvas()
        self.setup_list_model()
        self.setup_comboBox()
        self.setup_integration()
        self.exporter()


    def setup_integration(self):
        self.view.droite_radioButton.toggled.connect(
            lambda state: setattr(self.canvas_model, "radioButton_state", "droite") if state is True else None)
        self.view.gauche_radioButton.toggled.connect(
            lambda state: setattr(self.canvas_model, "radioButton_state", "gauche") if state is True else None)

        self.view.horizontalSlider.valueChanged.connect(
            lambda number: setattr(self.canvas_model, "nombre_de_rectangle", number))
        self.canvas_model.rectangle_parameters_changed.connect(
            lambda rectangles: self.canvas.draw_rectangles(rectangles))
        self.canvas_model.integral_result_changed.connect(lambda result: self.view.integral_lineEdit.setText(result))
        self.canvas_model.riemann_result_changed.connect(lambda result: self.view.somme_lineEdit.setText(result))
        self.view.calculer_pushButton.clicked.connect(self.canvas_model.on_clicked_integral)
        self.canvas_model.clear_rectangles.connect(lambda: self.canvas.update_plot(clear=True))

    def setup_canvas(self):
        self.canvas_model.function_parameters_changed.connect(self.canvas.update_plot)
        self.view.borne_inf_lineEdit.textChanged.connect(lambda text: setattr(self.canvas_model, "borne_inf", text))
        self.view.borne_sup_lineEdit.textChanged.connect(lambda text: setattr(self.canvas_model, "borne_sup", text))
        self.canvas_model.show_warning.connect(lambda message, type: self.view.show_warning(message, type))
        self.view.exporter_action.triggered.connect(self.on_export_clicked)

    def setup_list_model(self):
        self.view.ajouter_pushButton.clicked.connect(lambda: self.list_model.add_function(self.view.dock_lineEdit.text()))
        self.view.supprimer_pushButton.clicked.connect(
            lambda: self.list_model.remove_function(self.function_list_view.selectedIndexes()))
        self.view.dock_lineEdit.returnPressed.connect(self.view.ajouter_pushButton.click)
        self.list_model.error_statusBar.connect(lambda message: self.view.show_warning(message, "statusBar"))
        self.view.dock_lineEdit.style().polish(self.view.dock_lineEdit)

    def setup_comboBox(self):
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
    def exporter(self):
        self.view.enregistrer_pushButton.clicked.connect(self.list_model.enregister)

    def on_export_clicked(self):
        fig = self.canvas.figure


        file_filter = "PNG Files (*.png);;All Files (*)"

        filename, _ = QFileDialog.getSaveFileName(self.view, "Enregistrer l'image PNG", str(Path.home() / "plot.png"),
                                                  file_filter)  # chatgpt
        if not filename:
            return

        try:
            fig.savefig(filename)
        except Exception as exc:
            self.view.show_warning( f"Erreur d'exportation:\n{exc}","critique","Erreur")
            return

        self.view.show_warning( "L'image a été enregistrée avec succès ","information","Exporté")




