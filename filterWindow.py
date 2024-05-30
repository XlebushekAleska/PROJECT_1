from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QGridLayout
from PyQt5.QtCore import Qt


class Ui_Dialog_filter(QDialog):
    def __init__(self, config):
        super().__init__()
        self.setWindowTitle("Фильтры")

        self.config = config
        self.filter_widgets = {}

        self.layout = QVBoxLayout()

        self.init_ui()
        self.setLayout(self.layout)

    def init_ui(self):
        grid_layout = QGridLayout()

        if self.config == 0:
            self.create_filter_widgets(['min_price', 'max_price', 'min_count', 'max_count', 'name', 'article', 'category', 'warehouse_id'], grid_layout)
        elif self.config == 1:
            self.create_filter_widgets(['name', 'adress'], grid_layout)
        elif self.config == 2:
            self.create_filter_widgets(['first_date', 'last_date', 'status', 'first_price', 'last_price', 'name'], grid_layout)
        elif self.config == 3:
            self.create_filter_widgets(['min_orders_count' , 'max_orders_count', 'name'], grid_layout)
        elif self.config == 4:
            self.create_filter_widgets(['операция'], grid_layout)

        self.apply_button = QPushButton("Применить")
        self.clear_button = QPushButton("Очистить")
        self.clear_button.setFocusPolicy(Qt.NoFocus)
        self.apply_button.clicked.connect(self.apply_filters)
        self.clear_button.clicked.connect(self.clear_filters)

        self.layout.addLayout(grid_layout)
        self.layout.addWidget(self.clear_button)
        self.layout.addWidget(self.apply_button)

    def create_filter_widgets(self, filter_names, layout):
        row = 0
        for filter_name in filter_names:
            if 'min' in filter_name or "first" in filter_name:
                if 'min' in filter_name:
                    lb_text = filter_name.replace("min_", " ") + " from"
                else:
                    lb_text = filter_name.replace("first_", " ") + " from"
                label_from = QLabel(lb_text.replace('_', ' '))
                line_edit_min = QLineEdit()
                label_to = QLabel("to")
                line_edit_max = QLineEdit()
                layout.addWidget(label_from, row, 1)
                layout.addWidget(line_edit_min, row, 2)
                layout.addWidget(label_to, row, 3)
                layout.addWidget(line_edit_max, row, 4)
                self.filter_widgets[filter_name] = (line_edit_min, line_edit_max)
            elif 'max' in filter_name or 'last_' in filter_name:
                continue
            else:
                label = QLabel(filter_name.replace('_', ' '))
                label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                line_edit = QLineEdit()
                layout.addWidget(label, row, 0, 1, 2)
                layout.addWidget(line_edit, row, 2, 1, 4)
                self.filter_widgets[filter_name] = line_edit
            row += 1

    def apply_filters(self):
        filters = {}
        for filter_name, widget in self.filter_widgets.items():
            if isinstance(widget, tuple):
                line_edit_min, line_edit_max = widget
                if line_edit_min.text() != "":
                    filters[filter_name] = line_edit_min.text()
                if line_edit_max.text() != "":
                    if "min" in filter_name:
                        max_name = filter_name.replace("min_", "max_")
                    else:
                        max_name = filter_name.replace("first_", "last_")
                    filters[max_name] = line_edit_max.text()
            else:
                if widget.text() != "":
                    filters[filter_name] = widget.text()

        print(filters)
        self.finish_filter = filters
        self.accept()

    def clear_filters(self):
        for widget in self.filter_widgets.values():
            if isinstance(widget, tuple):
                line_edit_min, line_edit_max = widget
                line_edit_min.clear()
                line_edit_max.clear()
            else:
                widget.clear()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    dialog = Ui_Dialog_filter(0)
    dialog.exec_()
