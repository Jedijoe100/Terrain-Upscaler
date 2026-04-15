import sys
import os
from xgboost import XGBRegressor

from subfunctions.visualisation import visual_results

WORKING_DIR = os.getcwd()

if __name__ == "__main__":
    data_set_to_use = sys.argv[1] if len(sys.argv) > 1 else 0
    model = XGBRegressor()
    model.load_model(os.path.join(WORKING_DIR, 'models', 'model_{}.ubj'.format(data_set_to_use)))
    visual_results(model)
