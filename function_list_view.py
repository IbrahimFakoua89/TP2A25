from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QListView, QStyledItemDelegate, QStyle

from latex_delegate import LatexDelegate


class FunctionView(QListView):
    def __init__(self,model, parent):
        super().__init__()
        self.model = model
        self.setModel(model)
        self.parent = parent
        self.setup()
        self.setItemDelegate(LatexDelegate())

    def setup(self):
        self.parent.dock_verticalLayout.insertWidget(0,self)
        self.parent.ajouter_pushButton.clicked.connect( lambda: self.parent.list_model.add_function(self.parent.dock_lineEdit.text()))
        self.parent.supprimer_pushButton.clicked.connect(lambda: self.parent.list_model.remove_function(self.selectedIndexes()[0].row()))
        self.parent.dock_lineEdit.returnPressed.connect(self.parent.ajouter_pushButton.click)
        self.model.error_statusBar.connect(lambda message : self.parent.statusBar().showMessage(message, 3000))



