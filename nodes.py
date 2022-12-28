import pygame
import numpy as np
from vector import Vector2
from constants import *


class Node(object):
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.neighbors = {UP: None, DOWN: None, LEFT: None, RIGHT: None, PORTAL: None}

    def render(self, screen):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                line_start = self.position.asTuple()
                line_end = self.neighbors[n].position.asTuple()
                pygame.draw.line(screen, WHITE, line_start, line_end, 4)
                pygame.draw.circle(screen, RED, self.position.asTuple(), 12)


class NodeGroup(object):
    def __init__(self, level):
        self.Level = level
        self.nodesULT = {}
        self.nodeSymbols = ['+', 'P', 'n']
        self.pathSymbols = ['.', '-', '|', 'p']
        data = self.readMazeFile(level)
        self.createNodeTable(data)
        self.connectHorizontally(data)
        self.connectVertically(data)

    def readMazeFile(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')

    def createNodeTable(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    x, y = self.constructKey(col+xoffset, row+yoffset)
                    self.nodesULT[(x, y)] = Node(x, y)

    def constructKey(self, x, y):
        return x * TILEWIDTH, y * TILEHEIGHT

    def connectHorizontally(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col+xoffset, row+yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, row+yoffset)
                        self.nodesULT[key].neighbors[RIGHT] = self.nodesULT[otherkey]
                        self.nodesULT[otherkey].neighbors[LEFT] = self.nodesULT[key]
                        key = otherkey
                elif data[row][col] not in self.pathSymbols:
                    key = None

    def connectVertically(self, data, xoffset=0, yoffset=0):
        dataT = data.transpose()
        for col in list(range(dataT.shape[0])):
            key = None
            for row in list(range(dataT.shape[1])):
                if dataT[col][row] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col+xoffset, row+yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, row+yoffset)
                        self.nodesULT[key].neighbors[DOWN] = self.nodesULT[otherkey]
                        self.nodesULT[otherkey].neighbors[UP] = self.nodesULT[key]
                        key = otherkey
                elif dataT[col][row] not in self.pathSymbols:
                    key = None

    def getNodeFromPixels(self, xpixel, ypixel):
        if (xpixel, ypixel) in self.nodesULT.keys():
            return None

    def getNodeFromTiles(self, col, row):
        x, y = self.constructKey(col, row)
        if (x, y) in self.nodesULT.keys():
            return self.nodesULT[(x, y)]
        return None

    def getStartTempNode(self):
        nodes = list(self.nodesULT.values())
        return nodes[0]

    # portal part
    def setPortalPair(self, pair1, pair2):
        key1 = self.constructKey(*pair1)
        key2 = self.constructKey(*pair2)
        if key1 in self.nodesULT.keys() and key2 in self.nodesULT.keys():
            self.nodesULT[key1].neighbors[PORTAL] = self.nodesULT[key2]
            self.nodesULT[key2].neighbors[PORTAL] = self.nodesULT[key1]


    def render(self, screen):
        for node in self.nodesULT.values():
            node.render(screen)
