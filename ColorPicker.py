# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QGuiApplication, QColor, QCursor, QPainter, QPen
from PyQt5.QtWidgets import QWidget, QApplication
import ui_color_picker
import BindWindow
import win32api


class ColorPicker(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = ui_color_picker.Ui_ColorPicker()
        self.ui.setupUi(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.capture_mouse)
        self.timer.start(100)
        self.ui.pushButton.clicked.connect(self.on_push_button_clicked)
        self.child_window = BindWindow.BindWindow(self)
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

    def on_push_button_clicked(self):
        x = self.x() + self.width()
        y = self.y()
        self.child_window.move(x, y)
        self.child_window.show()

    def on_window_selected(self, window_info):
        if window_info is None:
            self.ui.pushButton.setText('Select Window')
            self.client_rect = None
            self.ui.label_relative_pos_value.clear()
        else:
            self.client_rect = window_info.client_rect
            title = show_title = window_info.title
            if len(title) >= 30:
                show_title = title[:12] + ' ... ' + title[-12:]
            self.ui.pushButton.setText(show_title)

    def closeEvent(self, close_event):
        self.child_window.close()

