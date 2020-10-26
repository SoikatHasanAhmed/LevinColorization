import colorsys
import numpy as np
import matplotlib.pyplot as plt
from scipy import misc
def image_preprocess(input_image, hinted_image):

        input_image = input_image.astype(float) / 255
        hinted_image = hinted_image.astype(float) / 255

        color_pixels = abs(input_image - hinted_image).sum(2) > 0.01

        (Y, _, _) = colorsys.rgb_to_yiq(input_image[:, :, 0], input_image[:, :, 1], input_image[:, :, 2])
        (_, I, Q) = colorsys.rgb_to_yiq(hinted_image[:, :, 0], hinted_image[:, :, 1], hinted_image[:, :, 2])


        YIQ_image = np.zeros(input_image.shape)
        YIQ_image[:, :, 0] = Y
        YIQ_image[:, :, 1] = I
        YIQ_image[:, :, 2] = Q
        return color_pixels, YIQ_image
def show_save(input,hint,img,name):
        misc.imsave('./output/{}.bmp'.format(name), img, format='bmp')
        a =plt.subplot(1, 3, 1)
        a.imshow(input)
        plt.axis('off')
        plt.subplot(1, 3, 2)
        plt.imshow(hint)
        plt.axis('off')
        plt.subplot(1, 3, 3)
        plt.imshow(img)
        plt.axis('off')
        plt.show()