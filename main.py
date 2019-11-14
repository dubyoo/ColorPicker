# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication
import ColorPicker

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = ColorPicker.ColorPicker()
    main_window.show()
    sys.exit(app.exec_())

