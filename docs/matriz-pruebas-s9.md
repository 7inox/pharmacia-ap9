# Matriz de pruebas S9

Ejecución: 11/10/2026. Frontend pharma-frontend y backend Practica con Oracle local. Datos sintéticos. 17 casos base y 4 propios: B-03, C-05, V-06, F-03.

18 pasan, 2 fallan y 1 queda parcial. Las respuestas HTTP JSON son capturas reales mediante PowerShell, no capturas de Network. Los 15 tests de lógica usan HTTP simulado. I-01 no se cuenta como aprobado.

| ID | Grupo | Precondición y datos | Esperado | Obtenido | Estado | Evidencia |
|---|---|---|---|---|---|---|
| B-01 | Buscadores | Clientes 21-24; apellido Tinocó; 24 inactivo | Buscar tinoco encuentra activos; DNI inactivo excluido | 3 activos; inactivo no aparece | Pasa | B-01_activo.jpg; B-01_inactivo.jpg |
| B-02 | Buscadores | Categoría S9 Tinoco 11oct; Enter | Agrega primero y muestra precio/stock; sin resumen | Una línea sin confirmar | Pasa | B-02_spa.jpg |
| C-01 | Cálculos | 12.50 x 3 | 37.50 | 37.50 | Pasa | C-01_spa.jpg |
| C-02 | Cálculos | 18.90 x 3 | 56.70 | 56.70 | Pasa | C-02_spa.jpg |
| C-03 | Cálculos | 18.90x3,12.50x3,5x2; quitar línea central | 56.70+37.50+10=104.20; después 66.70 | 104.20 -> 66.70 | Pasa | C-03_antes.jpg; C-03_spa.jpg |
| C-04 | Cálculos | Registrar C-03; venta 1 | Servidor calcula 66.70 con 2 líneas | GET 200; total 66.70 | Pasa | C-04_spa.jpg; C-04_http.json |
| V-01 | Validaciones | Sin cliente ni líneas | Errores; no abrir resumen | Validación impide continuar | Pasa | V-01_spa.jpg |
| V-02 | Validaciones | Cantidad 0 y 2.5; API producto41 | Rechazo local y API; entero positivo | SPA rechaza; API 201 transforma 2.5 en 2 | Falla | V-02_cero.jpg; V-02_spa.jpg; V-02_http.json; V-02_postman.jpg |
| V-03 | Validaciones | Producto43: stock2, cantidad3 | Aviso supera stock | Aviso visible | Pasa | V-03_spa.jpg |
| V-04 | Validaciones | Agregar mismo producto dos veces | Una línea, cantidad2 | Una línea, cantidad2 | Pasa | V-04_spa.jpg |
| V-05 | Validaciones | POST producto47 repetido dos líneas | Regla propuesta: rechazar antes de descontar | 201; venta2 admite dos líneas; total14 | Falla | V-05_http.json; V-05_postman.jpg |
| F-01 | Confirmación | Revisar y Volver antes del registro | Cierra; no POST | Formulario preservado; simulación verifica no POST | Pasa | F-01_spa.jpg; ../verificacion-automatizada-s9.json |
| F-02 | Confirmación | Doble clic Confirmar | Una venta; bloquear botón durante petición | Una venta creada: id1 | Pasa | F-02_spa.jpg; C-04_http.json |
| M-01 | Mensajes | Dos pestañas; producto43 stock2; ambas qty2 | Primera201; segunda409; corregible | Venta4; segunda409, conserva líneas y actualiza stock0 | Pasa | M-01_spa.jpg; M-01_ventas.json |
| M-02 | Mensajes | POST cliente24 inactivo | 409; mensaje explicativo | 409 cliente inactivo | Pasa | M-02_http.json; M-02_postman.jpg |
| I-01 | Impresión | Intentar venta registrada, anulada y consulta | Guardar 3 PDF; formato y sello verificables | Botón invoca impresión; sin endpoint de anulación ni venta anulada; no se guardaron 3 PDF | Parcial | src/app/features/ventas/ventas.ts; ventas.css |
| X-01 | Consistencia | Venta1; productos42 y46 | Stock30->27 y30->28; total66.70; 2 ítems | Consulta y stock coinciden | Pasa | X-01_spa.jpg; C-04_http.json |
| B-03 | Buscadores | Texto sin coincidencias; Enter | Mensaje vacío; no agrega | Sin línea agregada | Pasa | B-03_spa.jpg |
| C-05 | Cálculos | 0.10x3 + 0.20x1 | 0.30+0.20=0.50 | 0.50 | Pasa | C-05_spa.jpg |
| V-06 | Validaciones | Cantidad -1 local y API | Rechazo local y HTTP400 | Aviso local y400 | Pasa | V-06_spa.jpg; V-06_http.json |
| F-03 | Confirmación | Volver; cambiar qty3->4 del producto0.10 | Resumen0.50->0.60; volver no POST | Resumen0.60 | Pasa | F-03_spa.jpg |

Evidencias en docs/evidencias salvo ruta indicada. Reporte histórico verificado: 11 unidades y S/125.70 (ventas1-4); rango invertido bloqueado; fechas futuras vacío. Backend unidadesVendidas adaptado a cantidadVendida. R-01_http.json fue tomado antes de venta4: 9 unidades/S/105.70. Capturas R-01_spa.jpg, R-02_spa.jpg, R-03_spa.jpg.
