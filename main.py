from createFactura import create_invoice
from openSalesReport import generate_invoice_data
import pandas as pd
import pprint


# Uso del método CAMBIAR FILEPATH de reporteVentas 
reporte_ventas_path = 'bd\\reportesVentas.xlsx'
data_inmobiliarias_path = 'bd\\dataInmobiliarias_updatedFeb.xlsx'

invoice_data = generate_invoice_data(reporte_ventas_path, data_inmobiliarias_path)


pprint.pprint(invoice_data, indent=2)


df = pd.read_excel(data_inmobiliarias_path, sheet_name='Costumer')


create_invoice(invoice_data, df )