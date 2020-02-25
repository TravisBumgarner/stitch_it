import cv2
import numpy as np
import imutils
import matplotlib.pyplot as plt
from skimage import io 

OUTPUT_WIDTH = 500
OUTPUT_HEIGHT = 500
SLICE = 100 # px

def kmeans_preview(img):
    pixels = np.float32(img.reshape(-1, 3))

    n_colors = 3
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)

    dominant = palette[np.argmax(counts)]
    print(dominant)

    average = img.mean(axis=0).mean(axis=0)

    avg_patch = np.ones(shape=img.shape, dtype=np.uint8)*np.uint8(average)

    indices = np.argsort(counts)[::-1]   
    freqs = np.cumsum(np.hstack([[0], counts[indices]/counts.sum()]))
    rows = np.int_(img.shape[0]*freqs)

    dom_patch = np.zeros(shape=img.shape, dtype=np.uint8)
    for i in range(len(rows) - 1):
        dom_patch[rows[i]:rows[i + 1], :, :] += np.uint8(palette[indices[i]])

    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(12,6))
    ax0.imshow(avg_patch)
    ax0.set_title('Average color')
    ax0.axis('off')
    ax1.imshow(dom_patch)
    ax1.set_title('Dominant colors')
    ax1.axis('off')
    plt.show(fig)


def kmeans_image(img):
    pixels = np.float32(img.reshape(-1, 3))

    n_colors = 3
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)

    dominant = palette[np.argmax(counts)]
    # print(palette)
    # kmeans_preview(img)
    return np.uint8(palette[-1])

def main():
    output = []
    img = io.imread('sample.jpg') #[:, :, :-1]
    input_width, input_height, _ = img.shape

    output_width = round(input_width / SLICE)
    output_height = round(input_height / SLICE)

    output = np.zeros((output_width, output_height,3))

    for i in range(0, output_width):
        for j in range(0, output_height):
            subsection = img[i*SLICE:i*SLICE+SLICE, j*SLICE:j*SLICE+SLICE]
            output[i][j] = kmeans_image(subsection)
    io.imsave("output.jpg", output)
main()