import numpy as np

def connected_components(image):
    labels = np.zeros_like(image)
    label = 1
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i, j] == 1 and labels[i, j] == 0:
                dfs(image, labels, i, j, label)
                label += 1
    return labels

def dfs(image, labels, i, j, label):
    labels[i, j] = label
    if i > 0 and image[i-1, j] == 1 and labels[i-1, j] == 0:
        dfs(image, labels, i-1, j, label)
    if j > 0 and image[i, j-1] == 1 and labels[i, j-1] == 0:
        dfs(image, labels, i, j-1, label)
    if i < image.shape[0]-1 and image[i+1, j] == 1 and labels[i+1, j] == 0:
        dfs(image, labels, i+1, j, label)
    if j < image.shape[1]-1 and image[i, j+1] == 1 and labels[i, j+1] == 0:
        dfs(image, labels, i, j+1, label)
