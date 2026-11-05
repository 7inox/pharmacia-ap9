"""Construye el PDF de la sesión 11 a partir de capturas reales verificadas."""

from pathlib import Path
from PIL import Image
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
CAPTURES = ROOT / "docs" / "capturas-s11"
OUTPUT = ROOT / "docs" / "Tinoco_LP2_S11_Practica.pdf"
W, H = landscape(A4)
NAVY = HexColor("#11325e")
GOLD = HexColor("#e3a72b")
INK = HexColor("#233448")
MUTED = HexColor("#576879")

pdfmetrics.registerFont(TTFont("Arial", r"C:\Windows\Fonts\arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", r"C:\Windows\Fonts\arialbd.ttf"))

CASES = [
    ("01-sin-sesion.png", "Sin sesión: ruta /ventas", "La SPA envió al login con returnUrl=%2Fventas."),
    ("02-formulario-vacio.png", "Formulario vacío", "Se mostraron los dos mensajes de validación; no se envió login."),
    ("03-clave-incorrecta.png", "Contraseña incorrecta", "El backend respondió 401 y el formulario mostró el mensaje genérico."),
    ("04-inactivo.png", "Cuenta inactiva", "El backend respondió 401 con el mismo mensaje genérico."),
    ("05-vendedor-ventas.png", "Ingreso de VENDEDOR", "Volvió a /ventas; el encabezado mostró nombre, rol y vencimiento."),
    ("06-get-productos-bearer.png", "GET /productos con Bearer", "Tráfico real: POST /auth/login sin Bearer; GET /productos 200 con Bearer. Token omitido."),
    ("07-sessionstorage-verificado.png", "Sesión en sessionStorage", "Clave pharmasoft.sesion con token, expiraEn y permisos. Valor del token omitido."),
    ("08-f5-con-sesion.png", "F5 en Productos", "La página siguió autenticada después de la recarga."),
    ("09-vendedor-solo-lectura.png", "VENDEDOR sin edición", "Productos no mostró Nuevo producto ni columna Acciones."),
    ("10-vendedor-edicion-denegada.png", "VENDEDOR en /productos/nuevo", "La URL directa mostró 403 - Acceso denegado."),
    ("11-login-con-sesion.png", "Login con sesión abierta", "La ruta /login redirigió a /inicio."),
    ("12-cerrar-sesion.png", "Cerrar sesión", "Volvió al login; pharmasoft.sesion desapareció de sessionStorage."),
    ("13-almacen-ventas-denegadas.png", "ALMACENERO en /ventas", "Ventas no apareció en el menú y la URL directa mostró acceso denegado."),
    ("14-supervisor-permisos-unidos.png", "SUPERVISOR con permisos unidos", "Mostró Ventas y las acciones Nuevo producto, Editar y Dar de baja."),
    ("15-token-alterado.png", "Token modificado y F5", "La SPA cerró la sesión y mostró Su sesión expiró con retorno a /productos."),
    ("16b-expiracion-automatica.png", "Expiración automática a un minuto", "Al minuto volvió al login con aviso y returnUrl=/productos; después regresó a Productos."),
]

CODE = [
    ("codigo-01-auth-service.png", "AuthService: signal, login y sessionStorage", (35, 470, 1150, 1110)),
    ("codigo-01b-auth-expiracion.png", "AuthService: expiración y recuperación", (35, 105, 1200, 1060)),
    ("codigo-02-interceptores.png", "Interceptores de token y error", (18, 45, 950, 670)),
    ("codigo-03-guards.png", "Guards de sesión, invitado y permiso", (18, 195, 890, 630)),
    ("codigo-04-rutas.png", "Rutas protegidas", (18, 150, 1240, 650)),
    ("codigo-05-directiva.png", "Directiva estructural de permisos", (18, 140, 950, 665)),
]


def write(c, x, y, text, size=10, font="Arial", color=INK):
    c.setFont(font, size)
    c.setFillColor(color)
    c.drawString(x, y, text)


def wrap(text, width, size=10, font="Arial"):
    result, line = [], ""
    for word in text.split():
        candidate = f"{line} {word}".strip()
        if line and pdfmetrics.stringWidth(candidate, font, size) > width:
            result.append(line)
            line = word
        else:
            line = candidate
    if line:
        result.append(line)
    return result


def lines(c, x, y, text, width, size=10, leading=15, color=INK):
    for line in wrap(text, width, size):
        write(c, x, y, line, size=size, color=color)
        y -= leading
    return y


def chrome(c, section, title):
    c.setFillColor(NAVY)
    c.rect(0, H - 61, W, 61, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, H - 65, W, 4, fill=1, stroke=0)
    write(c, 34, H - 26, "PHARMASOFT  |  LP II - UNIDAD II - SESIÓN 11", 10, "Arial-Bold", white)
    write(c, 34, H - 48, f"{section}  ·  {title}", 14, "Arial-Bold", white)
    c.setStrokeColor(HexColor("#d7e0e9"))
    c.line(34, 31, W - 34, 31)
    write(c, 34, 17, "Tinoco  ·  22 de octubre de 2026  ·  evidencia de ejecución real", 8, color=MUTED)
    write(c, W - 85, 17, f"Pág. {c.getPageNumber()}", 8, color=MUTED)


def fit_image(c, img, box):
    x, y, max_w, max_h = box
    w, h = img.getSize()
    scale = min(max_w / w, max_h / h)
    dw, dh = w * scale, h * scale
    c.drawImage(img, x + (max_w - dw) / 2, y + (max_h - dh) / 2, dw, dh, mask="auto")


def photo_page(c, number, filename, title, finding, extra=None):
    path = CAPTURES / filename
    if not path.is_file():
        raise FileNotFoundError(path)
    chrome(c, f"PRUEBA {number:02d} / 16", title)
    c.setStrokeColor(HexColor("#cbd5e1"))
    c.roundRect(30, 91, W - 60, H - 174, 8, stroke=1, fill=0)
    fit_image(c, ImageReader(str(path)), (36, 97, W - 72, H - 186))
    y = lines(c, 35, 78, "Resultado: " + finding, W - 70, 10, 14)
    if extra:
        lines(c, 35, y - 2, extra, W - 70, 9, 12, MUTED)
    c.showPage()


def code_page(c, path_name, title, crop):
    path = CAPTURES / path_name
    if not path.is_file():
        raise FileNotFoundError(path)
    chrome(c, "CAPTURA DEL CÓDIGO", title)
    with Image.open(path) as source:
        x1, y1, x2, y2 = crop
        piece = source.crop((x1, y1, min(x2, source.width), min(y2, source.height)))
        image = ImageReader(piece)
        c.setStrokeColor(HexColor("#cbd5e1"))
        c.roundRect(30, 91, W - 60, H - 174, 8, stroke=1, fill=0)
        fit_image(c, image, (36, 97, W - 72, H - 186))
    lines(c, 35, 78, "Fuente: rama feature/seguridad-frontend-tinoco publicada en GitHub. Captura recortada para lectura.", W - 70, 9, 12, MUTED)
    c.showPage()


def make():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=(W, H))
    c.setTitle("Tinoco - LP2 - Sesión 11 - Actividad práctica")
    c.setAuthor("Tinoco")

    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, H - 18, W, 18, fill=1, stroke=0)
    write(c, 46, 468, "LENGUAJE DE PROGRAMACIÓN II", 16, "Arial-Bold", white)
    write(c, 46, 413, "Seguridad frontend en PharmaSoft", 29, "Arial-Bold", white)
    write(c, 46, 377, "Actividad práctica · Sesión 11 · Unidad II", 17, color=HexColor("#cadbf0"))
    c.setStrokeColor(GOLD)
    c.line(46, 349, 580, 349)
    lines(c, 46, 313, "Login, sesión con vencimiento, interceptores, guards y permisos. Evidencia de 16 pruebas con Angular, Spring Boot y Oracle SYSVENTAS.", 660, 13, 20, white)
    write(c, 46, 127, "Proyecto existente: Tinoco_LP2_AP9_Codigo / pharma-ap9", 11, color=white)
    write(c, 46, 102, "Rama: feature/seguridad-frontend-tinoco", 11, color=white)
    write(c, 46, 77, "Fecha: 22 de octubre de 2026", 11, color=white)
    c.showPage()

    chrome(c, "RESUMEN", "Resultados verificados")
    write(c, 40, H - 96, "16 / 16 casos ejecutados con backend y Oracle reales", 17, "Arial-Bold", NAVY)
    write(c, 40, H - 119, "Cinco perfiles: admin, vendedor, almacén, supervisor e inactivo.", 11)
    write(c, 40, H - 143, "Build Angular correcto · 1 prueba automatizada aprobada · backend compilado.", 11)
    short = [
        "01 Redirección", "02 Validación", "03 Clave errónea", "04 Inactivo",
        "05 Vendedor", "06 Bearer", "07 Almacenamiento", "08 F5",
        "09 Solo lectura", "10 Ruta denegada", "11 Invitado", "12 Logout",
        "13 Almacén", "14 Supervisor", "15 Token alterado", "16 Vencimiento",
    ]
    for index, label in enumerate(short):
        col, row = divmod(index, 8)
        x, y = 40 + col * 397, H - 183 - row * 43
        c.setFillColor(HexColor("#eef4fa"))
        c.roundRect(x, y - 13, 370, 32, 5, stroke=0, fill=1)
        write(c, x + 11, y - 1, label, 10, "Arial-Bold")
        write(c, x + 306, y - 1, "OK", 10, "Arial-Bold", HexColor("#176548"))
    c.showPage()

    for idx, (filename, title, finding) in enumerate(CASES, 1):
        photo_page(c, idx, filename, title, finding)

    # La prueba 16 incluye las dos pantallas adicionales de su secuencia.
    chrome(c, "PRUEBA 16 / 16", "Inicio y retorno tras el vencimiento")
    first = ImageReader(str(CAPTURES / "16a-sesion-un-minuto.png"))
    last = ImageReader(str(CAPTURES / "16c-retorno-productos.png"))
    fit_image(c, first, (34, 289, 375, 230))
    fit_image(c, last, (433, 289, 375, 230))
    write(c, 40, 265, "Antes: sesión en Productos con JWT de 1 minuto.", 10)
    write(c, 432, 265, "Después: el nuevo ingreso regresa a Productos.", 10)
    lines(c, 40, 226, "La vigencia temporal de un minuto se retiró al terminar la prueba. Las cinco contraseñas originales de demostración fueron restauradas y comprobadas.", W - 80, 11, 17)
    c.showPage()

    for path_name, title, crop in CODE:
        code_page(c, path_name, title, crop)

    chrome(c, "IMPLEMENTACIÓN", "Repositorio y comprobaciones")
    lines(c, 42, 492, "Código: https://github.com/7inox/pharmacia-ap9/tree/feature/seguridad-frontend-tinoco", W - 84, 12, 19)
    lines(c, 42, 450, "La rama incluye seis commits de seguridad frontend y datos de demostración. El login consume el campo real expiresIn del backend y almacena expiraEn en la sesión.", W - 84, 11, 17)
    lines(c, 42, 389, "Comprobaciones: npm run build, npm test -- --watch=false, compilación Maven, conexión SYSVENTAS a FREEPDB1 y las 16 pruebas de interfaz. La inspección de Red confirmó que el login no envía Bearer y GET /productos sí lo envía. Los valores de JWT y las contraseñas no aparecen en este documento.", W - 84, 11, 17)
    write(c, 42, 245, "Material de la sesión", 13, "Arial-Bold", NAVY)
    lines(c, 42, 219, "Guía práctica de la sesión 11, Facultad de Ingeniería y Arquitectura, EP Ingeniería de Sistemas, Lenguaje de Programación II.", W - 84, 11, 17)
    write(c, 42, 151, "Entrega: Tinoco_LP2_S11_Practica.pdf", 12, "Arial-Bold")
    c.showPage()
    c.save()
    print(f"PDF creado: {OUTPUT}")


if __name__ == "__main__":
    make()
