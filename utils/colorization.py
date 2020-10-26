from .methods import *
from .converts import  *
from scipy.sparse import linalg
from scipy import sparse

def colorize(input_image, hinted_image):


    color_pixels, YIQ_image = image_preprocess(input_image, hinted_image)  # returns color mask , YIQ image
    n = YIQ_image.shape[0]  # n = image height
    m = YIQ_image.shape[1]  # m = image width
    imgSize = n * m

    # making dummy image with image size
    temp = np.arange(imgSize).reshape(n, m, order='F').copy()


    center = 1
   
    row_index = np.zeros(imgSize * (2 * center + 1) ** 2, dtype=np.int64)
    colom_index = np.zeros(imgSize * (2 * center + 1) ** 2, dtype=np.int64)
    vals = np.zeros(imgSize * (2 * center + 1) ** 2)

    length = 0
    consts_len = 0
    for j in range(m):
        for i in range(n):
            if not color_pixels[i, j]:
                tlen = 0
                gvals = np.zeros((2 * center + 1) ** 2)
                for ii in range(max(0, i - center), min(i + center + 1, n)):
                    for jj in range(max(0, j - center), min(j + center + 1, m)):
                        if ii != i or jj != j:
                            row_index[length] = consts_len
                            colom_index[length] = temp[ii, jj]
                            gvals[tlen] = YIQ_image[ii, jj, 0]
                            length += 1
                            tlen += 1
                t_vals = YIQ_image[i, j, 0].copy()
                gvals[tlen] = t_vals
                c_var = np.mean(
                    (gvals[0:tlen + 1] - np.mean(gvals[0:tlen + 1])) ** 2)
                csig = c_var * 0.6
                mgv = min((gvals[0:tlen + 1] - t_vals) ** 2)
                if csig < (-mgv / np.log(0.01)):
                    csig = -mgv / np.log(0.01)
                if csig < 0.000002:
                    csig = 0.000002
                gvals[0:tlen] = np.exp(-((gvals[0:tlen] - t_vals) ** 2) / csig)
                gvals[0:tlen] = gvals[0:tlen] / np.sum(
                    gvals[0:tlen])
                vals[length - tlen:length] = -gvals[0:tlen]
            row_index[length] = consts_len
            colom_index[length] = temp[i, j]
            vals[length] = 1
            length += 1
            consts_len += 1

    vals = vals[0:length]
    colom_index = colom_index[0:length]
    row_index = row_index[0:length]

    # Optimization
    A = sparse.csr_matrix((vals, (row_index, colom_index)), (consts_len, imgSize))
    b = np.zeros((A.shape[0]))
    nI = np.zeros(YIQ_image.shape)
    nI[:, :, 0] = YIQ_image[:, :, 0]
    colorCopy = color_pixels.reshape(imgSize, order='F').copy()
    lblInds = np.nonzero(colorCopy)
    for t in [1, 2]:
        curIm = YIQ_image[:, :, t].reshape(imgSize, order='F').copy()
        b[lblInds] = curIm[lblInds]
        new_vals = linalg.spsolve(A, b)
        nI[:, :, t] = new_vals.reshape(n, m, order='F')
    (R, G, B) = outputConvertRGB(nI[:, :, 0], nI[:, :, 1], nI[:, :, 2])
    RGB = np.zeros(nI.shape)
    RGB[:, :, 0] = R
    RGB[:, :, 1] = G
    RGB[:, :, 2] = B
    return RGB

