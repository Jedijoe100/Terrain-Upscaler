import logging
import numpy as np
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)

def train_model(model, id, X, Y):
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    rmse = np.sqrt(np.mean((y_test - y_pred) ** 2))
    logger.info('Region {}: RMSE: {}'.format(id, rmse))

