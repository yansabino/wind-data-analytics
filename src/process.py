import geopandas as gpd
import pandas as pd

BRAZIL_BOUNDARY_PATH = '../brazil_boundary_data/brazil_Brazil_Country_Boundary.shp'

def process_data(df: pd.DataFrame) -> gpd.GeoDataFrame:
    """
    Processa os dados brutos do DataFrame de entrada, convertendo coordenadas UTM para
    latitude e longitude, limpa dados inválidos/outliers, e filtra pontos que estão
    fora do limite territorial do Brasil.

    Etapas:
    1. Converte coordenadas X, Y e FUSO_AG (UTM) para latitude e longitude (EPSG:4326).
    2. Remove linhas com valores inválidos (infinito ou NaN) em latitude ou longitude.
    3. Remove outliers na coluna POT_MW (potência), definindo um limite superior (ex: 20 MW).
    4. Filtra pontos geograficamente para incluir apenas aqueles dentro do limite do Brasil
       usando o shapefile em BRAZIL_BOUNDARY_PATH.

    Args:
        df (pd.DataFrame): DataFrame com colunas 'X', 'Y' e 'FUSO_AG', e outras colunas
                         que serão mantidas no resultado.

    Returns:
        gpd.GeoDataFrame: GeoDataFrame limpo e filtrado com colunas 'latitude',
                          'longitude' e as colunas originais, contendo apenas
                          aerogeradores válidos dentro do território brasileiro.
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

    initial_rows = len(gdf_final)
    print(f"Número inicial de linhas após o processamento inicial: {initial_rows}")

    
    print("Limpando valores inválidos de latitude e longitude...")
    
    gdf_cleaned_coords = gdf_final.replace([float('inf'), float('-inf')], pd.NA).dropna(subset=['latitude', 'longitude'])
    rows_after_coord_cleaning = len(gdf_cleaned_coords)
    rows_removed_coord = initial_rows - rows_after_coord_cleaning
    print(f"Linhas removidas devido a coordenadas inválidas: {rows_removed_coord}")

    pot_mw_threshold = 20.0
    print(f"Removendo outliers de POT_MW acima de {pot_mw_threshold} MW...")
    gdf_cleaned_coords['POT_MW'] = pd.to_numeric(gdf_cleaned_coords['POT_MW'], errors='coerce')
    gdf_cleaned_outliers = gdf_cleaned_coords.dropna(subset=['POT_MW'])[gdf_cleaned_coords['POT_MW'] <= pot_mw_threshold]

    rows_after_outlier_cleaning = len(gdf_cleaned_outliers)
    rows_removed_outliers = rows_after_coord_cleaning - rows_after_outlier_cleaning
    print(f"Linhas removidas devido a outliers de POT_MW: {rows_removed_outliers}")

    print("Realizando verificação geográfica...")

    try:
        gdf_brazil = gpd.read_file(BRAZIL_BOUNDARY_PATH)
    except Exception as e:
        print(f"Erro ao ler o shapefile do limite do Brasil: {e}")
        print("Pulando filtragem geográfica.")
        return gdf_cleaned_outliers # Return data after outlier cleaning if boundary file fails

    if gdf_cleaned_outliers.crs != gdf_brazil.crs:
        print(f"Reprojetando dados de aerogeradores de {gdf_cleaned_outliers.crs} para {gdf_brazil.crs}...")
        gdf_cleaned_outliers = gdf_cleaned_outliers.to_crs(gdf_brazil.crs)

    gdf_windmills_within_brazil = gpd.sjoin(gdf_cleaned_outliers, gdf_brazil, predicate='within', how='inner')

    rows_after_geo_check = len(gdf_windmills_within_brazil)
    rows_removed_geo_relative_to_initial = rows_after_outlier_cleaning - rows_after_geo_check

    print(f"Linhas removidas porque estão fora do limite do Brasil: {rows_removed_geo_relative_to_initial}")
    print(f"Número final de linhas após toda a limpeza e filtragem: {rows_after_geo_check}")

    gdf_final_cleaned = gdf_windmills_within_brazil.drop(columns=[col for col in gdf_windmills_within_brazil.columns if 'index_' in col], errors='ignore')

    return gdf_final_cleaned

