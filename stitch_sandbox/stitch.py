import cv2
import numpy as np
import imutils
import matplotlib.pyplot as plt
from skimage import io 

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
    # kmeans_preview(img)
    return np.uint8(palette[-1])



def stitch_image(image, image_sample_side_length, thread_side_length):
    img = io.imread(image)
    input_width, input_height, _ = img.shape

    horizontal_samples = round(input_width / image_sample_side_length)
    vertical_samples = round(input_height / image_sample_side_length)

    output_html = f'''
    <html>
        <head>
        </head>
        <body>
            <style>
                body {{
                    background-color: #ccc;
                }}
                .row {{
                    display: flex;
                }}
                .cell {{
                    margin: 1px;
                    border-radius: 30%;
                    width:{thread_side_length}px;
                    display: inline-block;
                    height:{thread_side_length}px; 
                }}
            </style>
    '''

    output_html += '\t\t<div class="wrapper">\n'
    
    for i in range(0, horizontal_samples):
        output_html += '\t\t\t<div class="row">\n'
        
        for j in range(0, vertical_samples):
            i_start = i*image_sample_side_length
            i_end = i*image_sample_side_length+image_sample_side_length
            j_start = j*image_sample_side_length
            j_end = j*image_sample_side_length+image_sample_side_length

            r,g,b = kmeans_image(img[i_start:i_end, j_start:j_end])
            output_html += f'\t\t\t\t<div style="background-color: rgb({r},{g},{b});" class="cell"></div>\n'
        
        output_html += '\t\t\t</div>\n'
    
    output_html += '\t\t</div>\n'
    output_html += '\t</body>\n</html>'

    with open('output.html', 'w') as file:
        file.write(output_html)

main(image='woof.jpg', image_sample_side_length=2, thread_side_length=10)