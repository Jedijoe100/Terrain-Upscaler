
import PIL.Image as Image
import os
import numpy as np
import logging
from subfunctions.visualisation import display_as_plot
logger = logging.getLogger(__name__)

WORKING_DIR = os.getcwd()

def load_data(region):
    #load data from data/data_sets.json
    with Image.open(os.path.join(WORKING_DIR, os.getenv('DATA_DIR'), region['High Res File'])) as img:
        high_res = img.copy()
    with Image.open(os.path.join(WORKING_DIR, os.getenv('DATA_DIR'), region['Low Res File'])) as img:
        low_res = img.copy()
    display_as_plot(high_res, low_res, save_path=os.path.join(WORKING_DIR, os.getenv('VISUALISATION_DIR'), 'region_{}.png'.format(region['id'])), save_only=True)    
    logger.info('Region {}: High Res - Max: {}, Min: {}; Low Res - Max: {}, Min: {}'.format(
        region['id'], np.max(high_res), np.min(high_res), np.max(low_res), np.min(low_res)))
    return (region['id'], region, np.array(high_res), np.array(low_res))