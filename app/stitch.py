import cv2
import numpy as np
import imutils
from skimage import io 

def kmeans_image(img):
    pixels = np.float32(img.reshape(-1, 3))

    n_colors = 3
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)

    return np.uint8(palette[-1])


def stitch_image(filestr, horizontal_samples_user_input, stitch_style, stitch_size, stitch_spacing):
    npimg = np.fromstring(filestr, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
    print(img.shape)
    # if not img:
    #     return "Hmm. Something went wrong."
    
    img = imutils.resize(img, width=1000)
    img = imutils.resize(img, height=1000) # imutils will not respect both width and height at same time
    input_width, input_height, *_ = img.shape

    if len(img.shape) > 2 and img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    sample_size = round(input_width / horizontal_samples_user_input)
    vertical_samples = round(input_height / sample_size)

    output_html = ''

    output_html += '\t\t<div id="wrapper"><div id="image">\n'
    
    for i in range(0, horizontal_samples_user_input):
        output_html += '\t\t\t<div class="row">\n'
        
        for j in range(0, vertical_samples):
            i_start = i*sample_size
            i_end = i*sample_size+sample_size
            j_start = j*sample_size
            j_end = j*sample_size+sample_size

            r,g,b = kmeans_image(img[i_start:i_end, j_start:j_end])
            output_html += f'\t\t\t\t<div style="background-color: rgb({r},{g},{b});" class="cell"></div>\n'
        
        output_html += '\t\t\t</div>\n'
    
    output_html += '\t\t</div></div>\n'
    return output_html
