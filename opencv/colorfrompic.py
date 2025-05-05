import cv2
import numpy as np
from sklearn.cluster import KMeans

def color_detection(image_path, num_colors):
    image = cv2.imread(image_path)

    pixels = image.reshape(-1, 3)

    kmeans = KMeans(n_clusters=num_colors)
    
    colors = kmeans.cluster_centers_

    return colors.astype(int)

image_path = 'path_to_your_image'
num_colors = 5

dominant_colors = color_detection(image_path, num_colors)
print("Dominant Colors:")
for color in dominant_colors:
    print(color)