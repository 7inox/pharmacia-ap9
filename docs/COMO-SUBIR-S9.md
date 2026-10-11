# Subir AA9 / S9

## Archivos y estado

- Frontend trabajado: carpeta local `pharma-s9`, copia de `pharma-frontend`.
- Backend: `pharma-s9/backend`, copia de `Practica`; no se alteraron reglas de negocio para ocultar fallos.
- Informe: `docs/informe-s9.pdf`; copia para B-Learning: `Tinoco_LP2_S9_Autonoma.pdf`.
- Matriz: `docs/matriz-pruebas-s9.md`.
- Postman: `postman/PharmaSoft-S9-Ventas.json`; ya importado en la colección PharmaSoft - S9 Ventas.
- Evidencias: `docs/evidencias`. Datos sintéticos locales; no ejecutar de nuevo la preparación ni las ventas de prueba sin revisar stock y ventas existentes.

Resultado: 18 pasan, 2 fallan, 1 parcial. Las fallas forman parte del informe de pruebas. Para cumplir toda la guía faltan los tres PDF de I-01, la integración de práctica S9 en develop y commits de tres días diferentes. No cambiar fechas de commits ni presentar pruebas parciales como aprobadas.

## GitHub desde esta computadora

Abrir PowerShell en la carpeta `pharma-s9` creada por esta sesión. Los cambios ya están guardados en commits. Revisar:

```powershell
git status
git branch --show-current
git remote -v
git log -3 --oneline
```

La rama debe ser `feature/pruebas-reporte-ventas-tinoco` y origin debe apuntar a `https://github.com/7inox/pharma-frontend.git`. Para publicar esta rama:

```powershell
git push -u origin feature/pruebas-reporte-ventas-tinoco
```

Si Git abre Chrome, iniciar sesión en 7inox usando el flujo normal. No se necesitan códigos de los correos antiguos de GitHub; no compartir contraseñas ni tokens. No usar push --force.

En GitHub abrir pharma-frontend > Pull requests > New pull request. Elegir base `develop` y compare `feature/pruebas-reporte-ventas-tinoco`. Revisar el diff; crear inicialmente una PR borrador titulada `S9: pruebas de ventas y reporte por categoría`. Describir resultados, evidencias y pendientes del informe. Si la práctica S9 todavía no está en develop, integrar primero esa práctica y resolver el origen de esta rama antes de marcar lista la PR. No afirmar que se siguió ese flujo todavía.

## Desde el ZIP en otra carpeta

El ZIP incluye fuentes y `pharma-s9.bundle` con el historial local. Para recuperar un repositorio real, extraer el ZIP y ejecutar:

```powershell
git clone -b feature/pruebas-reporte-ventas-tinoco .\pharma-s9.bundle pharma-s9-recuperado
cd pharma-s9-recuperado
git remote set-url origin https://github.com/7inox/pharma-frontend.git
```

Después usar el push anterior. No subir node_modules, tmp, logs, credenciales ni el archivo bundle al repositorio. Las fuentes del ZIP no contienen la carpeta .git; clonar el bundle conserva el historial.

## B-Learning

Abrir LP2 > AA9. Adjuntar `Tinoco_LP2_S9_Autonoma.pdf`, añadir el enlace real de la PR cuando exista y los archivos que solicite el campo de entrega. Guardar y completar el envío según el botón visible. Verificar que la plataforma muestre entrega registrada; todavía no se ha enviado.

## Completar impresión I-01

Con frontend y Practica activos, entrar a Ventas. Imprimir una venta registrada y elegir Guardar como PDF en Chrome. Guardar también la consulta filtrada. Para la anulada hace falta completar el flujo de anulación y disponer de una venta anulada de prueba; el backend actual no expone ese endpoint. Revisar que los tres PDF oculten menús/botones y que muestren DNI, totales, filtros y sello ANULADA según corresponda. Solo entonces cambiar I-01 a Pasa y actualizar informe/matriz con los archivos reales.

## Ejecutar proyecto

Frontend normal: `npm.cmd ci` y `npm.cmd start`. Backend: Java 21 y Maven; definir DB_URL, DB_USERNAME, DB_PASSWORD como variables de entorno locales, sin guardarlas en el repositorio. Oracle de esta computadora respondió en puerto 1522/FREEPDB1. El servidor temporal AOT es una alternativa de validación de esta sesión, no reemplaza el build de producción. Verificación de lógica: `node scripts/verificar-s9.cjs`.
