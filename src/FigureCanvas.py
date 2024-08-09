#
# Created by MC着火的冰块 on 2024/8/9
#
# 参考：https://blog.csdn.net/ZHOU_YONG915/article/details/135826622
#

import matplotlib

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from pylab import mpl

# matplotlib 中文支持
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False


class NetherTrafficFigure(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure()
        super().__init__(self.fig)
        self.axes = self.fig.add_subplot(111)
