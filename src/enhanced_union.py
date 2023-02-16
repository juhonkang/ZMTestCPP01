import numpy as np


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1

def connected_components(image):
    labels = np.zeros_like(image)
    uf = UnionFind(np.count_nonzero(image))
    label = 1
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i, j] == 1:
                if i > 0 and image[i-1, j] == 1:
                    uf.union(i*image.shape[1]+j, (i-1)*image.shape[1]+j)
                if j > 0 and image[i, j-1] == 1:
                    uf.union(i*image.shape[1]+j, i*image.shape[1]+j-1)
                labels[i, j] = uf.find(i*image.shape[1]+j)+1
                if labels[i, j] == label:
                    label += 1
    return labels
