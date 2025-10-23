import sys
import traceback

from PyQt6.QtWidgets import QStyledItemDelegate, QApplication, QListView, QStyle
from PyQt6.QtGui import QPixmap, QPainter, QColor
from PyQt6.QtCore import QSize, Qt, QStringListModel
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import io
from PyQt6.QtGui import QPixmap



class LatexDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cache = {}

    def render_latex(self, formula: str, dpi=100) -> QPixmap:
        fig = plt.figure(figsize=(0.01, 0.01))
        t = fig.text(0.5, 0.5, f"${formula}$", fontsize=14, color="white",ha="center", va="center")
        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        bbox = t.get_window_extent(renderer=canvas.get_renderer())
        width, height = bbox.size / dpi

        fig.set_size_inches(width, height + 0.4)
        t.set_position((0.5, 0.5))
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=dpi, transparent=True)

        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())
        plt.close(fig)
        return pixmap

    def paint(self, painter, option, index):

        formula = index.data(Qt.ItemDataRole.DisplayRole)
        if not formula:
            return
        if option.state & QStyle.StateFlag.State_Selected:

            painter.setPen(QColor("white"))
            painter.drawRect(option.rect.adjusted(0, 0, -1, -1))

        pixmap = self.cache.get(formula)
        if pixmap is None:
            pixmap = self.render_latex(formula)
            self.cache[formula] = pixmap

        rect = option.rect
        x = rect.x() + (rect.width() - pixmap.width()) // 2
        y = rect.y() + (rect.height() - pixmap.height()) // 2
        painter.drawPixmap(x, y, pixmap)

    def sizeHint(self, option, index):

        formula = index.data(Qt.ItemDataRole.DisplayRole)

        pixmap = self.cache.get(formula)

        if pixmap:
            return QSize(pixmap.width(), pixmap.height())
        else:
            pixmap = self.render_latex(formula)
            self.cache[formula] = pixmap
            return QSize(pixmap.width(), pixmap.height())


