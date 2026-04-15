import os
import logging
import requests

logger = logging.getLogger(__name__)

#get the working directory of the project
WORKING_DIR = os.getcwd()

def request_data(region):
    #Initialising coordinates for OpenTopography API - convert from BNG to WGS84
    north = region['Ymax'] - 90
    south = region['Ymin'] - 90
    west = region['Xmin']
    east = region['Xmax']
    logger.info('Converted coordinates for region {}: West: {}, South: {}, East: {}, North: {}'.format(region['id'], west, south, east, north))
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
    logger.info('Received data for region {}: High Res Status Code: {}, Low Res Status Code: {}'.format(region['id'], high_res.status_code, low_res.status_code))
    #save tiff files to data directory
    with open(os.path.join(WORKING_DIR, os.getenv('DATA_DIR'), 'high_res_{}.tif'.format(region['id'])), 'wb') as f:
        f.write(high_res.content)
    with open(os.path.join(WORKING_DIR, os.getenv('DATA_DIR'), 'low_res_{}.tif'.format(region['id'])), 'wb') as f:
        f.write(low_res.content)
    if high_res.status_code != 200 or low_res.status_code != 200:
        raise Exception('Failed to retrieve data for region {}, see tif files for more details'.format(region['id']))
    region['High Res File'] = 'high_res_{}.tif'.format(region['id'])
    region['Low Res File'] = 'low_res_{}.tif'.format(region['id'])
    return region