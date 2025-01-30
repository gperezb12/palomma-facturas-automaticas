import pandas as pd 

def generate_invoice_data(reporte_ventas_path, data_inmobiliarias_path):
    # Leer los archivos
    reporte_ventas_df = pd.read_excel(reporte_ventas_path, sheet_name= "Reporte Rentals")  # AGREGAR EL SHEET NAME PARA EL FUTURO!!!
    data_inmobiliarias_df = pd.read_excel(data_inmobiliarias_path, sheet_name='Costumer')
    reporte_ventas_df_payouts = pd.read_excel(reporte_ventas_path, sheet_name= "Reporte RentalsPayouts")
    
    # Crear un diccionario para mapear los métodos de pago a los códigos
    payment_method_codes = {
        "pse": 9,
        "bancolombiaButton": 6,
        "nequiButton": 8,
    }
    
    # Crear un diccionario para mapear los métodos de pago a sus descripciones
    payment_method_descriptions = {
        "pse": "Servicios de tecnología de pagos - PSE",
        "bancolombiaButton": "Servicios de tecnología de pagos - Botón Bancolombia",
        "nequiButton": "Servicios de tecnología de pagos - Botón Nequi",
    }
    
    # Crear un diccionario para determinar si aplica retefuente
    retefuente_dict = dict(zip(data_inmobiliarias_df["MerchantID"], data_inmobiliarias_df["RTE Fuente"]))

    # Diccionario final
    invoice_dict = {}


    for _, row in reporte_ventas_df.iterrows():
        merchant_id = row["rentalsMerchantId"]
        payment_method = row["paymentMethod"]
        fee = row["fee"]
        razon_social = row["rentalsMerchantId"]
        
        # Ignorar métodos de pago "card"
        if payment_method == "card":
            continue

        # Determinar si aplica retefuente
        aplica_retefuente = retefuente_dict.get(razon_social, "NO") == "SI"
        # Calcular el precio
        if aplica_retefuente:
            price =  round(fee / 1.155)
            
        else:
            price =  round(fee / 1.19)

        # Base del item
        item = {
            "code": str(payment_method_codes.get(payment_method, "0")),  # Código según el método de pago
            "description": payment_method_descriptions.get(payment_method, "Descripción no definida"),
            "quantity": 1,
            "price": price,
            "taxes": [{"id": 11917}],  # IVA 19%
        }

        # Agregar retefuente si aplica
        if aplica_retefuente:
            item["taxes"].append({"id": 11934})  # ReteFuente 3.5%

        # Añadir al diccionario final

        if merchant_id not in invoice_dict:
            invoice_dict[merchant_id] = []

        invoice_dict[merchant_id].append(item)

    for _, row in reporte_ventas_df_payouts.iterrows():
        merchant_id = row["rentalsMerchantId"]
        fixed_fee = row["fixedFee"]
        variable_fee = row["variableFee"]
        
        # Agregar fixedFee si es mayor a 0
        if fixed_fee > 0:
            fixed_fee_price = round(fixed_fee / 1.155)
            item_fixed_fee = {
                "code": "5",  # Código para Dispersiones
                "description": "Servicio de tecnología de pagos Dispersiones",
                "quantity": 1,
                "price": fixed_fee_price,
                "taxes": [{"id": 11917}, {"id": 11934}],  # IVA y retefuente
            }

            if merchant_id in invoice_dict:
                invoice_dict[merchant_id].append(item_fixed_fee)
            else:
                invoice_dict[merchant_id] = [item_fixed_fee]

        # Agregar variableFee (sin impuestos)
        if variable_fee > 0:
            item_variable_fee = {
                "code": "5",  # Código para Dispersiones
                "description": "Servicio de tecnología de pagos Dispersiones",
                "quantity": 1,
                "price": round(variable_fee, 2),  # Sin impuestos
            }
            if merchant_id in invoice_dict:
                invoice_dict[merchant_id].append(item_variable_fee)
            else:
                invoice_dict[merchant_id] = [item_variable_fee]


    return invoice_dict





