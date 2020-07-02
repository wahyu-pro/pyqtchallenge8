from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QAbstractListModel
import sys

import qtmodern.styles
import qtmodern.windows

class ListModel(QAbstractListModel):
    def __init__(self, datalist):
        super(ListModel, self).__init__()
        self.datalists = datalist

    def data(self, index, role):
        if role == Qt.DisplayRole:
            text = self.datalists[index.row()]
            return text

    def rowCount(self, index):
        result = len(self.datalists)
        return result


class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.mainUI()
        self.layoutVertical()
        self.setCentralWidget(self.setWidget)

    def mainUI(self):
        self.list = QListView()
        self.model = ListModel(datalist=[])
        self.list.setModel(self.model)
        self.btnAdd = QPushButton("Add")
        self.btnAdd.clicked.connect(self.addItem)
        self.buttonRemove = QPushButton("Remove")
        self.buttonRemove.clicked.connect(self.removeItems)
        self.btnClear = QPushButton("Clear")
        self.btnClear.clicked.connect(self.clear)
        self.btnUpdate = QPushButton("Update")
        self.btnUpdate.clicked.connect(self.update)
        self.btnDuplicate = QPushButton("Duplicate")
        self.btnDuplicate.clicked.connect(self.duplicate)

        # Slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.valueChanged.connect(self.valueSlider)

        # progressbar
        self.progressBar = QProgressBar()

    def layoutVertical(self):
        self.layoutList = QVBoxLayout()
        self.layoutList.addWidget(self.list)
        self.layoutList.addWidget(self.layoutHorizontal())
        self.layoutList.addWidget(self.slider)
        self.layoutList.addWidget(self.progressBar)

        self.setWidget = QWidget()
        self.setWidget.setLayout(self.layoutList)

    def layoutHorizontal(self):
        self.LayoutH = QHBoxLayout()
        self.LayoutH.addWidget(self.btnAdd)
        self.LayoutH.addWidget(self.buttonRemove)
        self.LayoutH.addWidget(self.btnClear)
        self.LayoutH.addWidget(self.btnUpdate)
        self.LayoutH.addWidget(self.btnDuplicate)

        self.widgetH = QWidget()
        self.widgetH.setLayout(self.LayoutH)
        return self.widgetH

    def addItem(self):
        add, ok = QInputDialog.getText(self, "Add item", "Add list item")
        if add != "" and ok == True:
            self.model.datalists.append(add)
            self.model.layoutChanged.emit()

        self.progressBar.setValue(len(self.model.datalists))

    def removeItems(self):
        index = self.list.selectedIndexes()
        if not index:
            QMessageBox.warning(self, "Warning", "Please select item !")
        else:
            indexes = index[0]
            del self.model.datalists[indexes.row()]
            self.model.layoutChanged.emit()
            self.progressBar.setValue(len(self.model.datalists))

    def clear(self):
        self.model.datalists.clear()
        self.model.layoutChanged.emit()
        self.progressBar.setValue(len(self.model.datalists))

    def update(self):
        index = self.list.selectedIndexes()
        if not index:
            QMessageBox.warning(self, "Warning", "Please select item !")
        else:
            selected = self.model.datalists[index[0].row()]
            update, ok = QInputDialog.getText(self, "Add item", "Add list item", text=selected)
            self.model.datalists[index[0].row()] = update
            self.model.layoutChanged.emit()

    def valueSlider(self):
        value = self.slider.value()
        return value

    def duplicate(self):
        value = self.valueSlider()
        index = self.list.selectedIndexes()
        if not index:
            QMessageBox.warning(self, "Warning", "Please select item !")
        else:
            results = self.model.datalists[index[0].row()]
            for x in range(value):
                self.model.datalists.append(results)
                self.model.layoutChanged.emit()

            self.progressBar.setValue(len(self.model.datalists))


if __name__ == "__main__":
    app = QApplication([])
    window = MyApp()
    qtmodern.styles.light(app)
    theme = qtmodern.windows.ModernWindow(window)
    theme.show()
    app.exec_()