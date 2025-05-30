import sys
sys.path.append('../src')

from extract import fetch_data_from_arcgis
from process import process_data
from storage import save_for_tableau
from utils import log

# Configurações
API_URL = "https://sigel.aneel.gov.br/arcgis/rest/services/PORTAL/WFS/MapServer/0/query"
PARAMS = {
    "where": "1=1",
    "outFields": "*",
    "f": "json"
}

log("Iniciando extração de dados...")
df_raw = fetch_data_from_arcgis(API_URL, PARAMS)

log("Processando dados...")
gdf_clean = process_data(df_raw)
log(gdf_clean.head())

log("Salvando dados para Tableau...")
save_for_tableau(gdf_clean, "data/processed/aerogeradores.csv")

log("Pipeline finalizado!")