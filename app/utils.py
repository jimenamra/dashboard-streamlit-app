import pandas as pd
import json
import ast

def extract_parsed_data(df, column_name='data', key_to_extract='competition_name'):
    """
    Extrae un valor específico de una clave en una columna en formato JSON dentro de un DataFrame.
    
    Args:
        df (pd.DataFrame): El DataFrame que contiene la columna a procesar.
        column_name (str): El nombre de la columna que contiene los datos en formato JSON.
        key_to_extract (str): La clave cuyo valor deseas extraer.

    Returns:
        pd.DataFrame: DataFrame con una nueva columna con los valores extraídos, nombrada como la clave extraída.
    """
    def extract_value(row):
        if isinstance(row, str):  # Si es un string, limpiarlo y convertirlo a diccionario
            row = row.replace("Decimal('", "").replace("')", "").replace("'", '"')  # Ajustes para JSON válido
            try:
                parsed_row = json.loads(row)  # Parsear el string a diccionario
            except json.JSONDecodeError:
                return None  # Si falla, devolver None
        elif isinstance(row, dict):  # Si ya es un diccionario, usarlo directamente
            parsed_row = row
        else:  # Si no es ni string ni dict, devolver None
            return None
        return parsed_row.get(key_to_extract, None)  # Extraer el valor de la clave

    # Aplicar la extracción y crear una nueva columna con el nombre de la clave extraída
    df[key_to_extract] = df[column_name].apply(extract_value)
    return df


def extract_team_names(df, column_name='data'):
    """
    Extrae los nombres de los equipos (claves del diccionario) de la columna anidada.
    
    Args:
        df (pd.DataFrame): DataFrame principal con una columna anidada.
        column_name (str): Nombre de la columna que contiene los datos en formato string.

    Returns:
        pd.DataFrame: DataFrame con una nueva columna 'team_names' que contiene listas de nombres de equipos.
    """
    def get_team_names(row):
        try:
            # Convertir la fila en un diccionario
            parsed_data = ast.literal_eval(row)
            # Extraer las claves del diccionario (nombres de equipos)
            return list(parsed_data.keys())
        except (ValueError, SyntaxError):
            return None

    # Crear una nueva columna con los nombres de los equipos
    df['team_name'] = df[column_name].apply(get_team_names)
    return df


def expand_positions(lineups_df):
    """
    Extrae y expande la información de posiciones desde la columna 'data' en el DataFrame de alineaciones.
    """
    if "data" not in lineups_df.columns:
        return pd.DataFrame()  # Retorna un DataFrame vacío para evitar errores

    expanded_rows = []
    for _, row in lineups_df.iterrows():
        team_name = row.get("team_name")
        data = row.get("data")

        # Extraer 'positions' de la columna 'data'
        positions = data.get("positions") if isinstance(data, dict) else []

        if not isinstance(positions, list):
            continue

        # Expandir cada posición en una nueva fila
        for position in positions:
            expanded_rows.append({
                "team_name": team_name,
                "position_id": position.get("position_id"),
                "position": position.get("position"),
                "minutes_played": position.get("minutes", 0)  # Ejemplo para agregar tiempo jugado si está disponible
            })

    # Convertir a DataFrame
    expanded_df = pd.DataFrame(expanded_rows)
    return expanded_df
