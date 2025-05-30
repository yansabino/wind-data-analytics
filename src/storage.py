import geopandas as gpd
import os

def save_for_tableau(gdf: gpd.GeoDataFrame, filepath: str) -> None:
    """
    Salva os dados em formato CSV para o Tableau.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    gdf.drop(columns='geometry').to_csv(filepath, index=False) 