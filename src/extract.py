import requests
from typing import Optional
import pandas as pd
import time

def fetch_data_from_arcgis(api_url: str, params: Optional[dict] = None) -> pd.DataFrame:
    """
    Coleta todos os dados dos aerogeradores a partir da API ArcGIS da ANEEL, utilizando paginação.
    """
    if params is None:
        params = {}
    all_records = []
    offset = 0
    max_records = 1000  # Valor padrão da maioria das APIs ArcGIS
    while True:
        paged_params = params.copy()
        paged_params["resultOffset"] = offset
        paged_params["resultRecordCount"] = max_records
        response = requests.get(api_url, params=paged_params)
        response.raise_for_status()
        data = response.json()
        features = data.get('features', [])
        if not features:
            break
        records = [f['attributes'] for f in features]
        all_records.extend(records)
        print(f"Registros coletados até agora: {len(all_records)}")
        if len(features) < max_records:
            break  # Última página
        offset += max_records
        time.sleep(0.2)  # Pequeno delay para evitar sobrecarga na API
    return pd.DataFrame(all_records)