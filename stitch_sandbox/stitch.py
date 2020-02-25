import cv2
import numpy as np
import imutils
import matplotlib.pyplot as plt
from skimage import io 

OUTPUT_WIDTH = 500
OUTPUT_HEIGHT = 500
OUTPUT_THREAD_SIZE = 10
SLICE = 5 # px

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


HTML_HEADER = '''
<html>
    <head>
    </head>
    <body>
        <style>
            .wrapper {
                
            }
            .row {
                display: flex;
            }
            .cell {
                margin: 1px;
                border-radius: 30%;
                width:5px;
                display: inline-block;
                height:5px; 
            }
        </style>
'''

def main():
    output = []
    img = io.imread('pika.png') #[:, :, :-1]
    input_width, input_height, _ = img.shape

    output_width = round(input_width / SLICE)
    output_height = round(input_height / SLICE)

    output = np.zeros((output_width * OUTPUT_THREAD_SIZE, output_height * OUTPUT_THREAD_SIZE,3))
    output_html = HTML_HEADER
    output_html += '\t\t<div class="wrapper">\n'
    for i in range(0, output_width):
        output_html += '\t\t\t<div class="row">\n'
        for j in range(0, output_height):
            subsection = img[i*SLICE:i*SLICE+SLICE, j*SLICE:j*SLICE+SLICE]
            suggested_color = kmeans_image(subsection)
            html_color = f'{suggested_color[0]}, {suggested_color[1]}, {suggested_color[2]}'
            output_html += f'\t\t\t\t<div style="background-color: rgb({html_color});" class="cell"></div>\n'
            output[i*OUTPUT_THREAD_SIZE:i*OUTPUT_THREAD_SIZE+OUTPUT_THREAD_SIZE,j*OUTPUT_THREAD_SIZE:j*OUTPUT_THREAD_SIZE+OUTPUT_THREAD_SIZE] = suggested_color
        output_html += '\t\t\t</div>\n'
    output_html += '\t\t</div>\n'
    output_html += '\t</body>\n</html>'
    io.imsave("output8.png", np.uint8(output))
    with open('output.html', 'w') as file:
        file.write(output_html)
main()