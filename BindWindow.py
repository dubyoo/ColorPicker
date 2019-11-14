# -*- coding: utf-8 -*-
import win32gui
from PyQt5.QtWidgets import QWidget
import ui_bind_window


def get_widows_information(hwnd, window_list):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd)
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]
        y = rect[1]
        if x != -32000 and y != -32000 and title != '':
            window_list.append(WindowInformation(title, rect))


class WindowInformation:
    def __init__(self, title='', rect=()):
        self.title = title
        self.rect = rect


class BindWindow(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)
        self.ui = ui_bind_window.Ui_BindWindow()
        self.ui.setupUi(self)
        self.parent_window = parent
        self.window_list = []

    def show(self):
        super().hide()
        super().show()
        self.ui.listWidget.clear()
        self.get_windows()

        for i in range(len(self.window_list)):
            title = show_title = self.window_list[i].title
            if len(title) > 35:
                show_title = title[:15] + ' ... ' + title[-15:]
            self.ui.listWidget.addItem(show_title)
            rect = self.window_list[i].rect
            tooltip = title + '\n' + 'x = %d, y = %d, width = %d, height = %d' % (rect[0], rect[1], rect[2], rect[3])
            self.ui.listWidget.item(i).setToolTip(tooltip)

        self.ui.listWidget.doubleClicked.connect(self.check_item)

    def get_windows(self):
        self.window_list.clear()
        win32gui.EnumWindows(get_widows_information, self.window_list)

    def check_item(self, item):
        self.parent_window.on_window_selected(self.window_list[item.row()])
        self.hide()

    def closeEvent(self, close_event):
        super().close()
        self.parent_window.on_window_selected(None)
