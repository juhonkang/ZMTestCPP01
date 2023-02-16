import numpy as np

class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))

    def find(self, i):
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            self.parent[root_j] = root_i

def connected_components(image):
    labels = np.zeros_like(image)
    label = 1
    uf = UnionFind(image.size)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i, j] == 0:
                continue
            neighbors = []
            if i > 0 and image[i-1, j] != 0:
                neighbors.append(labels[i-1, j])
            if j > 0 and image[i, j-1] != 0:
                neighbors.append(labels[i, j-1])
            if not neighbors:
                labels[i, j] = label
                label += 1
            else:
                min_label = min(neighbors)
                labels[i, j] = min_label
                for neighbor in neighbors:
                    uf.union(min_label-1, neighbor-1)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if labels[i, j] != 0:
                labels[i, j] = uf.find(labels[i, j]-1) + 1
    return labels
