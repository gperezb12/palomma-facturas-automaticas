import requests
import pandas as pd
from datetime import datetime
import pprint
import math


# Configuración
SIIGO_URL = "https://api.siigo.com/auth"
SIIGO_USERNAME = "facturas@palomma.com"
SIIGO_ACCESS_KEY = "OGExNzM4ZjUtZWNkNC00NGNkLWJiMzQtNzA5MDc2M2QzODI0OjF7eVVpN2RDZlk="
SELLER_ID = 570

# Aplicar la conversión antes de enviar el payloa
def correct_decimal(value):
    """
    If the decimal part of a float ends in '49', change it to '50', regardless of the number of decimal places.
    
    :param value: A float number to be checked and corrected.
    :return: The corrected float value.
    """
    value_str = str(value)  # Convert to string, remove trailing zeros for precision

    integer_part, _, decimal_part = value_str.partition(".")  # Split into integer and decimal parts

    if decimal_part.endswith("49"):
        # Adjust the last two digits from '49' to '50'
        corrected_decimal_part = decimal_part[:-2] + "50"
        corrected_value_str = f"{integer_part}.{corrected_decimal_part}"
        return float(corrected_value_str)  # Convert back to float
    return value

# Función para obtener el token de acceso
def get_access_token():
    response = requests.post(
        f"{SIIGO_URL}/auth",
        json={
            "username": SIIGO_USERNAME,
            "access_key": SIIGO_ACCESS_KEY,
        },
        headers={"Content-Type": "application/json"}
    )
    response.raise_for_status()
    return response.json()["access_token"]


# Crear la factura
def create_invoice(invoice_dict, data_inmobiliarias_df):
    # Obtener el token
    token = get_access_token()

    for merchant_id, items in invoice_dict.items():
        # Obtener el customer_document a partir del merchant_id en el DataFrame de inmobiliarias
        customer_document_row = data_inmobiliarias_df[data_inmobiliarias_df["MerchantID"] == merchant_id]
        
        if customer_document_row.empty:
            print(f"Error: No se encontró el documento para el merchant_id: {merchant_id}")
            continue
        
        customer_document = customer_document_row["ID"].values[0]  # Extraer el documento del merchant

        # Calcular el total de la factura
        total_value = 0
        for item in items:
            price = item["price"]
            taxes = item.get("taxes", [])
            

            if len(taxes) == 1:  # Solo IVA
                iva =  round(price*0.19,2)
                total_value += round((price + iva) , 2)
            elif len(taxes) == 2:  # IVA y Retefuente
                iva =  round(price*0.155,2)
                total_value += round((price + iva),2)
            
            else:
                total_value += round(price,2) #Esto se hace para los elementos que no tienen impuestos
        
        total = total_value
        print(total)
        
        # Parámetros de la factura
        invoice_payload = {
            "document": {"id": 26990},  # Factura electrónica
            "date": datetime.now().strftime("%Y-%m-%d"),
            "customer": {
                "identification": str(customer_document),
            },
            "seller": SELLER_ID,
            "stamp": {"send": False},  # No enviar a la DIAN
            "items":items,  # Los items generados anteriormente
            "payments": [
                {
                    "id": 5105,  # ID de la forma de pago "Crédito"
                    "value": total,
                    "due_date": datetime.now().strftime("%Y-%m-%d"),
                },
            ]
        }
        # Headers revisados
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Partner-Id": "palomma" 
        }



        pprint.pprint(invoice_payload, indent=2)
        
        # Enviar la solicitud para crear la factura
        invoice_url = "https://api.siigo.com/v1/invoices"
        try:
            response = requests.post(invoice_url, json=invoice_payload, headers=headers)
            print("Status Code:", response.status_code)
            response.raise_for_status()
            invoice_id = response.json()["id"]
            print(f"Factura creada con ID: {invoice_id}")
        except requests.exceptions.HTTPError as e:
            # Mostrar más detalles del error
            print("Error al crear la factura:")
            print("Status Code:", e.response.status_code)
            print("Headers:", e.response.headers)
            print("Error Response:", e.response.text)
        
            