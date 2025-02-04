from createFactura import create_invoice
from openSalesReport import generate_invoice_data
import pandas as pd
import pprint


# Uso del método
reporte_ventas_path = 'bd\\reportesVentas_Ene22a31.xlsx'
data_inmobiliarias_path = 'bd\\dataInmobiliarias.xlsx'

invoice_data = generate_invoice_data(reporte_ventas_path, data_inmobiliarias_path)


pprint.pprint(invoice_data, indent=2)

df = pd.read_excel(data_inmobiliarias_path, sheet_name='Costumer')


create_invoice(invoice_data, df )