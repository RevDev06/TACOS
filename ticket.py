from fpdf import FPDF
from datetime import datetime
import pymysql

from db import CBD
from inicio import Carrito

cbd = CBD()
cbd.conectar()
conex = CBD()
cc = Carrito()

cursor = cbd.cursor
cursor.execute('SELECT id, nombre, costo FROM productos WHERE id = %s', (id,))
compra = cursor.fetchone

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 35)
        self.cell(0, 10, 'T C A O S - E', 0, 1, 'C')
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Ticket de compra', 0, 1, 'C')

        self.cell(0, 10, '==============================================', 0, 1, 'C')
        self.cell(0, 10, f'Fecha y hora: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'C')
        self.cell(0, 10, '==============================================', 0, 1, 'C')



    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

pdf = PDF()
pdf.add_page()
pdf.set_font('Arial', '', 12)

# Consultar la base de datos
cursor.execute('SELECT id, nombre, descripcion, costo FROM productos WHERE id = %s', (id,))
compra = cursor.fetchone()

# Verificar si la consulta devolvió algún resultado
if compra is not None:
    # Asignar valores a las variables
    id = compra[0]
    nombre = compra[1]
    descripcion = compra[2]
    costo = compra[3]

    # Agregar contenido al ticket
    pdf.cell(0, 10, '==============================================', 0, 1, 'C')
    pdf.cell(0, 10, f'#{id}   {nombre}        ${costo}', 0, 1, 'C')
    pdf.cell(0, 10, f'Descripción: {descripcion}', 0, 1, 'C')
    pdf.cell(0, 10, '==============================================', 0, 1, 'C')
    pdf.cell(0, 10, '==============================================', 0, 1, 'C')
    pdf.cell(0, 10, 'TOTAL: {total}', 0, 1, 'C')
    pdf.cell(0, 10, '==============================================', 0, 1, 'C')
    pdf.cell(0, 10, 'ESTE NO ES UN COMPROBANTE FISCAL', 0, 1, 'C')


else:
    # Si no se encontró ningún resultado, imprimir un mensaje de error o manejar la situación de otra manera
    print("No se encontró ningún producto con el ID proporcionado.")


pdf.output('ticket_compra.pdf')
