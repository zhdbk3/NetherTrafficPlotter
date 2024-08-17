#
# Created by MC着火的冰块 on 2024/8/9
#

from PyQt5.QtWidgets import QMainWindow, QFileDialog
import matplotlib.lines as mlines

from ui_ntp import Ui_MainWindow
from classes import *


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.traffic = NetherTraffic()

        # 连接信号与槽
        self.connect()

        self.plot()

    def connect(self):
        """连接信号与槽"""
        self.pushButton_add_node.clicked.connect(self.add_node)
        self.pushButton_remove_node.clicked.connect(self.remove_node)
        self.pushButton_add_way.clicked.connect(self.add_way)
        self.pushButton_remove_way.clicked.connect(self.remove_way)
        self.action_save.triggered.connect(self.save_data)
        self.action_open.triggered.connect(self.load_data)
        self.pushButton_save_img.clicked.connect(self.save_img)
        self.pushButton_rename_node.clicked.connect(self.rename_node)

    def plot(self) -> None:
        """根据已有信息绘制图像"""
        # 清除原有的图像
        axes = self.figure.axes
        axes.clear()

        # 坐标轴标签
        axes.set_xlabel('x')
        axes.set_ylabel('z')
        # 反转 z(y) 轴
        axes.invert_yaxis()
        # 添加图例
        axes.legend(handles=[
            mlines.Line2D([], [], color=NetherPortal.color,
                          linestyle='None', marker='o', label=NetherPortal.legend),
            mlines.Line2D([], [], color=BifurcationPoint.color,
                          linestyle='None', marker='o', label=BifurcationPoint.legend),
            mlines.Line2D([], [], color=Railway.color, linestyle='-', label=Railway.legend),
            mlines.Line2D([], [], color=IceWay.color, linestyle='-', label=IceWay.legend)
        ])

        # 绘制节点
        for node in self.traffic.nodes:
            axes.scatter(node.x, node.z, c=node.color, marker='o')
            # 标注名字
            axes.annotate(node.name, xy=(node.x, node.z))
        # 绘制线路
        for way in self.traffic.ways:
            node1 = way.node1
            node2 = way.node2
            axes.plot([node1.x, node2.x], [node1.z, node2.z], c=way.color)

        # 刷新画布
        self.figure.fig.canvas.draw()

    def update_combo_boxes(self):
        """节点变化，更新选择框"""
        for box in (self.comboBox_node1, self.comboBox_node2, self.comboBox_selected_node):
            box.clear()
            box.addItems([node.name for node in self.traffic.nodes])

    def add_node(self) -> None:
        """添加节点"""
        node_type = type_named[self.comboBox_node_type.currentText()]
        x = int(self.lineEdit_x.text())
        z = int(self.lineEdit_z.text())
        name = self.lineEdit_name.text()
        node = node_type(x, z, name)
        self.traffic.add_node(node)
        self.plot()
        self.update_combo_boxes()

    def remove_node(self) -> None:
        """删除节点及其线路"""
        name = self.comboBox_selected_node.currentText()
        self.traffic.remove_node(name)
        self.plot()
        self.update_combo_boxes()

    def add_way(self) -> None:
        """添加线路"""
        way_type = type_named[self.comboBox_way_type.currentText()]
        node1 = self.traffic.node_named(self.comboBox_node1.currentText())
        node2 = self.traffic.node_named(self.comboBox_node2.currentText())
        way = way_type(node1, node2)
        self.traffic.add_way(way)
        self.plot()

    def remove_way(self) -> None:
        """删除线路"""
        name1 = self.comboBox_node1.currentText()
        name2 = self.comboBox_node2.currentText()
        self.traffic.remove_way(name1, name2)
        self.plot()

    def save_data(self) -> None:
        """保存数据至本地"""
        path = QFileDialog.getSaveFileName(self, '保存数据', '', 'Python 序列化文件 (*.ntp.pickle)')[0]
        if path:
            self.traffic.save(path)

    def load_data(self) -> None:
        """从本地加载数据"""
        path = QFileDialog.getOpenFileName(self, '加载数据', '', 'Python 序列化文件 (*.ntp.pickle)')[0]
        if path:
            self.traffic = NetherTraffic.load(path)
            self.plot()
            self.update_combo_boxes()

    def save_img(self) -> None:
        """保存图像"""
        path = QFileDialog.getSaveFileName(self, '保存图像', '', 'PNG 图片 (*.png)')[0]
        if path:
            self.figure.fig.savefig(path)

    def rename_node(self) -> None:
        """重命名节点"""
        old_name = self.comboBox_selected_node.currentText()
        new_name = self.lineEdit_new_name.text()
        self.traffic.rename_node(old_name, new_name)
        self.plot()
        self.update_combo_boxes()
