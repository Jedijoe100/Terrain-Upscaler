import json
import sys
import sqlite3
from dotenv import load_dotenv
from convertbng.util import convert_bng, convert_epsg3857_to_wgs84
load_dotenv()

from PIL.ImageShow import show
import numpy as np
import PIL.Image as Image
from PIL.TiffTags import TAGS
import os
import matplotlib.pyplot as plt
import requests

DATA_PATH = './data/'
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))

#TODO: Add logging instead of print statements
#TODO: Refactor code to separate data loading, preprocessing, model training, and evaluation into separate functions or classes
#TODO: Do model training and evaluation using a suitable machine learning framework (e.g. TensorFlow, PyTorch) and evaluate the model using appropriate metrics (e.g. RMSE, MAE)
#TODO: Add functionality to save the trained model and use it for inference on new data

#Import data from 
def load_data(region):
    #load data from data/data_sets.json
    with Image.open(os.path.join(WORKING_DIR, DATA_PATH, region['High Res File'])) as img:
        high_res = img.copy()
    with Image.open(os.path.join(WORKING_DIR, DATA_PATH, region['Low Res File'])) as img:
        low_res = img.copy()
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].set_title('High Resolution')
    axs[0].contourf(high_res, cmap='terrain')
    axs[1].set_title('Low Resolution')
    axs[1].contourf(low_res, cmap='terrain')
    plt.show()
    return (region['id'], region, np.array(high_res), np.array(low_res))
    #get metadata

def preprocess_data(data):
    # Perform any necessary preprocessing on the data (e.g., normalization, augmentation)
    # resultant data has the point and its 8 surrounding low res pixels as input and the corresponding 9 high res pixels as output
    high_res_shape = data[2].shape
    low_res_shape = data[3].shape
    print('High Res Shape: {}, Low Res Shape: {}'.format(high_res_shape, low_res_shape))
    low_res_input = np.zeros(((low_res_shape[0]-2)*(low_res_shape[1]-2), 9))
    low_res_input[:, 0] = data[3][:-2, :-2].flatten() # top left
    low_res_input[:, 1] = data[3][:-2, 1:-1].flatten() # top middle
    low_res_input[:, 2] = data[3][:-2, 2:].flatten() # top right
    low_res_input[:, 3] = data[3][1:-1, :-2].flatten() # middle left
    low_res_input[:, 4] = data[3][1:-1, 1:-1].flatten() # middle middle
    low_res_input[:, 5] = data[3][1:-1, 2:].flatten() # middle right
    low_res_input[:, 6] = data[3][2:, :-2].flatten() # bottom left
    low_res_input[:, 7] = data[3][2:, 1:-1].flatten() # bottom middle
    low_res_input[:, 8] = data[3][2:, 2:].flatten() # bottom right
    high_res_output = np.zeros(((low_res_shape[0]-2)*(low_res_shape[1]-2), 9))
    high_res_output[:, 0] = data[2][3:-3:3, 3:-3:3].flatten() # top left
    high_res_output[:, 1] = data[2][3:-3:3, 4:-3:3].flatten() # top middle
    high_res_output[:, 2] = data[2][3:-3:3, 5:-3:3].flatten() # top right
    high_res_output[:, 3] = data[2][4:-3:3, 3:-3:3].flatten() # middle left
    high_res_output[:, 4] = data[2][4:-3:3, 4:-3:3].flatten() # middle middle
    high_res_output[:, 5] = data[2][4:-3:3, 5:-3:3].flatten() # middle right
    high_res_output[:, 6] = data[2][5:-3:3, 3:-3:3].flatten() # bottom left
    high_res_output[:, 7] = data[2][5:-3:3, 4:-3:3].flatten() # bottom middle
    high_res_output[:, 8] = data[2][5:-3:3, 5:-3:3].flatten() # bottom right
    print('Low Res Input Shape: {}, High Res Output Shape: {}'.format(low_res_input.shape, high_res_output.shape))
    return (data[0], data[1], low_res_input, high_res_output)


def request_data(region):
    #Initialising coordinates for OpenTopography API - convert from BNG to WGS84
    north = region['Ymax'] - 90
    south = region['Ymin'] - 90
    west = region['Xmin']
    east = region['Xmax']
    print('Converted coordinates for region {}: West: {}, South: {}, East: {}, North: {}'.format(region['id'], west, south, east, north))
    #Request data from OpenTopography using API key in secrets.env
    api_url = 'https://portal.opentopography.org/API/globaldem'
    #30m resolution data
    high_res = requests.get(api_url, params={
        'demtype': 'COP30',
        'south': south,
        'north': north,
        'west': west,
        'east': east,
        'API_Key': os.getenv('OPEN_TOPOGRAPHY_KEY')
        })
    low_res = requests.get(api_url, params={
        'demtype': 'COP90',
        'south': south,
        'north': north,
        'west': west,
        'east': east,
        'API_Key': os.getenv('OPEN_TOPOGRAPHY_KEY')
    })
    #handle errors properly
    print('Received data for region {}: High Res Status Code: {}, Low Res Status Code: {}'.format(region['id'], high_res.status_code, low_res.status_code))
    #save tiff files to data directory
    with open(os.path.join(WORKING_DIR, DATA_PATH, 'high_res_{}.tif'.format(region['id'])), 'wb') as f:
        f.write(high_res.content)
    with open(os.path.join(WORKING_DIR, DATA_PATH, 'low_res_{}.tif'.format(region['id'])), 'wb') as f:
        f.write(low_res.content)
    if high_res.status_code != 200 or low_res.status_code != 200:
        raise Exception('Failed to retrieve data for region {}, see tif files for more details'.format(region['id']))
    region['High Res File'] = 'high_res_{}.tif'.format(region['id'])
    region['Low Res File'] = 'low_res_{}.tif'.format(region['id'])
    return region


if __name__ == "__main__":
    data_set_to_use = sys.argv[1] if len(sys.argv) > 1 else 0
    con = sqlite3.connect(os.path.join(WORKING_DIR, 'data.db'))
    selected_regions = con.execute('SELECT * FROM regions where type = ?', (data_set_to_use,)).fetchall()
    if len(selected_regions) == 0:
        print('No regions found for type {}'.format(data_set_to_use))
        sys.exit(1)
    else:
        print('Found {} regions for type {}'.format(len(selected_regions), data_set_to_use))
    regions_processed = []
    data = []
    for region in selected_regions:
        region_dict = {
            'id': region[0],
            'type': region[1],
            'Xmin': region[2],
            'Xmax': region[3],
            'Ymin': region[4],
            'Ymax': region[5]
        }
        if region[6] == None or region[7] == None or not os.path.exists(os.path.join(WORKING_DIR, DATA_PATH, region[6])) or not os.path.exists(os.path.join(WORKING_DIR, DATA_PATH, region[7])):
            print('Requesting data for region {}'.format(region_dict['id']))
            request_data(region_dict)
            con.execute('UPDATE regions SET low_res_file = ?, high_res_file = ? WHERE id = ?', (region_dict['Low Res File'], region_dict['High Res File'], region_dict['id']))
            con.commit()
        else:
            print('Data already exists for region {}'.format(region_dict['id']))
            region_dict['High Res File'] = region[6]
            region_dict['Low Res File'] = region[7]
        preprocess_data(load_data(region_dict))
        #data.append(load_data(region_dict))
    
    #Preprocess data
    
    #Train model
    
    #Evaluate model