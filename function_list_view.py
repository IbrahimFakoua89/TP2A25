
from PyQt6.QtWidgets import QListView




class FunctionViewList(QListView):
    def __init__(self,model, parent, delegate):
        super().__init__()
        self.model = model
        self.setModel(model)
        self.parent = parent

        self.setItemDelegate(delegate)








