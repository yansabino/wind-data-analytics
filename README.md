# Wind Data Analytics - ANEEL Wind Turbine Case

## Overview
This project implements a data pipeline to extract, process, and export wind turbine data from the ANEEL ArcGIS API. The processed data is ready for geospatial analysis and visualization (e.g., in Tableau). The pipeline is written in Python and includes modular scripts for extraction, transformation, and storage.

## Project Structure
```
data_analytics_case/
├── data/
│   └── processed/
│       └── aerogeradores.csv      # Main processed output (CSV)
├── notebooks/
│   └── main.ipynb                # Jupyter notebook running the pipeline
├── src/
│   ├── extract.py                # Data extraction from ArcGIS API
│   ├── process.py                # Data cleaning and geospatial transformation
│   ├── storage.py                # Export to CSV for Tableau
│   ├── utils.py                  # Logging utility
│   └── run.py                    # Main pipeline script (optional)
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
```

## Setup

1. **Clone the repository** and navigate to the `data_analytics_case` folder.
2. **(Recommended) Create a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Jupyter Notebook
- Open `notebooks/main.ipynb` for an interactive, step-by-step example of the pipeline.
- The notebook will:
  - Fetch wind turbine data from the ANEEL ArcGIS API
  - Process and clean the data, converting coordinates to latitude/longitude
  - Save the processed data as `data/processed/aerogeradores.csv`

### Script (Optional)
- You may also run the pipeline as a script (if implemented in `src/run.py`):
  ```bash
  python src/run.py
  ```

## Output

- **Main output:** `data/processed/aerogeradores.csv`
- **Description:** CSV file with georeferenced wind turbine data, ready for Tableau or other analytics tools.
- **Example columns:**
  - POT_MW, ALT_TOTAL, ALT_TORRE, DIAM_ROTOR, DATA_ATUALIZACAO, EOL_VERSAO_ID, NOME_EOL, DEN_AEG, X, Y, VERSAO, DATUM_EMP, OPERACAO, FUSO_AG, PROPRIETARIO, ORIGEM, OBJECTID, UF, CEG, latitude, longitude

## Modules

- **extract.py**: Fetches data from the ANEEL ArcGIS API.
- **process.py**: Cleans and transforms the data, handling geospatial projections and extracting latitude/longitude.
- **storage.py**: Exports the processed data to CSV.
- **utils.py**: Simple logging utility.
- **run.py**: (Optional) Orchestrates the full pipeline.

## Requirements

- Python 3.8+
- pandas
- geopandas
- requests
- jupyter (for notebooks)

## License

MIT License (or specify your license)

## Author

###Yan Sabino Corrêa