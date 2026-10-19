"""Prepara vistas locales de fragmentos exactos para capturas del anexo S10."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "capturas-s10" / "vistas"
OUT.mkdir(parents=True, exist_ok=True)

VIEWS = {
    "05-conexion": (
        "Conexión backend - Oracle y puertos",
        [("backend/src/main/resources/application-dev.yaml", [(1, 12), (25, 28)])],
    ),
    "06-seguridad": (
        "Backend - reglas de acceso HTTP",
        [("backend/src/main/java/pe/edu/upeu/Practica/config/SecurityConfig.java", [(27, 47)])],
    ),
    "07-endpoints": (
        "Backend - endpoints de la actividad autónoma",
        [
            ("backend/src/main/java/pe/edu/upeu/Practica/controller/AuthController.java", [(10, 22)]),
            ("backend/src/main/java/pe/edu/upeu/Practica/controller/UsuarioController.java", [(20, 27)]),
        ],
    ),
    "08-logica": (
        "Backend - reglas de negocio B1, B2 y B3",
        [("backend/src/main/java/pe/edu/upeu/Practica/service/impl/SeguridadService.java", [(48, 56), (86, 100)])],
    ),
    "09-frontend": (
        "Frontend - token Bearer y actualización de usuarios",
        [
            ("src/app/core/auth/auth.interceptor.ts", [(7, 17)]),
            ("src/app/features/usuarios/usuarios.ts", [(53, 69)]),
        ],
    ),
    "10-json": (
        "JSON - respuestas HTTP de la verificación",
        [
            ("docs/evidencias-s10/B-01a.json", [(1, 10)]),
            ("docs/evidencias-s10/C-01.json", [(1, 12)]),
        ],
    ),
    "11-postman": (
        "JSON - colección de Postman S10",
        [("postman/PharmaSoft-S10-Seguridad.json", [(1, 17), (27, 38)])],
    ),
}

CSS = """
* { box-sizing: border-box; }
html, body { margin: 0; background: #e6edf4; color: #14253b; font-family: Segoe UI, Arial, sans-serif; }
.page { width: 1180px; min-height: 790px; padding: 22px 28px; }
h1 { font-size: 29px; margin: 0 0 7px; color: #12345c; }
.sub { font-size: 15px; color: #536578; margin-bottom: 16px; }
.panel { background: #101722; color: #e6edf3; border-radius: 12px; overflow: hidden; margin-bottom: 14px; box-shadow: 0 5px 18px #9baebe; }
.path { background: #25364d; color: #b8e4f2; font: 15px Consolas, monospace; padding: 9px 15px; overflow: hidden; white-space: nowrap; }
pre { margin: 0; padding: 12px 15px 14px; font: 17px/24px Consolas, 'Courier New', monospace; white-space: pre-wrap; overflow-wrap: anywhere; }
.num { color: #8393a7; display: inline-block; width: 40px; user-select: none; }
.gap { color: #7f8da2; }
"""

def block(path, ranges):
    lines = (ROOT / path).read_text(encoding="utf-8").splitlines()
    rendered = []
    previous_end = 0
    for start, end in ranges:
        if previous_end and start > previous_end + 1:
            rendered.append('<span class="num">...</span><span class="gap">fragmento omitido</span>')
        for number in range(start, min(end, len(lines)) + 1):
            rendered.append(f'<span class="num">{number:>3}</span>{escape(lines[number - 1])}')
        previous_end = end
    return f'<section class="panel"><div class="path">{escape(path)}</div><pre>' + "\n".join(rendered) + "</pre></section>"

for slug, (title, sources) in VIEWS.items():
    body = "".join(block(path, spans) for path, spans in sources)
    html = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{escape(title)}</title><style>{CSS}</style></head><body><main class="page"><h1>{escape(title)}</h1><div class="sub">Vista de evidencia generada de archivos locales del proyecto · fragmentos con líneas originales</div>{body}</main></body></html>'''
    target = OUT / f"{slug}.html"
    target.write_text(html, encoding="utf-8")
    print(target)
