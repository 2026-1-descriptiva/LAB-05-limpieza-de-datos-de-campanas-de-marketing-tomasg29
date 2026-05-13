"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel

import os
import zipfile
import pandas as pd


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaign_contacts
    - previous_outcome: cambiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_date: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months
    """
    
    # Crear carpeta de salida
    os.makedirs("files/output", exist_ok=True)
    
    # Buscar todos los archivos .zip en la carpeta files/input/
    zip_files = [f for f in os.listdir("files/input") if f.endswith('.zip')]
    
    if not zip_files:
        raise FileNotFoundError("No se encontraron archivos .zip en files/input/")
    
    # Lista para almacenar todos los DataFrames
    dfs = []
    
    # Leer cada archivo ZIP y concatenar
    for zip_file in zip_files:
        zip_path = os.path.join("files/input", zip_file)
        
        with zipfile.ZipFile(zip_path, 'r') as z:
            # Obtener el primer archivo .csv dentro del ZIP
            csv_files = [f for f in z.namelist() if f.endswith('.csv')]
            if csv_files:
                with z.open(csv_files[0]) as f:
                    df_temp = pd.read_csv(f)
                    dfs.append(df_temp)
    
    # Concatenar todos los DataFrames
    df = pd.concat(dfs, ignore_index=True)
    
    # ==================== client.csv ====================
    client_df = df[['client_id', 'age', 'job', 'marital', 'education', 'credit_default', 'mortgage']].copy()
    
    # Limpiar job: reemplazar "." por "" y "-" por "_"
    client_df['job'] = client_df['job'].astype(str).str.replace('.', '', regex=False).str.replace('-', '_', regex=False)
    
    # Limpiar education: cambiar "." por "_" y "unknown" por pd.NA
    client_df['education'] = client_df['education'].astype(str).str.replace('.', '_', regex=False)
    client_df['education'] = client_df['education'].replace('unknown', pd.NA)
    
    # credit_default: "yes" -> 1, cualquier otro -> 0
    client_df['credit_default'] = client_df['credit_default'].apply(lambda x: 1 if x == 'yes' else 0)
    
    # mortgage: "yes" -> 1, cualquier otro -> 0
    client_df['mortgage'] = client_df['mortgage'].apply(lambda x: 1 if x == 'yes' else 0)
    
    # Guardar client.csv
    client_df.to_csv("files/output/client.csv", index=False)
    
    # ==================== campaign.csv ====================
    campaign_df = df[['client_id', 'number_contacts', 'contact_duration', 'previous_campaign_contacts', 
                      'previous_outcome', 'campaign_outcome', 'day', 'month']].copy()
    
    # previous_outcome: "success" -> 1, cualquier otro -> 0
    campaign_df['previous_outcome'] = campaign_df['previous_outcome'].apply(lambda x: 1 if x == 'success' else 0)
    
    # campaign_outcome: "yes" -> 1, cualquier otro -> 0
    campaign_df['campaign_outcome'] = campaign_df['campaign_outcome'].apply(lambda x: 1 if x == 'yes' else 0)
    
    # last_contact_date: combinar day, month con año 2022
    month_map = {
        'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06',
        'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
    }
    campaign_df['month_num'] = campaign_df['month'].str.lower().map(month_map)
    campaign_df['last_contact_date'] = '2022-' + campaign_df['month_num'] + '-' + campaign_df['day'].astype(str).str.zfill(2)
    
    # Seleccionar columnas finales - USAR EL NOMBRE CORRECTO: previous_campaign_contacts
    campaign_df = campaign_df[['client_id', 'number_contacts', 'contact_duration', 'previous_campaign_contacts',
                                'previous_outcome', 'campaign_outcome', 'last_contact_date']]
    
    # Guardar campaign.csv
    campaign_df.to_csv("files/output/campaign.csv", index=False)
    
    # ==================== economics.csv ====================
    economics_df = df[['client_id', 'cons_price_idx', 'euribor_three_months']].copy()
    
    # Guardar economics.csv
    economics_df.to_csv("files/output/economics.csv", index=False)
    
    return


if __name__ == "__main__":
    clean_campaign_data()