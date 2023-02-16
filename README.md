# ZMTestCPP01
ZM Little Challenge

In this connected component analysis challenge, you will be asked to write a simple script find the bounding boxes of the objects in an image, as shown in Figure 1. An object is defined as a continuous "Blob" of non-black pixels.

Read in `data.bin`, which contains an array of `unsigned char` numbers (0 - 255), which holds image frames with shape (10, 600, 800). Each image is stored in row-major format.

Implement an algorithm that identifies the bounding boxes of the objects in each image frame. 



| Figure 1.  Detected Objects       |
| ------------- |
|  ![image](https://user-images.githubusercontent.com/67153600/219402249-961d9574-a5c0-4dff-a062-bdd4c75d8077.png) |

## The success criteria for your programme are:

1. Accurate number of bounding boxes
2. Accurate positions and sizes
3. High performance (please use the macro provided to measure running time)
4. Bug free

## Please note:
Don't use any third party library to implement the algorithm (you can do better than them). However, you can use any tool to visualise the images for debugging purposes.


# Installing
``` 
pip install -r requirements.txt"
```

# Using
```
python ZMTest01.py
```

## Further exploration
In the src folder, there are other algorithms that can solve this problem. 

output folder stores debugging images
