import geopandas as gpd
import pandas as pd

def process_data(df: pd.DataFrame) -> gpd.GeoDataFrame:
    """
    Processa os dados brutos em um GeoDataFrame com latitude e longitude corretas,
    usando a zona UTM (coluna FUSO_AG) para aplicar o EPSG apropriado.

    Args:
        df (pd.DataFrame): DataFrame com colunas 'X', 'Y' e 'FUSO_AG'.

    Returns:
        gpd.GeoDataFrame: GeoDataFrame com colunas 'latitude' e 'longitude' reprojetadas.
    """
    if not {'X', 'Y', 'FUSO_AG'}.issubset(df.columns):
        raise ValueError("As colunas 'X', 'Y' e 'FUSO_AG' são obrigatórias.")

    df = df.dropna(subset=['X', 'Y', 'FUSO_AG'])

    epsg_map = {
        18: 31978,
        19: 31979,
        20: 31980,
        21: 31981,
        22: 31982,
        23: 31983,
        24: 31984,
        25: 31985,
    }

    df = df.dropna(subset=['X', 'Y', 'FUSO_AG'])
    df["FUSO_AG"] = df["FUSO_AG"].str.extract(r"UTM\s*(\d+)").astype(float)

    gdfs = []

    for zona in df["FUSO_AG"].unique():
        if zona not in epsg_map:
            print(f"[WARN] EPSG não encontrado para zona {zona}")
            continue

        epsg = epsg_map[zona]
        sub_df = df[df["FUSO_AG"] == zona].copy()

        if sub_df.empty:
            continue

        gdf = gpd.GeoDataFrame(
            sub_df,
            geometry=gpd.points_from_xy(sub_df.X, sub_df.Y),
            crs=f"EPSG:{epsg}"
        )

        gdf = gdf.to_crs("EPSG:4326")
        gdf["latitude"] = gdf.geometry.y
        gdf["longitude"] = gdf.geometry.x
        gdfs.append(gdf)
    
    if not gdfs:
        raise ValueError("Nenhum GeoDataFrame válido foi criado")

    gdf_final = pd.concat(gdfs).drop_duplicates().reset_index(drop=True)
    return gdf_final

