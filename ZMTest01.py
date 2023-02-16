import os
import matplotlib.pyplot as plt
import numpy as np
import argparse, time
# import deque
from collections import deque
from PIL import Image

def parse_args():
    parser = argparse.ArgumentParser(description='Zeta Motion Test 1 script')

    parser.add_argument('--width', default=800, type=int, help='width of the images')
    # height of the images
    parser.add_argument('--height', default=600, type=int, help='height of the images')
    # data .bin path 
    parser.add_argument('--data', default='data.bin', type=str, help='data.bin path')
    
    # save path
    parser.add_argument('--output', default='output', type=str, help='save path')
    parser.add_argument('--reduce_factor', default=2, type=int, help='Reduce image size\
         by factor before detection, reduce time but also reduce 1-2 pixel accuracy of bounding box')

    return parser.parse_args()


def blob_bbox(img, reduce=2):
    m, n = len(img), len(img[0])
    # resize image
    m, n = m//reduce, n//reduce
    img = np.array(Image.fromarray(img, mode='L').resize((n, m)))
    img[img>0] = 1
    DIR = [-1, 0, 1]


    bbox = dict()
    def bfs(r, c, tag):
        """
        BFS to find the bounding box of a blob and mark every pixel in the blob to 0
        """
        if r < 0 or r == m or c < 0 or c == n or img[r][c] == 0: return 0
        q = deque([(r, c)])
        while q:
            r, c = q.popleft()
            for i in DIR:
                for j in DIR:
                    if i == 0 and j == 0: continue
                    nr, nc = r + i, c + j
                    if nr < 0 or nr == m or nc < 0 or nc == n or img[nr][nc] == 0: continue
                    img[nr][nc] = 0  # Mark as visited
                    if bbox.get(tag) is None:
                        bbox[tag] = [[r], [r], [c], [c]]
                    else:
                        bbox[tag][0].append(r)
                        bbox[tag][1].append(r)
                        bbox[tag][2].append(c)
                        bbox[tag][3].append(c)
                    q.append([nr, nc])
        return 1

    tag = 1
    # find a connected component pixel 
    while np.argmax(img) != 0 or img[0][0] != 0:
        r, c = np.unravel_index(np.argmax(img), img.shape)
        if bfs(r, c, str(tag)): # run bfs on the connected component to detect the bounding box
            bbox[str(tag)][0] = np.min(bbox[str(tag)][0])
            bbox[str(tag)][1] = np.max(bbox[str(tag)][1])
            bbox[str(tag)][2] = np.min(bbox[str(tag)][2])
            bbox[str(tag)][3] = np.max(bbox[str(tag)][3])
            tag += 1



    return bbox



def blob_detection(img, save_fp, reduce=2):
    original_img = img.copy()
    original_img_ = original_img>0
    m, n = original_img.shape
    bbox = blob_bbox(img, reduce)

    # post check the bbox to increase the accuracy
    for tag, (minr, maxr, minc, maxc) in bbox.items():
        minr, maxr, minc, maxc = minr*reduce, maxr*reduce, minc*reduce, maxc*reduce
        minr_, maxr_, minc_, maxc_ = minr, maxr, minc, maxc

        # Expand bounding box by trials 
        for j in range((reduce*2)):
            try:
                if 0 <= minr_ < m and original_img_[minr_, minc:maxc+1].any():
                    minr = minr_
                    minr_ -= 1
            except: 
                pass
            try:
                if 0 <= maxr_ < m and original_img_[maxr_, minc:maxc+1].any():
                    maxr = maxr_
                    maxr_ += 1
            except: 
                pass
            try:
                if 0 <= minc_ < n and original_img_[minr:maxr+1, minc_].any():
                    minc = minc_
                    minc_ -= 1
            except:
                pass
            try:
                if 0 <= maxc_ < n and original_img_[minr:maxr+1, maxc_].any():
                    maxc = maxc_
                    maxc_ += 1
            except:
                pass
            try:
                if 0 <= maxc+1 < n and 0 <= maxr+1< m\
                      and original_img_[maxr+1, maxc+1]:
                    maxc+=1
                    maxr+=1

                    maxc_= maxc
                    maxr_= maxr

            except:
                pass
            
        original_img[minr, minc:maxc] = 255
        original_img[maxr, minc:maxc] = 255
        original_img[minr:maxr, minc] = 255
        original_img[minr:maxr, maxc] = 255
        original_img[maxr, maxc] = 255

        # save image
        plt.imsave(save_fp, original_img, cmap='gray')


if __name__ == "__main__":
    args = parse_args()


    try:
        # read data.bin with unsinged char data
        imgs = np.fromfile(args.data, dtype=np.uint8)
        imgs = imgs.reshape(-1, args.height, args.width)
    except:
        print("Error: wrong input configuration")
        exit()

    try:
        os.makedirs(args.output, exist_ok=True)
        n = imgs.shape[0]
        base_fp_data = os.path.basename(args.data).split('.')[0]
        start = time.time()
        print(f"Start processing {n} images")
        for i in range(n):
            save_fp = os.path.join(args.output, "{base}_{i}.jpg".\
                format(base=base_fp_data, i=i))
            blob_detection(imgs[i], save_fp, args.reduce_factor)

        print(f"Finish processing {n} images, time cost: {time.time() - start}")
    except:
        print("Error: Processing failed")
        exit()
            
            