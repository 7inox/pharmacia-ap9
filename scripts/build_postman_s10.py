"""Genera una colección Postman S10 sin contraseñas ni tokens reales."""
import json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
items=[]
def add(group,case,name,method,path,status,token=None,body=None,pre=None,post=None,description="",extra_headers=None):
    headers=[{"key":key,"value":value} for key,value in (extra_headers or {}).items()]
    if body is not None: headers.append({"key":"Content-Type","value":"application/json"})
    if token: headers.append({"key":"Authorization","value":"Bearer {{"+token+"}}"})
    req={"method":method,"header":headers,"url":"{{baseUrl}}"+path,
         "description":description or f"{case}: HTTP esperado {status}. Ejecutar los grupos en orden."}
    if body is not None:
        raw=json.dumps(body,ensure_ascii=False)
        for key in ("storeRoleId","vendorRoleId","adminRoleId"):
            raw=raw.replace('"{{'+key+'}}"','{{'+key+'}}')
        req["body"]={"mode":"raw","raw":raw}
    scripts=[]
    if pre: scripts.append({"listen":"prerequest","script":{"type":"text/javascript","exec":pre.splitlines()}})
    checks=[f'pm.test("{case}: HTTP {status}", () => pm.response.to.have.status({status}));']
    if post: checks.extend(post.splitlines())
    scripts.append({"listen":"test","script":{"type":"text/javascript","exec":checks}})
    items.append((group,{"name":f"{case} - {name}","request":req,"event":scripts}))

login={"username":"admin","password":"{{demoPassword}}"}
add("00 - Preparación","SET-01","Login ALMACENERO","POST","/auth/login",200,
    body={"username":"almacen","password":"{{demoPassword}}"},
    post='if(pm.response.code===200) pm.collectionVariables.set("storeToken", pm.response.json().token);')
add("00 - Preparación","SET-02","Login SUPERVISOR","POST","/auth/login",200,
    body={"username":"supervisor","password":"{{demoPassword}}"},
    post='if(pm.response.code===200) pm.collectionVariables.set("superToken", pm.response.json().token);')
add("A - Autenticación","A-01","Login ADMIN", "POST","/auth/login",200,body=login,
    post='if(pm.response.code===200) pm.collectionVariables.set("adminToken", pm.response.json().token);')
add("A - Autenticación","A-02","Login VENDEDOR","POST","/auth/login",200,
    body={"username":"vendedor","password":"{{demoPassword}}"},
    post='if(pm.response.code===200) pm.collectionVariables.set("vendorToken", pm.response.json().token);')
add("A - Autenticación","A-03","Contraseña incorrecta","POST","/auth/login",401,
    body={"username":"admin","password":"equivocada123"})
add("A - Autenticación","A-04","Usuario inactivo","POST","/auth/login",401,
    body={"username":"inactivo","password":"{{demoPassword}}"})
add("00 - Preparación","SET-03","Identificadores de usuarios","GET","/usuarios",200,token="adminToken",
    post='for(const u of pm.response.json()) { if(u.username==="admin") pm.collectionVariables.set("adminId",u.id); if(u.username==="vendedor") pm.collectionVariables.set("vendorId",u.id); if(u.username==="almacen") pm.collectionVariables.set("storeId",u.id); }')
add("00 - Preparación","SET-04","Identificadores de roles","GET","/roles",200,token="adminToken",
    post='for(const r of pm.response.json()) { if(r.nombre==="ADMIN") pm.collectionVariables.set("adminRoleId",r.id); if(r.nombre==="VENDEDOR") pm.collectionVariables.set("vendorRoleId",r.id); if(r.nombre==="ALMACENERO") pm.collectionVariables.set("storeRoleId",r.id); }')
add("T - Token","T-01","Sin token","GET","/productos",401)
add("T - Token","T-02","Mal formado","GET","/productos",401,token="malformedToken")
add("T - Token","T-03","Alterado","GET","/productos",401,token="tamperedToken",
    pre='pm.collectionVariables.set("tamperedToken", pm.collectionVariables.get("adminToken").slice(0,-2)+"zz");')
add("T - Token","T-04","Expirado","GET","/productos",401,token="expiredToken",
    description="Generar un JWT firmado y expirado con la clave del entorno de pruebas; no se incluye la clave en la colección.")
add("T - Token","T-05","Válido","GET","/auth/me",200,token="adminToken")
add("P - Permisos","P-01","Vendedor lee productos","GET","/productos",200,token="vendorToken")
add("P - Permisos","P-02","Vendedor no crea categoría","POST","/categorias",403,
    token="vendorToken",body={"nombre":"NO CREAR"})
add("P - Permisos","P-03","Almacenero no lee clientes","GET","/clientes",403,token="storeToken",
    )
add("P - Permisos","P-04","Admin ve reportes","GET","/reportes/ventas-por-categoria",200,token="adminToken")
add("U - Usuarios","U-01","Anónimo no lista usuarios","GET","/usuarios",401)
add("U - Usuarios","U-02","Vendedor no lista usuarios","GET","/usuarios",403,token="vendorToken")
add("C - Conexión","C-01","Datos de categorías Oracle","GET","/categorias",200,token="adminToken",
    post='pm.test("Hay datos reales", () => pm.expect(pm.response.json().length).to.be.above(0));')
add("X - Casos propios","X-01","Preflight CORS Angular","OPTIONS","/productos",200,
    extra_headers={"Origin":"http://localhost:4200","Access-Control-Request-Method":"GET"})
add("X - Casos propios","X-02","Rol inexistente","PUT","/usuarios/{{vendorId}}/roles",404,
    token="adminToken",body={"rolIds":[999999]})
add("X - Casos propios","X-03","Usuario inexistente","PATCH","/usuarios/999999/estado",404,
    token="adminToken",body={"estado":False})
add("X - Casos propios","X-04","Almacenero no ve reportes","GET","/reportes/ventas-por-categoria",403,token="storeToken")
add("B - Nuevos requerimientos","B-01","Cambiar contraseña","PUT","/auth/password",204,
    token="superToken",body={"passwordActual":"{{demoPassword}}","passwordNueva":"{{newPassword}}"})
add("B - Nuevos requerimientos","B-01a","Token anterior revocado","GET","/auth/me",401,
    token="superToken")
add("B - Nuevos requerimientos","SET-05","Login con contraseña nueva","POST","/auth/login",200,
    body={"username":"supervisor","password":"{{newPassword}}"},
    post='if(pm.response.code===200) pm.collectionVariables.set("superToken", pm.response.json().token);')
add("B - Nuevos requerimientos","B-02","Contraseña actual errada","PUT","/auth/password",409,
    token="superToken",body={"passwordActual":"Incorrecta123","passwordNueva":"{{newPassword}}"})
add("B - Nuevos requerimientos","B-03","Nueva contraseña igual","PUT","/auth/password",409,
    token="superToken",body={"passwordActual":"{{newPassword}}","passwordNueva":"{{newPassword}}"})
add("B - Nuevos requerimientos","RESET-01","Restaurar contraseña demo","PUT","/auth/password",204,
    token="superToken",body={"passwordActual":"{{newPassword}}","passwordNueva":"{{demoPassword}}"})
add("B - Nuevos requerimientos","B-08","Vendedor no cambia roles","PUT","/usuarios/{{storeId}}/roles",403,
    token="vendorToken",body={"rolIds":["{{adminRoleId}}"]})
add("B - Nuevos requerimientos","B-04","Asignar rol","PUT","/usuarios/{{vendorId}}/roles",200,
    token="adminToken",body={"rolIds":["{{storeRoleId}}"]})
add("B - Nuevos requerimientos","B-05","Admin no pierde ADMIN","PUT","/usuarios/{{adminId}}/roles",409,
    token="adminToken",body={"rolIds":["{{vendorRoleId}}"]})
add("B - Nuevos requerimientos","RESET-02","Restaurar rol vendedor","PUT","/usuarios/{{vendorId}}/roles",200,
    token="adminToken",body={"rolIds":["{{vendorRoleId}}"]})
add("B - Nuevos requerimientos","B-06","Desactivar usuario","PATCH","/usuarios/{{vendorId}}/estado",200,
    token="adminToken",body={"estado":False})
add("B - Nuevos requerimientos","B-07","Token desactivado","GET","/clientes",401,token="vendorToken")
add("B - Nuevos requerimientos","RESET-03","Reactivar vendedor","PATCH","/usuarios/{{vendorId}}/estado",200,
    token="adminToken",body={"estado":True})

groups=[]
for name in ["A - Autenticación","00 - Preparación","T - Token","P - Permisos","U - Usuarios",
             "C - Conexión","X - Casos propios","B - Nuevos requerimientos"]:
    groups.append({"name":name,"item":[item for group,item in items if group==name]})
collection={"info":{"name":"PharmaSoft - S10 Seguridad","schema":"https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
                    "description":"28 casos de la matriz S10. Use solo un entorno local de desarrollo. Los casos B alteran usuarios demo; restaurar al final."},
            "item":groups,"variable":[{"key":key,"value":value} for key,value in {
                "baseUrl":"http://localhost:8081/api/v1","demoPassword":"","newPassword":"",
                "adminToken":"","vendorToken":"","storeToken":"","superToken":"",
                "expiredToken":"","malformedToken":"mal-formado","tamperedToken":"",
                "vendorId":"","adminId":"","storeId":"","adminRoleId":"","vendorRoleId":"","storeRoleId":""}.items()]}
out=root/"postman"/"PharmaSoft-S10-Seguridad.json"
out.write_text(json.dumps(collection,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(out)
