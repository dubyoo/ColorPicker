# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QGuiApplication, QColor, QCursor, QPainter, QPen
from PyQt5.QtWidgets import QWidget, QApplication, QComboBox
import ui_color_picker
import win32api
import win32gui


def get_widows_information(hwnd, window_list):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd)
        rect = win32gui.GetClientRect(hwnd)
        x, y = win32gui.ClientToScreen(hwnd, (rect[0], rect[1]))
        client_rect = (x, y, rect[2], rect[3])
        if x != -32000 and y != -32000 and title != '':
            window_list.append(WindowInformation(title, client_rect))


class WindowInformation:
    def __init__(self, title='', rect=()):
        self.title = title
        self.client_rect = rect


class ColorPicker(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = ui_color_picker.Ui_ColorPicker()
        self.ui.setupUi(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.capture_mouse)
        self.timer.start(100)
        self.ui.comboBox.currentIndexChanged.connect(self.on_window_selected)
        self.window_list = []
        self.client_rect = None
        self.current_color = None
        self.current_point = None
        self.pix_map = None

    def capture_mouse(self):
        point = QCursor.pos()
        self.pix_map = QGuiApplication.primaryScreen().grabWindow(
            QApplication.desktop().winId(), point.x() - 25, point.y() - 25, 51, 51)
        if not self.pix_map.isNull():
            image = self.pix_map.toImage()
            if not image.isNull():
                color = QColor(image.pixel(25, 25))
                r, g, b, _ = color.getRgb()
                self.current_color = color
                self.current_point = point
                self.ui.label_color_value.setText('%s' % color.name().upper())
                self.ui.label_absolute_pos_value.setText('%d, %d' % (point.x(), point.y()))
                if self.client_rect is not None:
                    relative_x = point.x() - self.client_rect[0]
                    relative_y = point.y() - self.client_rect[1]
                    self.ui.label_relative_pos_value.setText('%d, %d' % (relative_x, relative_y))
                self.ui.label_rgb_value.setText('%d, %d, %d' % (r, g, b))
                self.zoom_display()

    def zoom_display(self):
        painter = QPainter(self.pix_map)
        painter.drawPixmap(self.pix_map.rect(), self.pix_map)
        painter.setPen(QPen(QColor(144, 238, 144, 90), 1, Qt.SolidLine))
        painter.drawLine(0, 25, 50, 26)
        painter.drawLine(25, 0, 25, 50)
        pix_map_resized = self.pix_map.scaled(204, 204)
        self.ui.label_display.setPixmap(pix_map_resized)

    def keyReleaseEvent(self, event):
        if event.modifiers() != Qt.ControlModifier:
            return

        line_edit = None
        x = self.current_point.x()
        y = self.current_point.y()

        if event.key() == Qt.Key_Left:
            win32api.SetCursorPos((x - 1, y))
        elif event.key() == Qt.Key_Right:
            win32api.SetCursorPos((x + 1, y))
        elif event.key() == Qt.Key_Up:
            win32api.SetCursorPos((x, y - 1))
        elif event.key() == Qt.Key_Down:
            win32api.SetCursorPos((x, y + 1))
        elif event.key() == Qt.Key_1:
            line_edit = self.ui.lineEdit_ctrl_1
        elif event.key() == Qt.Key_2:
            line_edit = self.ui.lineEdit_ctrl_2
        elif event.key() == Qt.Key_3:
            line_edit = self.ui.lineEdit_ctrl_3
        elif event.key() == Qt.Key_4:
            line_edit = self.ui.lineEdit_ctrl_4
        elif event.key() == Qt.Key_5:
            line_edit = self.ui.lineEdit_ctrl_5

        if line_edit is not None:
            r, g, b, _ = self.current_color.getRgb()
            color_name = self.current_color.name().upper()
            text_color = QColor(255 - r, 255 - g, 255 - b)
            text_color_name = text_color.name().upper()

            if self.client_rect is not None:
                x = x - self.client_rect[0]
                y = y - self.client_rect[1]
            line_edit.setText('[%d, %d] (%d, %d, %d) %s' % (x, y, r, g, b, color_name))
            line_edit.setStyleSheet('QLineEdit{border:1px solid %s; color:%s; background-color:%s}'
                                    % (color_name, text_color_name, color_name))

    def get_window_list(self):
        self.window_list.clear()
        win32gui.EnumWindows(get_widows_information, self.window_list)
        self.ui.comboBox.clear()
        index = 0
        for window in self.window_list:
            title = show_title = window.title
            if len(title) > 35:
                show_title = title[:35] + ' ... '
            rect = window.client_rect
            tooltip = 'Window Title:\n   ' + title + '\nWindow Rect:\n   ' \
                      + 'x = %d, y = %d, width = %d, height = %d' \
                      % (rect[0], rect[1], rect[2], rect[3])
            self.ui.comboBox.addItem(show_title)
            self.ui.comboBox.setItemData(index, tooltip, QtCore.Qt.ToolTipRole)
            index += 1
        self.ui.comboBox.setCurrentIndex(-1)

    def on_window_selected(self):
        index = self.ui.comboBox.currentIndex()
        if index == -1:
            self.client_rect = None
            self.ui.label_relative_pos_value.clear()
        else:
            window = self.window_list[index]
            self.client_rect = window.client_rect




