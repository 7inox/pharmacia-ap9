from pathlib import Path
from collections import Counter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
import shutil

root=Path(__file__).resolve().parents[1]
styles=getSampleStyleSheet()
styles['Normal'].fontSize=10
styles['Normal'].leading=14
styles['Title'].fontSize=21
styles['Heading2'].fontSize=13
story=[]
def p(text,style='Normal'):
    story.append(Paragraph(text,styles[style])); story.append(Spacer(1,7))
def table(data,widths):
    rows=[[Paragraph(str(v),styles['Normal']) for v in row] for row in data]
    t=Table(rows,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e3edf6')),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#c6d1db')),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    story.append(t);story.append(Spacer(1,12))
def footer(c,doc):
    c.setFont('Helvetica',8);c.setFillColor(colors.HexColor('#52667a'))
    c.drawString(42,26,'LP2 - AA9 | Tinoco | 11/10/2026')
    c.drawRightString(553,26,str(doc.page))

p('Pruebas de ventas y reporte por categoría','Title')
p('Lenguaje de Programación II - AA9 / S9','Heading2')
p('Miguel Ángel Tinoco López | Ejecución: 11 de octubre de 2026')
p('Entorno: Angular pharma-frontend, API Spring Boot Practica y Oracle local. Se trabajó en una copia del proyecto y se usaron clientes/productos sintéticos. Se implementaron Ventas y Reporte por categoría; el backend se conserva para documentar su comportamiento real.')
p('C1. Resultado de la matriz','Heading2')
table([['Grupo','Pasan','Fallan','Parcial'],['Buscadores','3','0','0'],['Cálculos','5','0','0'],['Validaciones','4','2','0'],['Confirmación','3','0','0'],['Mensajes','2','0','0'],['Impresión','0','0','1'],['Consistencia','1','0','0'],['Total: 21 casos','18','2','1']],[260,65,65,70])
p('La matriz contiene 17 casos base y cuatro propios de grupos distintos: B-03, C-05, V-06 y F-03. Veinte casos se completaron y uno quedó parcial. I-01 no se cuenta como aprobado. La matriz detallada y los archivos de evidencia acompañan el código.')
p('Cálculos de referencia: 12.50 x 3 = 37.50; 18.90 x 3 = 56.70. En C-03: 56.70 + 37.50 + 10.00 = 104.20; al retirar la línea central queda 66.70. La venta 1 devolvió ese total y dos detalles. El stock de productos 42 y 46 pasó de 30 a 27 y de 30 a 28.')
p('Reporte histórico observado antes de repetir pruebas en Postman: 11 unidades, S/125.70, ventas 1-4. Rango invertido bloqueado; fechas futuras muestran vacío. Se adaptó unidadesVendidas de Practica a cantidadVendida del frontend.')
story.append(PageBreak())
p('C2. Hallazgos y correcciones propuestas','Heading2')
p('<b>V-02 - Alta: cantidades decimales aceptadas por la API.</b> La SPA rechaza 0 y 2.5. POST con cantidad 2.5 obtuvo 201; el detalle registrado tiene cantidad 2 y total S/25.00. Evidencia: V-02_http.json y captura V-02_spa.jpg; repetición en Postman. Causa probable: coerción decimal a Integer antes de la validación de DetalleVentaRequestDTO. Corrección en backend: deshabilitar coerción float-to-int en Jackson y conservar @Positive; verificar 0, -1, 2.5 y enteros positivos con pruebas de integración.')
p('<b>V-05 - Media: productos duplicados admitidos.</b> Dos líneas con producto 47 y cantidad 1 cada una obtuvieron 201, total S/14.00. Evidencia: V-05_http.json. La regla elegida es rechazar productos repetidos. Causa probable: VentaServiceImpl.registrar procesa cada detalle sin comprobar IDs duplicados. Corrección en backend: validar unicidad con un conjunto antes de descontar stock; devolver error de negocio. La SPA ya combina el producto en una sola línea.')
p('<b>I-01 - Media, ejecución parcial: no están las tres impresiones PDF.</b> Se implementó impresión de venta y consulta con CSS que oculta navegación y controles; se invocó el botón de impresión. No se verificó salida final de tres PDF. Practica no expone anulación y no hubo una venta anulada disponible. Corrección: completar flujo de anulación con reposición de stock y dato controlado; luego guardar y revisar PDF de venta registrada, anulada y consulta filtrada. No se afirma que el sello o la salida PDF estén verificados.')
p('Evidencias y alcance','Heading2')
p('Las capturas de la SPA están en docs/evidencias. Los JSON HTTP se obtuvieron contra API real mediante PowerShell; no son capturas de Network. La colección postman/PharmaSoft-S9-Ventas.json fue importada en Postman. M-02 se repitió allí y devolvió 409 para cliente inactivo. M-01 usa dos pestañas: la primera agota stock y la segunda recibe 409, conserva las líneas y actualiza stock; no prueba solicitudes simultáneas ni bloqueo de base de datos.')
p('Validación técnica: compilación AOT con ngc y 15 pruebas de lógica pasan. Estas últimas simulan HTTP y no sustituyen la integración real. npm build no pudo completarse por acceso restringido de esbuild a directorios; se probó el frontend AOT en Chrome con un servidor local.')
story.append(PageBreak())
p('C3. Análisis técnico','Heading2')
p('<b>Total estimado y total definitivo.</b> La SPA calcula un estimado usando el precio visible y cantidades válidas. Para evitar errores de coma flotante trabaja con centavos. Ese valor ayuda al usuario a revisar, pero el POST solo envía cliente y detalles. Practica consulta precios, calcula con BigDecimal y devuelve el total definitivo. La consulta y el comprobante deben usar el total del servidor, porque catálogo y stock pueden cambiar después de abrir el formulario.')
p('<b>Producto repetido.</b> En la interfaz elegí incrementar una línea existente. Así el usuario ve una cantidad única y puede compararla con el stock. En la API propongo rechazar IDs repetidos antes de modificar existencias para mantener el mismo contrato y facilitar el comprobante. Si se decide permitirlos, debe agregarse la cantidad por producto y validar stock agregado de forma transaccional; no basta validar cada detalle aisladamente.')
p('<b>Experiencia ante HTTP 409.</b> Se muestra el mensaje devuelto, se cierra el resumen y se conserva cliente y detalles. El formulario vuelve a habilitarse y refresca el catálogo para que el usuario corrija la cantidad sin recargar la página. La prueba con dos pestañas confirmó este comportamiento al agotar el stock. Esto no reemplaza un bloqueo o control de versión en backend para solicitudes verdaderamente simultáneas.')
p('<b>Reporte y consulta de ventas.</b> El reporte agrupa por categoría, recibe fechas opcionales y muestra totales y barras relativas al mayor monto. La API entrega una lista agregada sin paginación. La consulta de ventas muestra registros individuales y permite filtrar; no debe confundirse el número de categorías con el número de ventas ni paginar el reporte en cliente como si representara el total del servidor. Para muchos registros individuales se recomienda paginación en API.')
p('Estado de entrega','Heading2')
p('Rama local: feature/pruebas-reporte-ventas-tinoco. No se hizo push, PR ni envío a B-Learning. Los commits son reales del 11/10/2026; no se cumple el requisito de tres días diferentes. La rama parte de S8 disponible; queda pendiente el procedimiento de integrar práctica S9 en develop y crear la PR correspondiente. Estas limitaciones y la impresión parcial deben revisarse antes de presentar la entrega como completamente conforme.')
p('Archivos: docs/matriz-pruebas-s9.md; docs/informe-s9.pdf; postman/PharmaSoft-S9-Ventas.json; docs/evidencias; scripts/verificar-s9.cjs. La matriz distingue los resultados reales de la verificación simulada.')
out=root/'docs'/'informe-s9.pdf'
SimpleDocTemplate(str(out),pagesize=(595.28,841.89),rightMargin=42,leftMargin=42,topMargin=38,bottomMargin=42).build(story,onFirstPage=footer,onLaterPages=footer)
deliver=root.parent/'output'/'pdf';deliver.mkdir(parents=True,exist_ok=True)
shutil.copy2(out,deliver/'Tinoco_LP2_S9_Autonoma.pdf')
print(out)
