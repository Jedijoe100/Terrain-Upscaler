# Terrain-Upscaler
Terrain upscaling using Neural Network (XGBoost). This can upscale raster data $3^n$ times (with n being the amount to upscale) and can be loaded with loader.py.

## Usage
After install the requirements to train on the test dataset run the following in terminal:
```
python trainer.py test
```
To use the test model run the following command in terminal:
```
python loader.py test
```

## Details
Different regions are chosen and loaded into a sqlite database with a category to allow for different models to be trained depending on terrain type (Mountainous, Dunes, Dry Rocks, Forest, etc.).
If data is not stored locally for the required values in the database it will pull the height maps from OpenTopography using an API.
The data is then trained using a XGBoost method with the data preprocessed to allow for training.
The models are then stored allowing the loader to use the model without retraining.

## Data Sources
Two data sources were used:
High Resolution Data: European Space Agency (2024).  <i>Copernicus Global Digital Elevation Model</i>.  Distributed by OpenTopography.  https://doi.org/10.5069/G9028PQB. Accessed 2026-04-13
Low Resolution Data: European Space Agency (2024).  <i>Copernicus Global Digital Elevation Model</i>.  Distributed by OpenTopography.  https://doi.org/10.5069/G9028PQB. Accessed 2026-04-13
