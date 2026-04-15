import numpy as np
import logging

logger = logging.getLogger(__name__)


def preprocess_data(data):
    # Perform any necessary preprocessing on the data (e.g., normalization, augmentation)
    # resultant data has the point and its 8 surrounding low res pixels as input and the corresponding 9 high res pixels as output
    high_res_shape = data[2].shape
    low_res_shape = data[3].shape
    logger.info('Region {}: High Res Shape: {}, Low Res Shape: {}'.format(data[0], high_res_shape, low_res_shape))
    low_res_input = format_low_res_input(data[3])
    high_res_output = format_high_res_output(data[2], low_res_shape)
    return (data[0], data[1], low_res_input, high_res_output)

def format_low_res_input(low_res):
    low_res_input = np.zeros(((low_res.shape[0]-2)*(low_res.shape[1]-2), 9))
    low_res_input[:, 0] = low_res[:-2, :-2].flatten() # top left
    low_res_input[:, 1] = low_res[:-2, 1:-1].flatten() # top middle
    low_res_input[:, 2] = low_res[:-2, 2:].flatten() # top right
    low_res_input[:, 3] = low_res[1:-1, :-2].flatten() # middle left
    low_res_input[:, 4] = low_res[1:-1, 1:-1].flatten() # middle middle
    low_res_input[:, 5] = low_res[1:-1, 2:].flatten() # middle right
    low_res_input[:, 6] = low_res[2:, :-2].flatten() # bottom left
    low_res_input[:, 7] = low_res[2:, 1:-1].flatten() # bottom middle
    low_res_input[:, 8] = low_res[2:, 2:].flatten() # bottom right
    return low_res_input

def format_high_res_output(high_res, low_res_shape):
    high_res_output = np.zeros(((low_res_shape[0]-2)*(low_res_shape[1]-2), 9))
    high_res_output[:, 0] = high_res[3:-3:3, 3:-3:3].flatten() # top left
    high_res_output[:, 1] = high_res[3:-3:3, 4:-3:3].flatten() # top middle
    high_res_output[:, 2] = high_res[3:-3:3, 5:-3:3].flatten() # top right
    high_res_output[:, 3] = high_res[4:-3:3, 3:-3:3].flatten() # middle left
    high_res_output[:, 4] = high_res[4:-3:3, 4:-3:3].flatten() # middle middle
    high_res_output[:, 5] = high_res[4:-3:3, 5:-3:3].flatten() # middle right
    high_res_output[:, 6] = high_res[5:-3:3, 3:-3:3].flatten() # bottom left
    high_res_output[:, 7] = high_res[5:-3:3, 4:-3:3].flatten() # bottom middle
    high_res_output[:, 8] = high_res[5:-3:3, 5:-3:3].flatten() # bottom right
    return high_res_output

def reverse_high_res_output(results, shape):
    high_res_output = np.zeros((shape[0]*3 - 6, shape[1]*3 - 6))
    high_res_output[::3, ::3] = results[:, 0].reshape((shape[0]-2, shape[1]-2)) # top left
    high_res_output[::3, 1::3] = results[:, 1].reshape((shape[0]-2, shape[1]-2)) # top middle
    high_res_output[::3, 2::3] = results[:, 2].reshape((shape[0]-2, shape[1]-2)) # top right
    high_res_output[1::3, ::3] = results[:, 3].reshape((shape[0]-2, shape[1]-2)) # middle left
    high_res_output[1::3, 1::3] = results[:, 4].reshape((shape[0]-2, shape[1]-2)) # middle middle
    high_res_output[1::3, 2::3] = results[:, 5].reshape((shape[0]-2, shape[1]-2)) # middle right
    high_res_output[2::3, ::3] = results[:, 6].reshape((shape[0]-2, shape[1]-2)) # bottom left
    high_res_output[2::3, 1::3] = results[:, 7].reshape((shape[0]-2, shape[1]-2)) # bottom middle
    high_res_output[2::3, 2::3] = results[:, 8].reshape((shape[0]-2, shape[1]-2)) # bottom right
    return high_res_output