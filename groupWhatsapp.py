import pandas as pd

#Open Rentals 

def Open_rentals(file_path):
    df = None 
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    df['settlementDate'] = pd.to_datetime(df['settlementDate'])

    df = df[df['status'] == 'paid']
    df = df[df['paymentSource'] == 'whatsapp']
    return df

def generate_transactions_dict(rentals: pd.DataFrame) -> dict:
    """
    Genera un diccionario con el número de transacciones por rentalsMerchantID.
    
    :param rentals: DataFrame con la columna 'rentalsMerchantID'.
    :return: Diccionario con rentalsMerchantID como clave y el número de transacciones como valor.
    """
    return rentals['rentalsMerchantId'].value_counts().to_dict()





rentalss  = "C:\\Users\\greg2\\Documents\\FacturacionAutomatica\\palomma-facturas-automaticas\\bd\\rentalsSettleEne.csv"
rentals_df = Open_rentals(rentalss)
transacciones = generate_transactions_dict(rentals_df)
