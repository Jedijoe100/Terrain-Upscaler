# Terrain-Upscaler
Terrain upscaling using Neural Network.

Different regions are chosen and loaded into a sqlite database with a category to allow for different models to be trained depending on terrain type (Mountainous, Dunes, Dry Rocks, Forest, etc.).
If data is not stored locally for the required values in the database it will pull the height maps from OpenTopography using an API.

## Data Sources
Two data sources were used:
High Resolution Data: European Space Agency (2024).  <i>Copernicus Global Digital Elevation Model</i>.  Distributed by OpenTopography.  https://doi.org/10.5069/G9028PQB. Accessed 2026-04-13
Low Resolution Data: European Space Agency (2024).  <i>Copernicus Global Digital Elevation Model</i>.  Distributed by OpenTopography.  https://doi.org/10.5069/G9028PQB. Accessed 2026-04-13
