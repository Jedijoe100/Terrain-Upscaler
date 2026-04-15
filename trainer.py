import sys
import sqlite3
import os
import logging
from dotenv import load_dotenv
from xgboost import XGBRegressor
load_dotenv()
from subfunctions.data_retrieval import request_data
from subfunctions.visualisation import visual_results
from subfunctions.loading import load_data
from subfunctions.preprocessing import preprocess_data
from subfunctions.training import train_model

logger = logging.getLogger(__name__)

MODEL_STORAGE_PATH = './models/'
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))

#TODO: Refactor code to separate data loading, preprocessing, model training, and evaluation into separate functions or classes
#TODO: Do model training and evaluation using a suitable machine learning framework (e.g. TensorFlow, PyTorch) and evaluate the model using appropriate metrics (e.g. RMSE, MAE)
#TODO: Add functionality to save the trained model and use it for inference on new data

if __name__ == "__main__":
    # retrieve the selected data set to train
    data_set_to_use = sys.argv[1] if len(sys.argv) > 1 else 0
    # set the default logging level to INFO, but allow it to be set to DEBUG using an environment variable
    logging_level = logging.DEBUG if os.getenv('DEBUG') == 'true' else logging.INFO
    logging.basicConfig(level=logging_level)
    con = sqlite3.connect(os.path.join(WORKING_DIR, 'data.db'))
    selected_regions = con.execute('SELECT * FROM regions where type = ?', (data_set_to_use,)).fetchall()
    model = XGBRegressor(n_estimators=300, max_depth=10, learning_rate=0.3)
    if len(selected_regions) == 0:
        logger.error('No regions found for type {}'.format(data_set_to_use))
        sys.exit(1)
    else:
        logger.info('Found {} regions for type {}'.format(len(selected_regions), data_set_to_use))
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
        if region[6] == None or region[7] == None or not os.path.exists(os.path.join(WORKING_DIR, os.getenv('DATA_DIR'), region[6])) or not os.path.exists(os.path.join(WORKING_DIR, os.getenv('DATA_DIR'), region[7])):
            logger.info('Requesting data for region {}'.format(region_dict['id']))
            request_data(region_dict)
            con.execute('UPDATE regions SET low_res_file = ?, high_res_file = ? WHERE id = ?', (region_dict['Low Res File'], region_dict['High Res File'], region_dict['id']))
            con.commit()
        else:
            logger.info('Data already exists for region {}'.format(region_dict['id']))
            region_dict['High Res File'] = region[6]
            region_dict['Low Res File'] = region[7]
        id, _, X, Y = preprocess_data(load_data(region_dict))
        train_model(model, id, X, Y)
        #data.append(load_data(region_dict))
    model.save_model(os.path.join(WORKING_DIR, MODEL_STORAGE_PATH, 'model_{}.ubj'.format(data_set_to_use)))
    visual_results(model)
    #Evaluate model