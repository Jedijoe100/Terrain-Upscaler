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

#TODO: Add error handling for API requests and file operations
#TODO: Add logging instead of print statements
#TODO: Refactor code to separate data loading, preprocessing, model training, and evaluation into separate functions or classes
#TODO: Do preprocessing of data (e.g. normalisation, augmentation) before training the model
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
    return (region['id'], region, high_res, low_res)
    #get metadata

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
        if region[6] == None or region[7] == None:
            print('Requesting data for region {}'.format(region_dict['id']))
            request_data(region_dict)
            con.execute('UPDATE regions SET low_res_file = ?, high_res_file = ? WHERE id = ?', (region_dict['Low Res File'], region_dict['High Res File'], region_dict['id']))
            con.commit()
        else:
            print('Data already exists for region {}'.format(region_dict['id']))
            region_dict['Low Res File'] = region[6]
            region_dict['High Res File'] = region[7]
        data.append(load_data(region_dict))
    
    #Preprocess data
    
    #Train model
    
    #Evaluate model