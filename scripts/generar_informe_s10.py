"""Genera el informe de seguridad S10 a partir de la matriz HTTP comprobada."""
import json
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.utils import ImageReader

root=Path(__file__).resolve().parents[1]
evidence=root/"docs"/"evidencias-s10"
ids=["A-01","A-02","A-03","A-04","T-01","T-02","T-03","T-04","T-05",
     "P-01","P-02","P-03","P-04","U-01","U-02","C-01","X-01","X-02","X-03","X-04",
     "B-01","B-02","B-03","B-04","B-05","B-06","B-07","B-08"]
results=[json.loads((evidence/f"{case}.json").read_text(encoding="utf-8")) for case in ids]
assert len(results)==28 and all(r["estado"]=="PASS" for r in results)
assert all((evidence/f"{case}.json").exists() for case in ["A-03a","B-01a","B-03a","B-04a","B-05a","B-06a","B-07a"])
out=root/"docs"/"informe-s10.pdf"

blue=colors.HexColor("#13345F"); cyan=colors.HexColor("#178AA0"); pale=colors.HexColor("#EAF3F7")
grey=colors.HexColor("#526477")
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleS10",parent=styles["Title"],fontName="Helvetica-Bold",fontSize=19,leading=23,
                          textColor=blue,spaceAfter=10,alignment=TA_LEFT))
styles.add(ParagraphStyle(name="HeadS10",parent=styles["Heading2"],fontSize=11,leading=14,textColor=blue,spaceBefore=10,spaceAfter=6))
styles.add(ParagraphStyle(name="BodyS10",parent=styles["BodyText"],fontSize=9,leading=13,spaceAfter=6))
styles.add(ParagraphStyle(name="SmallS10",parent=styles["BodyText"],fontSize=8,leading=11,spaceAfter=4,textColor=grey))
styles.add(ParagraphStyle(name="CellS10",parent=styles["BodyText"],fontSize=8,leading=10))
styles.add(ParagraphStyle(name="WhiteS10",parent=styles["BodyText"],fontName="Helvetica-Bold",fontSize=8,leading=10,textColor=colors.white))
P=lambda text,style="BodyS10":Paragraph(text,styles[style])

def table(rows,widths,header=True):
    t=Table([[P(str(c),"WhiteS10" if header and i==0 else "CellS10") for c in row]
             for i,row in enumerate(rows)],colWidths=widths,repeatRows=1 if header else 0,hAlign="LEFT")
    commands=[("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),7),
              ("RIGHTPADDING",(0,0),(-1,-1),7),("TOPPADDING",(0,0),(-1,-1),6),
              ("BOTTOMPADDING",(0,0),(-1,-1),6),("GRID",(0,0),(-1,-1),.35,colors.HexColor("#D9E4EC"))]
    if header:commands += [("BACKGROUND",(0,0),(-1,0),blue),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,pale])]
    t.setStyle(TableStyle(commands));return t

doc=SimpleDocTemplate(str(out),pagesize=(21*cm,29.7*cm),leftMargin=1.8*cm,rightMargin=1.8*cm,
                      topMargin=1.6*cm,bottomMargin=1.7*cm,title="Informe de seguridad S10 - PharmaSoft",
                      author="Miguel Angel Tinoco")
story=[]
story += [P("PharmaSoft | Informe de seguridad S10","TitleS10"),
          P("Lenguaje de Programación II · Unidad 2 · Sesión 4 · 18 de octubre de 2026","SmallS10"),
          P("1. Objetivo y alcance","HeadS10"),
          P("Se corrigió la conexión Oracle del proyecto AP9 y se implementó la actividad autónoma S10: autenticación JWT, permisos por rol, cambio de contraseña, asignación de roles y activación/desactivación de usuarios. También se integraron las pantallas Angular para usar estas funciones."),
          P("2. Entorno verificado","HeadS10"),
          table([["Componente","Configuración observada"],
                 ["Oracle","Oracle Free 23.26.1, contenedor oracle-local, host 1522 hacia contenedor 1521, servicio FREEPDB1, esquema SYSVENTAS."],
                 ["Backend","Spring Boot 4, Java 24, API en http://localhost:8081/api/v1."],
                 ["Frontend","Angular 22, http://localhost:4200; login, catálogo y pantalla de usuarios comprobados en Chrome."],
                 ["Datos","69 categorías visibles desde la SPA; 5 cuentas de prueba de seguridad en desarrollo."]],
                [3.1*cm,14.1*cm]),
          P("3. Método y resultados","HeadS10"),
          P("Se ejecutaron 28 casos principales sobre HTTP real (16 base, 4 propios y 8 B1-B3), más 7 verificaciones complementarias. Se comparó el estado obtenido con el esperado y se guardó un JSON por ID sin tokens ni contraseñas. Las cuentas modificadas durante las pruebas fueron restauradas."),
          table([["Grupo","Casos","Resultado"],
                 ["Autenticación A","4","4 correctos"],["Token T","5","5 correctos"],
                 ["Permisos P","4","4 correctos"],["Usuarios U","2","2 correctos"],
                 ["Conexión C","1","1 correcto"],["Propios X","4","4 correctos"],
                 ["Requerimientos B","8","8 correctos"],["Total","28","28/28 correctos"]],
                [6.2*cm,3*cm,8*cm]),
          P("Evidencia principal: docs/matriz-seguridad-s10.md y docs/evidencias-s10/&lt;ID&gt;.json. El archivo Postman se entrega sin credenciales ni JWT reales.","SmallS10"),
          PageBreak()]

story += [P("Hallazgos y correcciones","TitleS10"),
          P("4. Fichas de hallazgos","HeadS10"),
          table([["ID / severidad","Evidencia y causa","Corrección / estado"],
                 ["H-01 / Alta", "El perfil dev apuntaba a localhost:1521, mientras Oracle del proyecto expone el contenedor por 1522. Ese puerto corresponde a otra instancia local.",
                  "URL dev cambiada a jdbc:oracle:thin:@localhost:1522/FREEPDB1. Hikari conectó a SYSVENTAS y C-01 devolvió categorías. Resuelto."],
                 ["H-02 / Media", "Un JWT emitido antes de cambiar la contraseña podía seguir vigente hasta expirar si solo se verificaba firma y fecha.",
                  "El token lleva una huella del hash BCrypt; el filtro la compara con la credencial actual. B-01a obtuvo 401 con el token anterior. Resuelto."],
                 ["H-03 / Baja", "El origen 127.0.0.1:4200 no estaba en la lista CORS inicial; el servidor Angular también puede iniciarse con ese host.",
                  "Se añadieron localhost y 127.0.0.1 para los puertos de desarrollo 4200/4201. Los orígenes de producción son configurables. Resuelto."]],
                [2.8*cm,7.4*cm,7*cm]),
          P("No quedan casos fallidos en la matriz ejecutada. El estado PASS demuestra los escenarios listados, no una auditoría exhaustiva de producción.","SmallS10"),
          P("5. Diseño de los requerimientos nuevos","HeadS10"),
          table([["Requisito","Implementación","Evidencia"],
                 ["B1: PUT /auth/password","Usuario autenticado, validación 8-72 con letra y número, BCrypt, 204; 409 si la contraseña actual falla o se repite la nueva. El token previo queda revocado.","B-01, B-02, B-03, B-01a, B-03a"],
                 ["B2: PUT /usuarios/{id}/roles","ADMIN, conjunto de roles válido, 404 para ID inexistente, 409 si ADMIN se quita su propio rol; permisos recargados de BD por petición.","B-04, B-05, B-08, B-04a, B-05a"],
                 ["B3: PATCH /usuarios/{id}/estado","ADMIN, 404 si no existe, 409 si intenta desactivarse a sí mismo; token previo de usuario inactivo obtiene 401.","B-06, B-07, B-06a, B-07a"]],
                [3.6*cm,9.4*cm,4.2*cm]),
          P("6. Revisión de frontend","HeadS10"),
          P("La SPA usa inicio de sesión, interceptor Bearer, cierre de sesión ante 401, guardas de rutas y menú según permisos. Hay vistas para cambiar la contraseña y administrar roles/estado. El backend mantiene la autorización efectiva; ocultar enlaces en Angular solo mejora la navegación."),
          PageBreak()]

story += [P("Análisis y reproducción","TitleS10"),
          P("7. Preguntas de análisis de la guía","HeadS10"),
          P("<b>¿El login revela si falló el usuario o la contraseña?</b> No. Credenciales erradas y cuenta deshabilitada responden 401 con mensaje uniforme: \"Usuario o contraseña incorrectos\" (A-03 y A-04)."),
          P("<b>¿Qué ocurre con un token anterior tras cambiar contraseña?</b> El filtro verifica la huella de la contraseña almacenada en cada petición. Al cambiar el hash BCrypt, el token anterior devuelve 401 (B-01a); es necesario volver a iniciar sesión."),
          P("<b>¿Qué pasa si se filtra la clave JWT?</b> Quien la posea podría firmar tokens válidos. Debe rotarse JWT_SECRET desde un gestor de secretos o variable de entorno, reiniciar la API para invalidar firmas previas, revisar accesos y emitir nuevas sesiones. La clave y los tokens no se guardan en Git ni en Postman."),
          P("<b>¿Basta proteger una URL o conviene proteger métodos?</b> Las reglas por URL controlan el tráfico HTTP. La comprobación en métodos protege la operación si cambia el mapeo o se invoca desde otro controlador. El proyecto usa reglas por ruta y @PreAuthorize para reportes; las operaciones de usuarios están restringidas por URL. Conviene extender anotaciones de método a todo servicio crítico en una fase de endurecimiento."),
          P("8. Cómo reproducir","HeadS10"),
          P("1. Iniciar oracle-local y comprobar el mapeo 1522:1521. Configurar DB_USERNAME, DB_PASSWORD y JWT_SECRET (Base64 de al menos 32 bytes)."),
          P("2. En desarrollo, habilitar APP_SEED_DEMO_SECURITY=true y fijar PHARMA_DEMO_PASSWORD con una clave de prueba propia. Desde backend, ejecutar .\\mvnw.cmd spring-boot:run."),
          P("3. En la raíz, ejecutar npm ci y npm start. Abrir http://localhost:4200, iniciar sesión y revisar Catálogo, Usuarios y Mi cuenta."),
          P("4. Ejecutar scripts/verify_s10.py con PHARMA_DEMO_PASSWORD definido. Revisar la matriz y sus JSON. La colección Postman requiere completar sus variables locales y ejecutar sobre datos de demostración."),
          P("9. Límites y próximos pasos","HeadS10"),
          P("La prueba se hizo en el Oracle local del curso. El perfil dev usa Hibernate ddl-auto:update; para despliegue se recomienda una migración versionada. El cierre de sesión limpia el token del navegador, pero un JWT copiado sigue válido hasta caducar si no cambió la contraseña ni se desactivó la cuenta. No se probó una carga multiusuario ni un despliegue remoto."),
          P("La guía solicita trabajo en rama, colección, matriz e informe. Esta copia está en feature/seguridad-pruebas-tinoco. La entrega en B-Learning y el PR requieren acciones separadas; este informe registra solo el trabajo local verificado.","SmallS10"),
          P("Las páginas siguientes forman un anexo visual: capturas de la aplicación en Chrome y vistas de fragmentos exactos de los archivos locales. Los JSON muestran respuestas guardadas de las pruebas HTTP; la imagen de Postman muestra la colección, no una ejecución adicional.","SmallS10")]

captures=root/"docs"/"capturas-s10"
def screenshot(name,caption,max_width=17.3*cm,max_height=18.8*cm):
    path=captures/name
    assert path.exists(), f"Falta captura: {path}"
    width,height=ImageReader(str(path)).getSize()
    ratio=min(max_width/width,max_height/height)
    img=Image(str(path),width=width*ratio,height=height*ratio)
    img.hAlign="CENTER"
    return [P(caption,"HeadS10"),img,Spacer(1,0.28*cm)]

story += [PageBreak(),P("Anexo visual | Conexión y datos","TitleS10"),
          P("Las vistas de código se generaron a partir de los archivos indicados en cada captura, con números de línea originales y fragmentos omitidos señalados. Las pantallas de la SPA se capturaron en Chrome sobre la instancia local.","SmallS10")]
story += screenshot("05-conexion.jpg","Figura 1. Configuración dev: API 8081 y Oracle en localhost:1522/FREEPDB1.",max_height=10.0*cm)
story += screenshot("02-categorias.jpg","Figura 2. Categorías cargadas en la SPA: 69 registros desde Oracle.",max_height=10.3*cm)

annex=[
    ("Seguridad del backend","06-seguridad.jpg","Figura 3. Reglas HTTP: JWT, permisos por operación, 401 y 403."),
    ("Endpoints de la actividad autónoma","07-endpoints.jpg","Figura 4. Controladores para cambio de contraseña, roles y estado."),
    ("Reglas de negocio","08-logica.jpg","Figura 5. BCrypt y protecciones para el administrador."),
    ("Integración del frontend","09-frontend.jpg","Figura 6. Interceptor Bearer, cierre ante 401 y llamadas PUT/PATCH de usuarios."),
    ("Respuestas JSON verificadas","10-json.jpg","Figura 7. B-01a devuelve 401 con token previo y C-01 confirma 69 filas Oracle."),
    ("Colección Postman","11-postman.jpg","Figura 8. Estructura JSON de la colección S10 y prueba de estado HTTP."),
]
for title,name,caption in annex:
    story += [PageBreak(),P("Anexo visual | "+title,"TitleS10")]
    story += screenshot(name,caption)
    story += [P("Fuente: archivo indicado dentro de la captura. La colección Postman usa variables locales; no se incluyen credenciales ni JWT reales.","SmallS10")]

story += [PageBreak(),P("Anexo visual | Pantallas de usuario","TitleS10")]
story += screenshot("03-usuarios.jpg","Figura 9. Administración de roles y estado de cinco cuentas de prueba.",max_height=10.7*cm)
story += screenshot("04-cuenta.jpg","Figura 10. Vista Mi cuenta para el cambio de contraseña.",max_height=10.7*cm)

def footer(canvas,document):
    canvas.saveState();w,h=document.pagesize
    canvas.setStrokeColor(colors.HexColor("#D9E4EC"));canvas.line(1.8*cm,1.25*cm,w-1.8*cm,1.25*cm)
    canvas.setFont("Helvetica",8);canvas.setFillColor(grey)
    canvas.drawString(1.8*cm,0.95*cm,"PharmaSoft · Seguridad S10 · Miguel Angel Tinoco")
    canvas.drawRightString(w-1.8*cm,0.95*cm,f"Página {document.page}")
    canvas.restoreState()

doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(out)
