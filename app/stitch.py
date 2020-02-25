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


def stitch_image(image, sample_size, stitch_style, stitch_size, stitch_spacing):
    img = io.imread(image)
    input_width, input_height, _ = img.shape

    horizontal_samples = round(input_width / sample_size)
    vertical_samples = round(input_height / sample_size)

    output_html = f'''
    <html>
        <head>
        </head>
        <body>
            <style>
                :root {{
                    --stitch_spacing: {stitch_spacing}px;
                    --stitch_style: {stitch_style}%;
                    --stitch_size: {stitch_size}px;
                }}
                body {{
                    background-color: var(--bg);
                }}
                .row {{
                    line-height: 0;
                    white-space: nowrap;
                    clear: both;
                }}
                .cell {{
                    margin: var(--stitch_spacing);
                    border-radius: var(--stitch_style);
                    width: var(--stitch_size);
                    float: left;
                    height: var(--stitch_size); 
                }}
            </style>
    '''

    output_html += '\t\t<div id="wrapper">\n'
    
    for i in range(0, horizontal_samples):
        output_html += '\t\t\t<div class="row">\n'
        
        for j in range(0, vertical_samples):
            i_start = i*sample_size
            i_end = i*sample_size+sample_size
            j_start = j*sample_size
            j_end = j*sample_size+sample_size

            r,g,b = kmeans_image(img[i_start:i_end, j_start:j_end])
            output_html += f'\t\t\t\t<div style="background-color: rgb({r},{g},{b});" class="cell"></div>\n'
        
        output_html += '\t\t\t</div>\n'
    
    output_html += '\t\t</div>\n'
    output_html += '\t</body>\n</html>'

    return output_html
