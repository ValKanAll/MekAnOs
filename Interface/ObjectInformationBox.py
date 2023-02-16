from PyQt5.QtGui import QFont, QBrush, QColor
from PyQt5.Qt import QGroupBox, QTableWidget, QTableWidgetItem, QTreeWidget, QTreeWidgetItem, QVBoxLayout
from PyQt5.QtCore import QMargins


class ObjectInformationBox(QGroupBox):
    def __init__(self, parent=None):
        super(ObjectInformationBox, self).__init__(parent)

        self.setTitle("Object information")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.layout.setSpacing(0)

        # create Tree with object info
        self.objectInfoTree = QTreeWidget()
        font_objectInfoTree = QFont()
        font_objectInfoTree.setPointSize(11)
        self.objectInfoTree.setFont(font_objectInfoTree)
        self.objectInfoTree.setMinimumHeight(250)
        self.objectInfoTree.setMinimumWidth(450)
        self.objectInfoTree.setColumnCount(3)
        self.objectInfoTree.setColumnWidth(0, 200)
        self.objectInfoTree.setColumnWidth(1, 300)
        self.objectInfoTree.setColumnWidth(2, 95)
        self.objectInfoTree.setAlternatingRowColors(True)
        self.objectInfoTree.header().hide()

        self.layout.addWidget(self.objectInfoTree)

    def fill(self, object):
        self.objectInfoTree.clear()
        info_list = object.get_infos()
        for info in info_list:
            category_tree = QTreeWidgetItem(self.objectInfoTree, [info[0], str(len(info[2]))])
            category_tree.setExpanded(True)
            category_tree.setForeground(0, QBrush(QColor("#000000")))
            category_tree.setExpanded(info[1])
            for sub_info in info[2]:
                if type(sub_info[-1]) == list:
                    sub_tree = QTreeWidgetItem(category_tree, [sub_info[0]])
                    sub_tree.setForeground(0, QBrush(QColor("#666666")))
                    sub_tree.setExpanded(sub_info[1])
                    for sub_sub_info in sub_info[2]:
                        sub_sub_tree = QTreeWidgetItem(sub_tree, sub_sub_info)
                        sub_sub_tree.setForeground(0, QBrush(QColor("#666666")))
                        sub_sub_tree.setForeground(1, QBrush(QColor("#666666")))
                        try:
                            sub_sub_tree.setForeground(2, QBrush(QColor("#666666")))
                        except (ValueError, AttributeError, IndexError):
                            pass
                else:
                    sub_tree = QTreeWidgetItem(category_tree, sub_info)
                    sub_tree.setForeground(0, QBrush(QColor("#666666")))
                    sub_tree.setForeground(1, QBrush(QColor("#666666")))
                try:
                    sub_tree.setForeground(2, QBrush(QColor("#666666")))
                except (ValueError, AttributeError, IndexError):
                    pass
