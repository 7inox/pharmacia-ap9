# Matriz de seguridad S10 — PharmaSoft

Ejecución local: 2026-10-18T10:19
API: http://localhost:8081/api/v1

Los archivos `evidencias-s10/<ID>.json` contienen estado HTTP y mensaje sin tokens ni contraseñas.

| ID | Grupo | Caso | HTTP esperado | HTTP obtenido | Estado | Evidencia |
|---|---|---|---:|---:|---|---|
| A-01 | Autenticación | Login ADMIN válido | 200 | 200 | PASS | `evidencias-s10/A-01.json` |
| A-02 | Autenticación | Login VENDEDOR válido | 200 | 200 | PASS | `evidencias-s10/A-02.json` |
| A-03 | Autenticación | Contraseña incorrecta, mensaje uniforme | 401 | 401 | PASS | `evidencias-s10/A-03.json` |
| A-04 | Autenticación | Cuenta inactiva, mensaje uniforme | 401 | 401 | PASS | `evidencias-s10/A-04.json` |
| T-01 | Token | Sin token | 401 | 401 | PASS | `evidencias-s10/T-01.json` |
| T-02 | Token | Token mal formado | 401 | 401 | PASS | `evidencias-s10/T-02.json` |
| T-03 | Token | Token alterado | 401 | 401 | PASS | `evidencias-s10/T-03.json` |
| T-04 | Token | Token firmado pero expirado | 401 | 401 | PASS | `evidencias-s10/T-04.json` |
| T-05 | Token | Token válido | 200 | 200 | PASS | `evidencias-s10/T-05.json` |
| P-01 | Permisos | VENDEDOR lee catálogo | 200 | 200 | PASS | `evidencias-s10/P-01.json` |
| P-02 | Permisos | VENDEDOR no crea categoría | 403 | 403 | PASS | `evidencias-s10/P-02.json` |
| P-03 | Permisos | ALMACENERO no lee clientes | 403 | 403 | PASS | `evidencias-s10/P-03.json` |
| P-04 | Permisos | ADMIN consulta reportes | 200 | 200 | PASS | `evidencias-s10/P-04.json` |
| U-01 | Usuarios | Anónimo no lista usuarios | 401 | 401 | PASS | `evidencias-s10/U-01.json` |
| U-02 | Usuarios | VENDEDOR no lista usuarios | 403 | 403 | PASS | `evidencias-s10/U-02.json` |
| C-01 | Conexión | Categorías reales en Oracle | 200 | 200 | PASS | `evidencias-s10/C-01.json` |
| X-01 | CORS | Origen Angular permitido | 200 | 200 | PASS | `evidencias-s10/X-01.json` |
| X-02 | Validación | Rol inexistente | 404 | 404 | PASS | `evidencias-s10/X-02.json` |
| X-03 | Recurso | Usuario inexistente | 404 | 404 | PASS | `evidencias-s10/X-03.json` |
| X-04 | Autorización | ALMACENERO no consulta reportes | 403 | 403 | PASS | `evidencias-s10/X-04.json` |
| B-01 | B1 | Cambio de contraseña correcto | 204 | 204 | PASS | `evidencias-s10/B-01.json` |
| B-02 | B1 | Contraseña actual incorrecta | 409 | 409 | PASS | `evidencias-s10/B-02.json` |
| B-03 | B1 | Contraseña nueva igual a actual | 409 | 409 | PASS | `evidencias-s10/B-03.json` |
| B-08 | B2 | VENDEDOR no cambia roles | 403 | 403 | PASS | `evidencias-s10/B-08.json` |
| B-04 | B2 | ADMIN cambia roles | 200 | 200 | PASS | `evidencias-s10/B-04.json` |
| B-05 | B2 | ADMIN no se quita ADMIN | 409 | 409 | PASS | `evidencias-s10/B-05.json` |
| B-06 | B3 | ADMIN desactiva usuario | 200 | 200 | PASS | `evidencias-s10/B-06.json` |
| B-07 | B3 | Token de usuario desactivado | 401 | 401 | PASS | `evidencias-s10/B-07.json` |

**Resultado:** 28/28 casos principales correctos.

Casos complementarios: A-03a, B-01a, B-03a, B-04a, B-05a, B-06a y B-07a verifican mensajes uniformes, revocación, validación, autorización dinámica y conflictos de autoadministración.
