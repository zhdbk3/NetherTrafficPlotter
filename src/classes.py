#
# Created by MC着火的冰块 on 2024/8/9
#

import pickle


class ElementBase:
    """图上元素的基类"""
    color: str  # 颜色
    legend: str  # 图例


class NodeBase(ElementBase):
    def __init__(self, x: int, z: int, name: str):
        """
        节点的基类
        :param x: 地狱的 x 坐标
        :param z: 地狱的 z 坐标
        :param name: 节点名字
        """
        self.x = x
        self.z = z
        self.name = name


class NetherPortal(NodeBase):
    color = 'darkviolet'
    legend = '地狱门'


class BifurcationPoint(NodeBase):
    color = 'lightgrey'
    legend = '分叉点'


class WayBase(ElementBase):
    def __init__(self, node1: NodeBase, node2: NodeBase):
        """线路的基类"""
        self.node1 = node1
        self.node2 = node2


class Railway(WayBase):
    color = 'red'
    legend = '铁路'


class IceWay(WayBase):
    color = 'blue'
    legend = '冰道'


class NetherTraffic:
    def __init__(self):
        self.nodes: list[NodeBase] = []
        self.ways: list[WayBase] = []

    def add_node(self, node: NodeBase) -> None:
        """添加节点"""
        self.nodes.append(node)

    def add_way(self, way: WayBase) -> None:
        """添加线路"""
        self.ways.append(way)

    def node_named(self, name: str) -> NodeBase:
        """
        获取指定名字的节点对象，若没有则报错
        :param name: 节点名字
        :return: 节点对象
        """
        for node in self.nodes:
            if node.name == name:
                return node

    def remove_node(self, name: str) -> None:
        """
        删除节点，以及节点连着的线路
        :param name: 节点名字
        :return: None
        """
        node = self.node_named(name)
        self.nodes.remove(node)
        self.ways = [way for way in self.ways if node not in (way.node1, way.node2)]

    def remove_way(self, node_name_1: str, node_name_2: str) -> None:
        """删除线路"""
        node1 = self.node_named(node_name_1)
        node2 = self.node_named(node_name_2)
        for way in self.ways:
            if {node1, node2} == {way.node1, way.node2}:
                self.ways.remove(way)
                return

    def save(self, path: str) -> None:
        """将数据存储到本地"""
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(path: str) -> "NetherTraffic":
        """
        从本地读取数据
        :param path: pickle 文件路径
        :return: 一个 NetherTraffic 对象
        """
        with open(path, 'rb') as f:
            return pickle.load(f)


type_named: dict[str, type] = {
    '地狱门': NetherPortal, '分叉点': BifurcationPoint,
    '铁路': Railway, '冰道': IceWay
}

__all__ = [
    'NetherPortal', 'BifurcationPoint',
    'Railway', 'IceWay',
    'NetherTraffic',
    'type_named'
]
