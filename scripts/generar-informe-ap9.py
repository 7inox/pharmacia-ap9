from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from xml.sax.saxutils import escape
root=Path(__file__).resolve().parents[1]
ev=root/'docs/evidencias-ap9'
out=root.parent/'output/pdf/Tinoco_LP2_S9_Practica_AP9.pdf'
out.parent.mkdir(parents=True,exist_ok=True)
styles=getSampleStyleSheet()
styles['BodyText'].fontSize=10
styles['BodyText'].leading=15
cases=[
('Formulario vacío','P01.jpg','Revisar sin cliente ni líneas.','Muestra validaciones y no abre el resumen.'),
('Búsqueda de clientes','P02-activos.jpg','Buscar tinoco sin tilde y luego un texto inexistente.','Solo aparecen los tres clientes activos; la búsqueda sin coincidencias queda vacía. Evidencia adicional: P02-vacio.jpg.'),
('Cantidad y subtotal','P03.jpg','Agregar producto de S/18.90 y cambiar cantidad a 3.','Subtotal y total reactivos: S/56.70.'),
('Agregar con Enter y quitar','P04.jpg','Agregar dos productos con Enter y quitar una línea.','Enter agrega sin registrar; al quitar producto 1 el total pasa de S/74.20 a S/61.70.'),
('Producto repetido','P05.jpg','Agregar nuevamente producto 6.','Una sola fila, cantidad 2; total S/66.70.'),
('Stock insuficiente en formulario','P06.jpg','Ingresar cantidad 28 cuando el stock disponible es 27.','Muestra error de stock y bloquea el resumen.'),
('Resumen previo','P07.jpg','Revisar una venta válida.','Resumen con cliente, dos productos y total S/66.70.'),
('Volver sin registrar','P08.jpg','Volver desde el resumen.','Conserva formulario; ventas en API antes y después: 6. Evidencia HTTP: P08-http.json.'),
('Confirmación y comprobante','P09.jpg','Confirmar la venta revisada.','Venta 7 creada y navegación a su comprobante.'),
('Total definitivo','P10.jpg','Comparar total del resumen con respuesta del servidor.','Estimado y total persistido de venta 7: S/66.70. JSON de API incluido.'),
('Impresión automática','P11.jpg','Marcar imprimir al registrar y confirmar.','Venta 8 creada con total S/0.10. Se invocó impresión; vista previa, DNI y pie impresos pendientes de inspección visual.'),
('Comprobante ANULADA','P12.jpg','Consultar venta anulada e imprimir.','Pantalla muestra ANULADA. Venta 8 preparada como fixture JDBC, con devolución de stock. Vista previa y sello impreso pendientes.'),
('Imprimir consulta','P13.jpg','Filtrar cliente, estado y fechas, y elegir imprimir consulta.','Pantalla contiene filtros aplicados y total de página S/150.70; se invocó impresión. Ocultación de acciones en vista previa pendiente. La consulta sin filtro de estado excluye ANULADA de su suma (consulta-paginada.jpg).'),
('Descuento de existencias','P14.jpg','Consultar productos después de registrar venta 7.','Producto 2: 27 a 24; producto 6: 28 a 26. Pantalla y API coinciden.'),
('Conflicto de stock en dos pestañas','P15.jpg','Preparar dos ventas del producto 49, stock 2, cantidad 2. Confirmar primero una y después otra.','Primera crea venta 9 por S/8.40. Segunda obtiene HTTP 409, conserva cliente y línea, stock actualizado a 0; no crea otra venta. Es secuencial, no una prueba de simultaneidad estricta.'),
('Filtros y paginación','P16.jpg','Consultar cliente 21, REGISTRADA, fecha 11/10/2026, página de 5.','La API devuelve página filtrada; segunda página verificada. Parámetros opcionales vacíos se omiten. Evidencias P16-http.json y paginacion-segunda.jpg.'),
('Rango de fechas invertido','P17.jpg','Desde 12/10/2026 y hasta 11/10/2026.','Validación local; no se envía búsqueda. Log de consultas permanece en 7 (P17-http.json).')
]
story=[]
def p(s,style='BodyText'):return Paragraph(escape(s),styles[style])
story += [p('LP II · Práctica S9 / AP9','Title'),Spacer(1,20),p('Miguel Ángel Tinoco López','Heading2'),p('PharmaSoft · Registro, comprobante y consulta de ventas'),p('Ejecución: 11 de octubre de 2026. Frontend Angular 22, backend Spring Boot y Oracle. Datos de prueba sintéticos.'),Spacer(1,18),p('Resultado: 14 pruebas pasan y 3 pruebas parciales de impresión.','Heading2')]
rows=[['Caso','Resultado','Caso','Resultado']]
for i in range(9):
 a=i*2+1;b=a+1
 rows.append([str(a),'Parcial' if a in [11,12,13] else 'Pasa',str(b) if b<=17 else '',('Parcial' if b in [11,12,13] else 'Pasa') if b<=17 else ''])
t=Table(rows,colWidths=[50,180,50,180]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e1edf4')),('GRID',(0,0),(-1,-1),.4,colors.lightgrey),('PADDING',(0,0),(-1,-1),7)]));story += [t,Spacer(1,16),p('Validación adicional: 12/12 pruebas automatizadas sobre formularios Angular reales y compilación AOT de plantillas correctas.'),p('Pendientes de entrega: inspeccionar las tres vistas previas de impresión y publicar la rama con PR hacia develop. No se acredita un PR que aún no existe.'),p('La paginación del backend se realiza sobre la lista filtrada en memoria. La prueba de dos pestañas verifica confirmaciones sucesivas; no garantiza atomicidad simultánea.'),p('Referencia: Guía práctica S9 del curso LP II, 29 páginas; lista de 17 pruebas en la página 26.')]
for n,(title,img,step,result) in enumerate(cases,1):
 story += [PageBreak(),p(f'{n:02d} · {title}','Title'),p('PARCIAL' if n in [11,12,13] else 'PASA','Heading2'),p('Procedimiento: '+step),Spacer(1,12),Image(str(ev/img),width=475,height=267.2),Spacer(1,16),p('Resultado observado','Heading2'),p(result),Spacer(1,14),p('La captura muestra la aplicación real en Chrome. En los casos de impresión no es una captura de la vista previa nativa. Los JSON complementarios están en docs/evidencias-ap9 del código entregado.')]
def footer(c,d):
 c.setFont('Helvetica',8);c.setFillColor(colors.grey);c.drawString(42,25,'Tinoco · LP2 · AP9 · Evidencias de prueba');c.drawRightString(A4[0]-42,25,str(d.page))
SimpleDocTemplate(str(out),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=40,bottomMargin=42).build(story,onFirstPage=footer,onLaterPages=footer)
print(out)
