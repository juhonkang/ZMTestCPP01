import numpy as np

def connected_components(image):
    # First pass
    labels = np.zeros_like(image)
    label = 1
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i, j] == 0:
                continue
            if i == 0 and j == 0:
                labels[i, j] = label
                label += 1
            elif i == 0:
                if image[i, j-1] == 0:
                    labels[i, j] = label
                    label += 1
                else:
                    labels[i, j] = labels[i, j-1]
            elif j == 0:
                if image[i-1, j] == 0:
                    labels[i, j] = label
                    label += 1
                else:
                    labels[i, j] = labels[i-1, j]
            else:
                if image[i, j-1] == 0 and image[i-1, j] == 0:
                    labels[i, j] = label
                    label += 1
                elif image[i, j-1] != 0 and image[i-1, j] == 0:
                    labels[i, j] = labels[i, j-1]
                elif image[i, j-1] == 0 and image[i-1, j] != 0:
                    labels[i, j] = labels[i-1, j]
                else:
                    labels[i, j] = min(labels[i-1, j], labels[i, j-1])
                    if labels[i-1, j] != labels[i, j-1]:
                        for k in range(i):
                            for l in range(j):
                                if labels[k, l] == labels[i-1, j]:
                                    labels[k, l] = labels[i, j-1]
        # Second pass
    label_dict = {}
    label = 1
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if labels[i, j] != 0:
                if labels[i, j] not in label_dict:
                    label_dict[labels[i, j]] = label
                    label += 1
                labels[i, j] = label_dict[labels[i, j]]
    return labels
