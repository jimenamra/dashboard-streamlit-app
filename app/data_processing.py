import json
import pandas as pd

def extract_dynamodb_data(raw_data):
    """
    Extrae y transforma los datos de la columna 'data' en DynamoDB.
    Convierte cada entrada de la lista 'data' en filas individuales en el DataFrame.
    Asigna valores por defecto si las claves no existen.
    """
    expanded_data = []

    for record in raw_data:
        # Verificar si 'data' existe en el registro y es una lista
        if "data" in record and isinstance(record["data"], list):
            for entry in record["data"]:
                expanded_record = {}
                try:
                    # Expandir los campos del diccionario dentro de 'data'
                    for key, value in entry.items():
                        if isinstance(value, dict):
                            if "S" in value:
                                expanded_record[key] = value["S"]  # String
                            elif "N" in value:
                                expanded_record[key] = int(value["N"])  # Número
                            elif "BOOL" in value:
                                expanded_record[key] = value["BOOL"]  # Booleano
                            elif "NULL" in value:
                                expanded_record[key] = None  # Nulo
                            else:
                                expanded_record[key] = "No existe"
                        else:
                            expanded_record[key] = value  # Para valores simples
                    # Incorporar otras columnas del registro fuera de 'data'
                    for k, v in record.items():
                        if k != "data":
                            expanded_record[k] = v
                except Exception as e:
                    expanded_record["error"] = f"Error al procesar entrada: {e}"
                expanded_data.append(expanded_record)
        else:
            # Si 'data' no existe o no es una lista, agregar el registro como está
            expanded_data.append(record)

    # Convertir los datos expandidos en DataFrame
    df = pd.DataFrame(expanded_data)

    # Asignar valores por defecto a columnas faltantes
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].fillna("No existe")  # Texto
        elif pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(0)  # Numéricos

    return df


def process_competitions(raw_data):
    """
    Procesa la tabla competitions expandiendo la columna 'data'.

    Args:
        raw_data (list): Datos crudos de competitions.

    Returns:
        pd.DataFrame: DataFrame procesado.
    """
    df = extract_dynamodb_data(raw_data)
    df.to_csv("data/competitions_processed.csv", index=False)
    return df


def process_matches(raw_data):
    """
    Procesa la tabla matches expandiendo la columna 'data'.

    Args:
        raw_data (list): Datos crudos de matches.

    Returns:
        pd.DataFrame: DataFrame procesado.
    """
    df = extract_dynamodb_data(raw_data)
    df.to_csv("data/matches_processed.csv", index=False)
    return df


def process_lineups(raw_data):
    """
    Procesa la tabla lineups expandiendo la columna 'data'.

    Args:
        raw_data (list): Datos crudos de lineups.

    Returns:
        pd.DataFrame: DataFrame procesado.
    """
    df = extract_dynamodb_data(raw_data)
    df.to_csv("data/lineups_processed.csv", index=False)
    return df


def process_events(raw_data):
    """
    Procesa la tabla events expandiendo la columna 'data'.

    Args:
        raw_data (list): Datos crudos de events.

    Returns:
        pd.DataFrame: DataFrame procesado.
    """
    df = extract_dynamodb_data(raw_data)
    df.to_csv("data/events_processed.csv", index=False)
    return df
