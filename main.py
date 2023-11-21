import tkinter as tk
from tkinter import Canvas
import random
import math
import matplotlib.pyplot as plt

class Maximin:
    def __init__(self, num_objects):
        self.num_pnt = num_objects
        self.points = [(random.uniform(0, 10), random.uniform(0, 10)) for _ in range(num_objects)]
        self.clusters = [Cluster(self.points[0])]
        self.num_cls = 1

        max_distance = 0
        max_distance_index = 0
        for i in range(1, num_objects):
            distance = self.distance(self.clusters[0].centroid, self.points[i])
            if distance > max_distance:
                max_distance = distance
                max_distance_index = i
        self.clusters.append(Cluster(self.points[max_distance_index]))
        self.num_cls += 1
        self.bind()

    def bind(self):
        for cluster in self.clusters:
            cluster.points = []

        first_point = self.clusters[0].centroid
        for i in range(self.num_pnt):
            min_distance = self.distance(first_point, self.points[i])
            min_distance_index = 0
            for j in range(1, self.num_cls):
                distance = self.distance(self.clusters[j].centroid, self.points[i])
                if min_distance > distance:
                    min_distance = distance
                    min_distance_index = j
            self.clusters[min_distance_index].points.append(self.points[i])
        self.draw()

    def do_task(self):
        flag = True
        count = 0

        while flag:
            self.bind()
            max_distance = 0
            new_centroid = (0, 0)
            for i in range(self.num_cls):
                centroid = self.clusters[i].centroid
                for point in self.clusters[i].points:
                    distance = self.distance(centroid, point)
                    if distance > max_distance:
                        max_distance = distance
                        new_centroid = point
            mid_distance = 0
            for i in range(self.num_cls):
                centroid = self.clusters[i].centroid
                mid_distance += self.distance(centroid, new_centroid)
            mid_distance /= self.num_cls * 2

            if max_distance > mid_distance:
                new_cluster = Cluster(new_centroid)
                self.clusters.append(new_cluster)
                self.num_cls += 1
            else:
                flag = False
            count += 1
            print("Iteration:", count)

    def draw(self):
        root = tk.Tk()
        root.title("Maximin")
        canvas = Canvas(root, width=400, height=400, bg='black')
        canvas.pack()

        colors = ['#ff0000', '#bf00ff', '#0000ff', '#40ff00', '#00ffbf', '#00ffff', '#00bfff', '#0080ff', '#ffff00',
                  '#8000ff',
                  '#ffbf00', '#ff00bf', '#808080', '#ff99ff', '#660033', '#999966', '#cc3300', '#ccffcc', '#ff99cc',
                  '#99ccff']

        for i in range(self.num_cls):
            x = [point[0] for point in self.clusters[i].points]
            y = [point[1] for point in self.clusters[i].points]
            for j in range(len(x)):
                canvas.create_oval(x[j] * 20, y[j] * 20, x[j] * 20 + 5, y[j] * 20 + 5, fill=colors[i], outline='white')
            canvas.create_oval(self.clusters[i].centroid[0] * 20, self.clusters[i].centroid[1] * 20,
                               self.clusters[i].centroid[0] * 20 + 10, self.clusters[i].centroid[1] * 20 + 10,
                               fill='white', outline='black')

        root.mainloop()

    @staticmethod
    def distance(point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

class Cluster:
    def __init__(self, centroid):
        self.points = []
        self.centroid = centroid

if __name__ == '__main__':
    maximin = Maximin(50)
    maximin.do_task()
