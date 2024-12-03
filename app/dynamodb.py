import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import streamlit as st
import json

AWS_REGION = "us-east-1"

def get_dynamodb_table(table_name):
    """Conecta a DynamoDB y devuelve la tabla."""
    try:
        dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
        table = dynamodb.Table(table_name)
        return table
    except (NoCredentialsError, PartialCredentialsError):
        st.error("No se encontraron credenciales de AWS. Verifica tu configuración.")
        return None

def fetch_data(table_name):
    """
    Obtiene datos de una tabla DynamoDB y asegura que las columnas clave como 'data' sean incluidas correctamente.
    
    Args:
        table_name (str): Nombre de la tabla en DynamoDB.
    
    Returns:
        list: Lista de elementos obtenidos de la tabla.
    """
    table = get_dynamodb_table(table_name)
    if not table:
        return []
    
    try:
        items = []
        response = table.scan()
        items.extend(response.get('Items', []))
        
        # Manejar paginación
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response.get('Items', []))
        
        # Verificar y procesar la columna 'data'
        for item in items:
            if "data" in item:
                if isinstance(item["data"], str):
                    try:
                        item["data"] = json.loads(item["data"])  # Decodificar JSON si es una cadena
                    except json.JSONDecodeError:
                        st.warning(f"No se pudo decodificar 'data' para el item: {item}")
                elif isinstance(item["data"], dict):
                    item["data"] = item["data"]  # Si ya es un diccionario, mantenerlo
        
        return items
    
    except Exception as e:
        st.error(f"Error al leer la tabla {table_name}: {e}")
        return []


matches_data = fetch_data("matches")
print(matches_data[:1])  # Muestra las primeras 5 filas
