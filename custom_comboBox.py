
from PyQt6.QtWidgets import QComboBox, QStylePainter, QStyleOptionComboBox, QStyle




class CustomComboBox(QComboBox):
    def __init__(self, delegate,model, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.delegate = delegate
        self.setItemDelegate(delegate)
        self.setModel(model)
        self.parent = parent

        self.setStyleSheet("""
        
        QComboBox {
            background-color: #222;
            color: white;
            padding: 6px 30px 6px 8px; 
            border: 1px solid #555;
            border-radius: 6px;
        }

        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px; 
            border-left: 1px solid #444;
            background-color: #333;
        }


""")



    def paintEvent(self, e):
        painter = QStylePainter(self)  # self = QComboBox
        opt = QStyleOptionComboBox()
        self.initStyleOption(opt)

        painter.drawComplexControl(QStyle.ComplexControl.CC_ComboBox, opt)

        index = self.model().index(self.currentIndex(), self.modelColumn())

        self.delegate.paint(painter, opt, index)
