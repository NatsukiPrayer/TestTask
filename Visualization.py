import networkx as nx
import random
import matplotlib.pyplot as plt


class Visual:
    def __init__(self, links):
        self.__links = {}
        for i in range(int(len(links)/10)+1):
            self.__links[list(links.keys())[i]] = list(links.values())[i]

    def __mouse_move(event):
        x, y = event.xdata, event.ydata
        print(x, y)

    def draw(self):
        sitemap = nx.Graph()
        tempedgelist = []
        for url in list(self.__links.items()):
            if url[1]:
                for i in range(len(url[1])):
                    tempedgelist.append([url[0], url[1][i]])
                    if url[1][i] not in self.__links.keys():
                        self.__links[url[1][i]] = []

        x = [i for i in range(0, (int((len(self.__links)) ** (1 / 2)) + 1) * 20, 20)]
        y = [i for i in range(0, (int((len(self.__links)) ** (1 / 2)) + 1) * 20, 20)]
        xy = []
        for xx in x:
            for yy in y:
                xy.append([xx, yy])
        pos = {}
        sitemap.add_edges_from(tempedgelist)
        for url in range(len(list(self.__links.keys()))):
            pos[list(self.__links.keys())[url]] = xy[url]
        plt.figure(dpi=300, figsize=(16, 9))


        plt.connect('motion_notify_event', self.__mouse_move)
        nx.draw(sitemap, pos)
        plt.show(markersize=2)
