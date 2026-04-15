import numpy as np
from perlin_noise import PerlinNoise
import matplotlib.pyplot as plt
import logging
from subfunctions.preprocessing import format_low_res_input, reverse_high_res_output

logger = logging.getLogger(__name__)

def visual_results(model):
    resolution = (1000, 1000)
    #Initialize perlin noise for running with model
    noise = PerlinNoise(octaves=20, seed=1)
    values = np.array([[noise([i/resolution[0], j/resolution[1]]) for j in range(resolution[0])] for i in range(resolution[1])])*1000
    logger.info('Generating low res input for visualization - Max: {}, Min: {}'.format(np.max(values), np.min(values)))
    low_res_input = format_low_res_input(values)
    results = model.predict(low_res_input)
    high_res_output = reverse_high_res_output(results, resolution)
    logger.info('Generated high res output for visualization - Max: {}, Min: {}'.format(np.max(high_res_output), np.min(high_res_output)))
    display_as_plot(high_res_output, values)

def display_as_plot(high_res, low_res, save_path=None, save_only=False):
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].set_title('High Resolution')
    axs[0].contourf(high_res, cmap='terrain')
    axs[1].set_title('Low Resolution')
    axs[1].contourf(low_res, cmap='terrain')
    if save_path:
        plt.savefig(save_path)
    if not save_only:
        plt.show()