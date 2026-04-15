import numpy as np
from perlin_noise import PerlinNoise
import matplotlib.pyplot as plt
import logging
from subfunctions.preprocessing import format_low_res_input, reverse_high_res_output

logger = logging.getLogger(__name__)

def visual_results(model):
    resolution = (100, 100)
    #Initialize perlin noise for running with model
    noise = PerlinNoise(octaves=10, seed=1)
    values = np.array([[noise([i/resolution[0], j/resolution[1]]) for j in range(resolution[0])] for i in range(resolution[1])])*1000
    #Set any negative values to 0 as model cannot predict negative values as the training data has any below 0 values as water so it sets them to 0
    values[values < 0] = 0
    logger.info('Generating low res input for visualization - Max: {}, Min: {}'.format(np.max(values), np.min(values)))
    #Formating the low res input
    low_res_input = format_low_res_input(values)
    #upscale the low res input to higher res output using the model
    results = model.predict(low_res_input)
    #reshape the results
    middle_res_output = reverse_high_res_output(results, resolution)
    #Formating the middle res output to be used as input for the model to generate the high res output
    middle_res_input = format_low_res_input(middle_res_output)
    #Generate the high res output using the model
    results = model.predict(middle_res_input)
    logger.debug('Middle and Results shapes: {}, {}'.format(middle_res_output.shape, results.shape))
    #Reshape the results to be the same shape as the middle res output
    high_res_output = reverse_high_res_output(results, middle_res_output.shape)
    logger.info('Generated high res output for visualization - Max: {}, Min: {}'.format(np.max(results), np.min(results)))
    #Display the low res input, middle res output, and high res output as a plot
    display_as_plot([high_res_output, middle_res_output], values, save_path='example_visualisation.png')

def display_as_plot(high_res_list, low_res, save_path=None, save_only=False):
    #If high_res_list is not a list, convert it to a list
    if not isinstance(high_res_list, list):
        high_res_list = [high_res_list]
    #Get the resolution of the low res input to calculate the upscaling factor for the plot titles
    low_res_resolution = low_res.shape
    #Initialize the plot with subplots for each high res output and the low res input
    fig, axs = plt.subplots(1, len(high_res_list)+1, figsize=(5*(len(high_res_list)+1), 5))
    #Iterate through the high res outputs and display them as contour plots with a colorbar, and set the title to show the upscaling factor compared to the low res input
    for i, high_res in enumerate(high_res_list):
        upscaled_resolution = high_res.shape[0]/low_res_resolution[0]
        axs[i].set_title('Higher Resolution ({:.2f}x)'.format(upscaled_resolution))
        axs[i].contourf(high_res, cmap='terrain')
        fig.colorbar(axs[i].collections[0], ax=axs[i], orientation='vertical', fraction=0.02, pad=0.04)
    #Display the low res input as a contour plot with a colorbar and set the title to "Low Resolution"
    axs[-1].set_title('Low Resolution')
    axs[-1].contourf(low_res, cmap='terrain')
    fig.colorbar(axs[-1].collections[0], ax=axs[-1], orientation='vertical', fraction=0.02, pad=0.04)
    #If a save path is provided, save the plot to the specified path
    if save_path:
        plt.savefig(save_path)
    #If save_only is False, display the plot
    if not save_only:
        plt.show()