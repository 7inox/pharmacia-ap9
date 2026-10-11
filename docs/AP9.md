# AP9 · Práctica S9 · Miguel Ángel Tinoco López

Registro con formularios reactivos y FormArray, búsquedas normalizadas, resumen previo, comprobante y consulta paginada con filtros opcionales. El servidor recibe únicamente identificadores y cantidades; devuelve el total definitivo y descuenta existencias.

## Ejecución

Backend incluido en backend/ (proyecto Practica): Java y Maven. Configurar DB_URL, DB_USERNAME y DB_PASSWORD como variables del entorno para Oracle FREEPDB1. No se incluyen contraseñas. Ejecutar ./mvnw spring-boot:run desde backend. Puerto 8081.

Frontend (VS Code): npm install y npm start desde la raíz. Abrir http://localhost:4200/ventas. Las validaciones de esta entrega se ejecutaron en 4201 para conservar la ejecución anterior; ambos orígenes están autorizados por CORS.

Verificación: node scripts/verificar-ap9.cjs (12 pruebas usando formularios Angular reales y servicio simulado). Compilación de plantillas: node node_modules/@angular/compiler-cli/bundles/src/bin/ngc.js -p tsconfig.app.json.

## Evidencias y límites

Las 17 pruebas de la guía se documentan con capturas y resultados en el informe PDF. Catorce pasan; tres de impresión quedan parciales: se invocó window.print, pero la vista previa nativa de Chrome no fue inspeccionada. Antes de entregar, revisar impresión automática al registrar, comprobante ANULADA y consulta filtrada; comprobar ausencia del menú, DNI, pie y sello.

La venta 8 se preparó como ANULADA mediante fixture JDBC sobre datos sintéticos (scripts/PrepararVentaAnulada.java); no representa una función de anulación implementada. La prueba de stock usa dos pestañas con confirmaciones sucesivas; no demuestra seguridad ante dos transacciones estrictamente simultáneas.

La consulta pagina la lista filtrada en memoria en el backend. Para grandes volúmenes debe migrarse a Pageable en el repositorio.

Rama feature/ventas-tinoco. Cuatro o más commits reales de esta sesión. No hay PR hacia develop ni integración remota realizada; ese requisito queda pendiente de subir la rama y revisar el flujo del repositorio.

## Subir desde esta carpeta

git remote set-url origin https://github.com/7inox/pharma-s9-tinoco.git
git push -u origin feature/ventas-tinoco

Si el docente exige PR a develop, crear/revisar primero esa rama de integración en GitHub y abrir el PR con base develop y compare feature/ventas-tinoco. No usar main como sustituto sin indicación del docente.
