import numpy as np

def connected_components(image):
    labels = np.zeros_like(image)
    label = 1
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i, j] == 0:
                continue
            neighbors = []
            if i > 0 and labels[i-1, j] != 0:
                neighbors.append(labels[i-1, j])
            if j > 0 and labels[i, j-1] != 0:
                neighbors.append(labels[i, j-1])
            if not neighbors:
                labels[i, j] = label
                label += 1
            else:
                min_label = min(neighbors)
                labels[i, j] = min_label
                for neighbor in neighbors:
                    if neighbor != min_label:
                        labels[labels == neighbor] = min_label
    return labels
