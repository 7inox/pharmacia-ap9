# PharmaSoft - Sesión 10

## Estado comprobado

- Oracle Free `oracle-local` está publicado en el host por **1522** y en el contenedor por **1521**. Servicio: `FREEPDB1`; esquema usado por este proyecto: `SYSVENTAS`.
- Backend: `http://localhost:8081/api/v1`. Frontend: `http://localhost:4200`.
- La ejecución local del 18/10/2026 obtuvo **28/28** casos principales correctos y 7 comprobaciones complementarias. La SPA mostró 69 categorías reales y la administración de usuarios.

## Arranque

1. Iniciar el contenedor Oracle y comprobarlo con `docker ps`.
2. Configurar **en la terminal**, sin guardar secretos en Git:

   ```powershell
   $env:DB_USERNAME = '<usuario Oracle SYSVENTAS>'
   $env:DB_PASSWORD = '<contraseña Oracle>'
   $env:JWT_SECRET = [Convert]::ToBase64String([Security.Cryptography.RandomNumberGenerator]::GetBytes(64))
   ```

3. Para generar cuentas de prueba en el perfil `dev` solamente, antes del primer inicio:

   ```powershell
   $env:APP_SEED_DEMO_SECURITY = 'true'
   $env:PHARMA_DEMO_PASSWORD = '<contraseña de prueba, 8-72 caracteres con letras y números>'
   ```

   El cargador crea ADMIN, VENDEDOR, ALMACENERO, SUPERVISOR e INACTIVO solo si faltan. No reemplaza contraseñas existentes. Después se puede apagar con `APP_SEED_DEMO_SECURITY=false`. Nunca usar el cargador en producción.

4. En `backend/`, ejecutar `.\mvnw.cmd spring-boot:run`. Verificar `http://localhost:8081/api/health`.
5. En la raíz, ejecutar `npm ci` y `npm start`. Abrir `http://localhost:4200` e iniciar sesión con una cuenta de prueba creada.

El perfil `dev` ya usa `jdbc:oracle:thin:@localhost:1522/FREEPDB1`. Si el contenedor se publica en otro puerto, fijar `DB_URL` explícitamente. El perfil `prod` necesita sus propias variables de conexión y `JWT_SECRET`; no activa las cuentas de prueba.

## Funciones nuevas

| Función | Ruta | Perfil |
|---|---|
| Login | `POST /auth/login` | Pública |
| Cambiar contraseña | `PUT /auth/password` | Usuario autenticado |
| Listar usuarios | `GET /usuarios` | ADMIN |
| Reemplazar roles | `PUT /usuarios/{id}/roles` | ADMIN |
| Activar/desactivar | `PATCH /usuarios/{id}/estado` | ADMIN |

La SPA ofrece `Mi cuenta` para la contraseña y `Usuarios` para roles y estado. Cada petición al backend valida el JWT y carga los permisos actuales de Oracle. Al cambiar la contraseña, los tokens anteriores devuelven 401. Al desactivar un usuario, su token también devuelve 401. Al cambiar roles, el token existente adopta los permisos nuevos en la petición siguiente.

## Evidencias y Postman

- `matriz-seguridad-s10.md`: 28 casos con HTTP esperado, obtenido, estado y archivo de evidencia.
- `evidencias-s10/<ID>.json`: respuestas resumidas sin JWT ni contraseñas.
- `informe-s10.pdf`: informe de tres páginas con hallazgos y respuestas de análisis.
- `../postman/PharmaSoft-S10-Seguridad.json`: colección con variables vacías. Completar `demoPassword`, `newPassword` y `expiredToken` en el entorno local; usar solo cuentas de demostración. La colección incluye peticiones de restauración tras los cambios de prueba. Para `T-04`, `expiredToken` debe ser un JWT firmado con la clave de prueba del backend y fecha de expiración pasada.

Para repetir la matriz automática, ejecutar `scripts/verify_s10.py` con `PHARMA_DEMO_PASSWORD` y `PHARMA_TEST_JWT_SECRET` (igual a `JWT_SECRET` del servidor de prueba) definidos en esa terminal. El script altera únicamente cuentas de demostración y las restaura. No usarlo con datos de producción.

## Entrega académica

El trabajo está en la rama `feature/seguridad-pruebas-tinoco`. La guía solicita PR a `master`, matriz, colección, informe y entrega en B-Learning. Un requisito de commits realizados en tres días diferentes no puede acreditarse retroactivamente con trabajo hecho el 18/10/2026. El portal mostró para la tarea autónoma un vencimiento el **18/10/2026 a las 11:59 PM**, distinto de la fecha del PDF; comprobar el portal antes de enviar. Preparar los archivos locales no equivale a subirlos ni a entregar la tarea.
