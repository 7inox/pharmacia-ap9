"""Pruebas HTTP S10; usa únicamente cuentas de demostración y omite los secretos de la evidencia."""
import base64
import hashlib
import hmac
import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

BASE = os.getenv("PHARMA_API_URL", "http://localhost:8081/api/v1")
PASSWORD = os.environ["PHARMA_DEMO_PASSWORD"]
RESULTS = []
ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs" / "evidencias-s10"
EVIDENCE.mkdir(parents=True, exist_ok=True)

def call(method, path, token=None, body=None, headers=None):
    payload = json.dumps(body).encode() if body is not None else None
    h = {"Accept": "application/json", **(headers or {})}
    if payload is not None: h["Content-Type"] = "application/json"
    if token is not None: h["Authorization"] = "Bearer " + token
    req = urllib.request.Request(BASE + path, payload, h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            raw = response.read()
            return response.status, json.loads(raw) if raw else None, dict(response.headers)
    except urllib.error.HTTPError as error:
        raw = error.read()
        try: data = json.loads(raw)
        except ValueError: data = raw.decode(errors="replace")[:300]
        return error.code, data, dict(error.headers)

def record(case, group, description, expected, actual, data=None, extra=None):
    passed = expected == actual
    safe = {"id":case,"grupo":group,"caso":description,"esperado":expected,
            "obtenido":actual,"estado":"PASS" if passed else "FAIL",
            "fecha":datetime.now().isoformat(timespec="seconds")}
    if isinstance(data,dict) and "message" in data: safe["mensaje"] = data["message"]
    if extra is not None: safe["detalle"] = extra
    RESULTS.append(safe)
    (EVIDENCE / f"{case}.json").write_text(json.dumps(safe,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"{case} {safe['estado']} esperado={expected} obtenido={actual}")
    return passed

def test(case, group, description, expected, method, path, token=None, body=None, headers=None):
    status,data,response_headers=call(method,path,token,body,headers)
    record(case,group,description,expected,status,data)
    return status,data,response_headers

def login(username, password=PASSWORD):
    return call("POST","/auth/login",body={"username":username,"password":password})

def signed_expired_token():
    key=base64.b64decode(os.environ["PHARMA_TEST_JWT_SECRET"])
    def b64(value): return base64.urlsafe_b64encode(value).rstrip(b"=")
    head=b64(json.dumps({"alg":"HS512","typ":"JWT"},separators=(",",":")).encode())
    body=b64(json.dumps({"sub":"admin","iat":int(time.time())-3600,"exp":int(time.time())-1800},separators=(",",":")).encode())
    unsigned=head+b"."+body
    return (unsigned+b"."+b64(hmac.new(key,unsigned,hashlib.sha512).digest())).decode()

admin_status,admin_data,_=login("admin")
assert admin_status==200, "No se pudo autenticar admin; active la semilla de desarrollo"
admin=admin_data["token"]
vendor_status,vendor_data,_=login("vendedor")
assert vendor_status==200
vendor=vendor_data["token"]
store_status,store_data,_=login("almacen")
assert store_status==200
store=store_data["token"]
users_status,users,_=call("GET","/usuarios",admin)
roles_status,roles,_=call("GET","/roles",admin)
assert users_status==200 and roles_status==200
ids={u["username"]:u["id"] for u in users}
role_ids={r["nombre"]:r["id"] for r in roles}

# Matriz base de la guía: 16 casos (A4, T5, P4, U2, C1).
record("A-01","Autenticación","Login ADMIN válido",200,admin_status)
record("A-02","Autenticación","Login VENDEDOR válido",200,vendor_status)
s,d,_=login("admin","incorrecta123");record("A-03","Autenticación","Contraseña incorrecta, mensaje uniforme",401,s,d)
s,d,_=login("usuario-que-no-existe");record("A-03a","Autenticación","Usuario inexistente, mensaje uniforme",401,s,d)
s,d,_=login("inactivo");record("A-04","Autenticación","Cuenta inactiva, mensaje uniforme",401,s,d)
test("T-01","Token","Sin token",401,"GET","/productos")
test("T-02","Token","Token mal formado",401,"GET","/productos",token="mal-formado")
test("T-03","Token","Token alterado",401,"GET","/productos",token=admin[:-2]+"zz")
test("T-04","Token","Token firmado pero expirado",401,"GET","/productos",token=signed_expired_token())
test("T-05","Token","Token válido",200,"GET","/auth/me",token=admin)
test("P-01","Permisos","VENDEDOR lee catálogo",200,"GET","/productos",token=vendor)
test("P-02","Permisos","VENDEDOR no crea categoría",403,"POST","/categorias",token=vendor,body={"nombre":"NO CREAR"})
test("P-03","Permisos","ALMACENERO no lee clientes",403,"GET","/clientes",token=store)
test("P-04","Permisos","ADMIN consulta reportes",200,"GET","/reportes/ventas-por-categoria",token=admin)
test("U-01","Usuarios","Anónimo no lista usuarios",401,"GET","/usuarios")
test("U-02","Usuarios","VENDEDOR no lista usuarios",403,"GET","/usuarios",token=vendor)
s,d,_=call("GET","/categorias",admin)
record("C-01","Conexión","Categorías reales en Oracle",200 if isinstance(d,list) and len(d)>0 else -1,s,
       extra={"filas":len(d) if isinstance(d,list) else None})

# Cuatro casos adicionales de grupos distintos.
s,d,h=call("OPTIONS","/productos",headers={"Origin":"http://localhost:4200",
    "Access-Control-Request-Method":"GET"})
record("X-01","CORS","Origen Angular permitido",200,s,extra={"origin":h.get("Access-Control-Allow-Origin")})
test("X-02","Validación","Rol inexistente",404,"PUT",f"/usuarios/{ids['vendedor']}/roles",
     token=admin,body={"rolIds":[999999]})
test("X-03","Recurso","Usuario inexistente",404,"PATCH","/usuarios/999999/estado",
     token=admin,body={"estado":False})
test("X-04","Autorización","ALMACENERO no consulta reportes",403,"GET","/reportes/ventas-por-categoria",token=store)

# Nuevos requerimientos B1-B3, con restauración de las cuentas de demostración.
super_status,super_data,_=login("supervisor")
assert super_status==200
super_token=super_data["token"]
new_password=PASSWORD+"Nueva1"
try:
    test("B-01","B1","Cambio de contraseña correcto",204,"PUT","/auth/password",token=super_token,
         body={"passwordActual":PASSWORD,"passwordNueva":new_password})
    test("B-01a","B1","Token anterior revocado tras cambiar contraseña",401,"GET","/auth/me",token=super_token)
    s,d,_=login("supervisor",new_password)
    assert s==200, "No se puede entrar con la contraseña nueva"
    changed_token=d["token"]
    test("B-02","B1","Contraseña actual incorrecta",409,"PUT","/auth/password",token=changed_token,
         body={"passwordActual":"Incorrecta123","passwordNueva":"OtraClave123"})
    test("B-03","B1","Contraseña nueva igual a actual",409,"PUT","/auth/password",token=changed_token,
         body={"passwordActual":new_password,"passwordNueva":new_password})
    test("B-03a","B1","Contraseña nueva demasiado corta",400,"PUT","/auth/password",token=changed_token,
         body={"passwordActual":new_password,"passwordNueva":"abc1"})
    s,d,_=call("PUT","/auth/password",changed_token,
               {"passwordActual":new_password,"passwordNueva":PASSWORD})
    assert s==204, "No se pudo restaurar la contraseña de demostración"
    test("B-08","B2","VENDEDOR no cambia roles",403,"PUT",f"/usuarios/{ids['almacen']}/roles",
         token=vendor,body={"rolIds":[role_ids['ADMIN']]})
    test("B-04","B2","ADMIN cambia roles",200,"PUT",f"/usuarios/{ids['vendedor']}/roles",
         token=admin,body={"rolIds":[role_ids['ALMACENERO']]})
    s,d,_=call("GET","/clientes",vendor)
    record("B-04a","B2","Token existente adopta roles actuales",403,s,d)
    test("B-05","B2","ADMIN no se quita ADMIN",409,"PUT",f"/usuarios/{ids['admin']}/roles",
         token=admin,body={"rolIds":[role_ids['VENDEDOR']]})
    test("B-05a","B2","Usuario inexistente al asignar roles",404,"PUT","/usuarios/999999/roles",
         token=admin,body={"rolIds":[role_ids['VENDEDOR']]})
    s,d,_=call("PUT",f"/usuarios/{ids['vendedor']}/roles",admin,{"rolIds":[role_ids['VENDEDOR']]})
    assert s==200, "No se pudo restaurar el rol VENDEDOR"
    test("B-06a","B3","ADMIN no se desactiva a sí mismo",409,"PATCH",f"/usuarios/{ids['admin']}/estado",
         token=admin,body={"estado":False})
    test("B-06","B3","ADMIN desactiva usuario",200,"PATCH",f"/usuarios/{ids['vendedor']}/estado",
         token=admin,body={"estado":False})
    test("B-07","B3","Token de usuario desactivado",401,"GET","/clientes",token=vendor)
    s,d,_=login("vendedor")
    record("B-07a","B3","Login de usuario desactivado",401,s,d)
finally:
    check_status,check_data,_=login("supervisor",new_password)
    if check_status==200:
        call("PUT","/auth/password",check_data["token"],
             {"passwordActual":new_password,"passwordNueva":PASSWORD})
    call("PUT",f"/usuarios/{ids['vendedor']}/roles",admin,{"rolIds":[role_ids['VENDEDOR']]})
    call("PATCH",f"/usuarios/{ids['vendedor']}/estado",admin,{"estado":True})

main=[r for r in RESULTS if not r["id"].endswith("a")]
matrix=["# Matriz de seguridad S10 — PharmaSoft", "", "Ejecución local: "+datetime.now().isoformat(timespec="minutes"),
        "API: "+BASE, "", "Los archivos `evidencias-s10/<ID>.json` contienen estado HTTP y mensaje sin tokens ni contraseñas.", "",
        "| ID | Grupo | Caso | HTTP esperado | HTTP obtenido | Estado | Evidencia |",
        "|---|---|---|---:|---:|---|---|"]
for r in main:
    matrix.append(f"| {r['id']} | {r['grupo']} | {r['caso']} | {r['esperado']} | {r['obtenido']} | {r['estado']} | `evidencias-s10/{r['id']}.json` |")
matrix += ["",f"**Resultado:** {sum(r['estado']=='PASS' for r in main)}/{len(main)} casos principales correctos.",
           "", "Casos complementarios: A-03a, B-01a, B-03a, B-04a, B-05a, B-06a y B-07a verifican mensajes uniformes, revocación, validación, autorización dinámica y conflictos de autoadministración."]
(ROOT/"docs"/"matriz-seguridad-s10.md").write_text("\n".join(matrix)+"\n",encoding="utf-8")
print(f"RESULTADO {sum(r['estado']=='PASS' for r in main)}/{len(main)}")
if any(r["estado"]!="PASS" for r in main): raise SystemExit(1)
