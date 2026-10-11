# Matriz de pruebas S8 - Dependencias

Miguel Ángel Tinoco López. Ejecución: 04/10/2026, hora de Lima.

Se ejecutaron 18 casos: 14 pasan y 4 fallan. Altas: 8 casos (7 pasan, 1 falla). Cambios: 5 (2 pasan, 3 fallan). Bajas: 5 (5 pasan, 0 fallan). Los casos propios son A-07, A-08, C-05 y B-05.

Reglas elegidas: C-03 debe impedir la desactivación de una categoría con productos activos (409) para no dejar artículos vendibles sin clasificación activa; B-04 debe rechazar la eliminación si quedan productos inactivos (409) para preservar integridad e historial.

Medios: SPA Angular ejecutada en localhost:4201 y mejora final verificada en localhost:4203 (copias de la rama autónoma), conectada a la API real localhost:8080. Las peticiones directas se ejecutaron por HTTP en el navegador y se registraron; no se ejecutó Postman. La colección v2.1 se generó con las peticiones reales para importarlas y repetirlas en Postman. El código probado debe aplicarse todavía al frontend original de E:.

Los datos se prepararon en categorías exclusivas Auto S8 343626; había tres categorías activas, una inactiva y ocho productos, incluido uno de baja, antes de iniciar la matriz.

| ID | Operación | Precondición | Datos | Resultado esperado | Resultado obtenido (SPA y HTTP) | Estado | Evidencia |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A-01 | Alta válida | Categoría activa existente | nombre=AA Auto S8 343626 A01 válido; precio=5.5; stock=10; categoriaId=92 | 201 y producto con categoría visible | SPA guardó, HTTP 201; categoría visible. | Pasa | [A-01_spa.png](evidencias-s8/A-01_spa.png); [A-01_spa_network.png](evidencias-s8/A-01_spa_network.png) |
| A-02 | Alta sin categoría | Formulario nuevo; ninguna categoría elegida | categoriaId omitido | SPA no envía; API 400 | SPA sin POST; API 400 con categoriaId obligatorio. | Pasa | [A-02_http.png](evidencias-s8/A-02_http.png); [A-02_http_network.png](evidencias-s8/A-02_http_network.png); [A-02_spa.png](evidencias-s8/A-02_spa.png); [A-02_spa_network.png](evidencias-s8/A-02_spa_network.png) |
| A-03 | Alta con categoría inexistente | Categoría 999 inexistente | categoriaId=999 | 404 Categoria no encontrada | HTTP 404: Categoria no encontrada con id: 999 | Pasa | [A-03_http.png](evidencias-s8/A-03_http.png); [A-03_http_network.png](evidencias-s8/A-03_http_network.png) |
| A-04 | Alta en categoría inactiva | Categoría existente con estado=false | categoriaId=95 | SPA no ofrece; API rechaza con 409 | SPA oculta: true; API 201 creó el producto. | Falla | [A-04_http.png](evidencias-s8/A-04_http.png); [A-04_http_network.png](evidencias-s8/A-04_http_network.png); [A-04_spa.png](evidencias-s8/A-04_spa.png); [A-04_spa_network.png](evidencias-s8/A-04_spa_network.png) |
| A-05 | Alta con nombre duplicado | Existe el producto A-01 | Mismo nombre en minúsculas | 409 Ya existe un producto | SPA muestra conflicto; POST 409. | Pasa | [A-05_spa.png](evidencias-s8/A-05_spa.png); [A-05_spa_network.png](evidencias-s8/A-05_spa_network.png) |
| A-06 | Alta con precio y stock inválidos | Categoría activa | precio=0; stock=-1 | SPA bloquea; API 400 con precio y stock | SPA sin POST; API 400; validationErrors={"precio":"El precio mínimo es 0.01","stock":"El stock no puede ser negativo"} | Pasa | [A-06_http.png](evidencias-s8/A-06_http.png); [A-06_http_network.png](evidencias-s8/A-06_http_network.png); [A-06_spa.png](evidencias-s8/A-06_spa.png); [A-06_spa_network.png](evidencias-s8/A-06_spa_network.png) |
| C-01 | Cambio a categoría activa | Producto A-01 y segunda categoría activa | categoriaId=93 | 200 y nueva categoría en listado | PUT 200; listado muestra Auto S8 343626 otra | Pasa | [C-01_spa.png](evidencias-s8/C-01_spa.png); [C-01_spa_network.png](evidencias-s8/C-01_spa_network.png) |
| C-02 | Cambio a categoría inactiva | Producto existente; categoría inactiva | productoId=32; categoriaId=95 | SPA impide; API rechaza con 409 | SPA bloquea: true; API 200 guardó categoría inactiva. | Falla | [C-02_http.png](evidencias-s8/C-02_http.png); [C-02_http_network.png](evidencias-s8/C-02_http_network.png); [C-02_spa.png](evidencias-s8/C-02_spa.png); [C-02_spa_network.png](evidencias-s8/C-02_spa_network.png) |
| C-03 | Desactivar categoría con productos activos | Categoría ventas tiene producto activo | categoriaId=96; estado=false | 409; impedir desactivación para preservar productos vendibles | SPA permitió; PUT 200 dejó producto activo en categoría inactiva. | Falla | [C-03_spa.png](evidencias-s8/C-03_spa.png); [C-03_spa_network.png](evidencias-s8/C-03_spa_network.png) |
| C-04 | Alta con categoría desactivada en otra pestaña | Pestaña 1 cargó categoría X activa; pestaña 2 la desactivó | categoriaId=97; producto nuevo | API revalida y rechaza; no crea producto en categoría inactiva | Pestaña 2 desactivó; pestaña 1 envió y POST 201 creó el producto. | Falla | [C-04_pestana1.png](evidencias-s8/C-04_pestana1.png); [C-04_pestana2.png](evidencias-s8/C-04_pestana2.png); [C-04_spa.png](evidencias-s8/C-04_spa.png); [C-04_spa_network.png](evidencias-s8/C-04_spa_network.png) |
| B-01 | Baja lógica de producto activo | Producto A-01 activo | productoId=32 | 204; permanece como Inactivo | DELETE 204, GET y fila Inactivo con botón deshabilitado. | Pasa | [B-01_spa.png](evidencias-s8/B-01_spa.png); [B-01_spa_network.png](evidencias-s8/B-01_spa_network.png) |
| B-02 | Baja repetida | Producto A-01 ya inactivo | productoId=32 | 409 producto ya inactivo | HTTP 409: El producto ya está inactivo. | Pasa | [B-02_http.png](evidencias-s8/B-02_http.png); [B-02_http_network.png](evidencias-s8/B-02_http_network.png) |
| B-03 | Eliminar categoría sin productos | Categoría temporal sin productos | categoriaId=98 | 204; desaparece del listado y select | DELETE 204; categoría ausente en nuevo formulario. | Pasa | [B-03_select.png](evidencias-s8/B-03_select.png); [B-03_spa.png](evidencias-s8/B-03_spa.png); [B-03_spa_network.png](evidencias-s8/B-03_spa_network.png) |
| B-04 | Eliminar categoría con productos dados de baja | Solo un producto inactivo en categoría historial | categoriaId=99 | 409; preservar categoría para trazabilidad de reportes | DELETE 409; no elimina categoría. | Pasa | [B-04_spa.png](evidencias-s8/B-04_spa.png); [B-04_spa_network.png](evidencias-s8/B-04_spa_network.png) |
| A-07 | Alta en límites válidos | Categoría activa | precio=0.01; stock=0 | 201; ambos límites son válidos | HTTP 201; precio y stock conservados. | Pasa | [A-07_http.png](evidencias-s8/A-07_http.png); [A-07_http_network.png](evidencias-s8/A-07_http_network.png) |
| A-08 | Alta con ID de categoría negativo | Petición directa | categoriaId=-1 | 400 validationErrors.categoriaId | HTTP 400; {"categoriaId":"La categoría debe tener un identificador positivo"} | Pasa | [A-08_http.png](evidencias-s8/A-08_http.png); [A-08_http_network.png](evidencias-s8/A-08_http_network.png) |
| C-05 | Cambio a categoría inexistente | Producto existente y categoría 999 inexistente | categoriaId=999 | 404; conservar asociación anterior | HTTP 404: Categoria no encontrada con id: 999 | Pasa | [C-05_http.png](evidencias-s8/C-05_http.png); [C-05_http_network.png](evidencias-s8/C-05_http_network.png) |
| B-05 | Eliminar categoría con productos activos | Categoría otra conserva producto secundario activo | categoriaId=93 | 409; impedir pérdida de relación | DELETE 409; mensaje de productos asociados. | Pasa | [B-05_spa.png](evidencias-s8/B-05_spa.png); [B-05_spa_network.png](evidencias-s8/B-05_spa_network.png) |

## Evidencia adicional de la mejora

[Categorías y Ver productos](evidencias-s8/MEJORA_categorias.png), [Productos filtrados](evidencias-s8/MEJORA_productos.png), [Network tamaño 100](evidencias-s8/MEJORA_productos_network.png).

## Reproducción y límites

Importar postman/PharmaSoft-S8-Dependencias.json. Las altas usan nombres únicos e IDs de esta ejecución: repetirlas sin preparar datos nuevos puede producir 409 por duplicación. Cambiar nombres e IDs antes de repetir. La matriz describe esta ejecución; no una ejecución adicional en Postman. El estudiante debe reproducir los casos para poder explicarlos en clase, como exige la actividad.

Versionamiento: se preparan commits con fechas reales del 04/10/2026. Aún faltan commits en días distintos, PR hacia develop y carga al aula virtual.
