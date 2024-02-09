import sys
import numpy as np
from PyQt6.QtWidgets import QVBoxLayout, QMainWindow, QApplication, QLabel, QLineEdit, QPushButton, QWidget, QSlider
from PyQt6 import uic
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class AppDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        ui = uic.loadUi("./MainWindow.ui", self)

        # 生成空图像
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # 获取控件
        self.input_box: QLineEdit = ui.input_box
        self.button: QPushButton = ui.button
        self.plot_widget: QWidget = ui.plot_widget
        self.lable_result: QLabel = ui.label_result
        self.slider: QSlider = ui.slider

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.plot_widget.setLayout(layout)

        # 设置事件
        self.button.clicked.connect(self.on_button_clicked)
        self.slider.valueChanged.connect(self.on_value_changed)

    def draw(self, theta_deg: float):
        cueball_center = (0, 0)

        theta = theta_deg / 180 * np.pi
        target_center = (np.sin(theta), np.cos(theta))
        target_center = (np.sin(theta), np.cos(theta))
        d = 1
        r = d / 2
        result = 1 - target_center[0]

        # 清除之前的图表
        self.figure.clear()

        # 绘制俯视图
        ax_top = self.figure.add_subplot(111)
        ax_top.add_patch(Circle(cueball_center, r, edgecolor="blue", facecolor="none"))
        ax_top.add_patch(Circle(target_center, r, edgecolor="red", facecolor="none"))

        # 设置坐标轴比例和范围
        ax_top.set_aspect("equal")
        ax_top.spines["top"].set_color("none")
        ax_top.spines["right"].set_color("none")
        ax_top.spines["bottom"].set_position(("data", 0))
        ax_top.spines["left"].set_position(("data", 0))
        ax_top.set_xticklabels([])
        ax_top.set_yticklabels([])
        ax_top.set_xlim(-2, 2)
        ax_top.set_ylim(-2, 2)

        # 绘制遮挡效果
        ax_front = self.figure.add_subplot(122)
        ax_front.add_patch(Circle((cueball_center[0], 0), r, edgecolor="blue", facecolor="none", zorder=2))
        ax_front.add_patch(Circle((target_center[0], 0), r, edgecolor="red", facecolor="none", zorder=1))
        ax_front.set_aspect("equal")
        ax_front.spines["top"].set_color("none")
        ax_front.spines["right"].set_color("none")
        ax_front.spines["bottom"].set_position(("data", 0))
        ax_front.spines["left"].set_position(("data", 0))
        ax_front.set_xticklabels([])
        ax_front.set_yticklabels([])
        ax_front.set_xlim(-2, 2)
        ax_front.set_ylim(-2, 2)

        # 刷新画布
        self.canvas.draw()

        # 更新文本
        self.lable_result.setText(f"当目标角为{theta_deg}度时，母球应遮住{result}颗目标球")

    def on_button_clicked(self):
        # 数据计算
        theta_deg = float(self.input_box.text())
        self.draw(theta_deg)
        self.slider.setValue(int(theta_deg))

    def on_value_changed(self, value):
        theta_deg = float(value)
        self.draw(theta_deg)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = AppDemo()
    demo.show()
    sys.exit(app.exec())
