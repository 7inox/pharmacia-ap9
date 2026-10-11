$ErrorActionPreference = 'Stop'
$taskBase = 'http://localhost:8080/api/v1'
function Crear($recurso,$datos) {
  Invoke-RestMethod -Uri "$taskBase/$recurso" -Method Post -ContentType 'application/json; charset=utf-8' -Body ([Text.Encoding]::UTF8.GetBytes(($datos | ConvertTo-Json -Depth 10)))
}
$taskCategoria = Crear 'categorias' @{nombre='S9 Tinoco 11oct';descripcion='Datos exclusivos de pruebas AA9';estado=$true}
$taskClientes=@()
foreach($n in 1..4) {
  $taskClientes += Crear 'clientes' @{dni=('9910110'+$n);nombres=('Prueba S9 '+$n);apellidos='Tinocó';email="s9.$n@example.invalid";telefono='900000000';direccion='Datos académicos sintéticos';estado=($n -ne 4)}
}
$taskProductos=@()
$taskPrecios=@(12.50,18.90,10,0.10,0.20,5,7,9)
foreach($n in 1..8) {
  $taskProductos += Crear 'productos' @{nombre=('S9 Tinoco producto '+$n);precio=$taskPrecios[$n-1];stock=$(if($n -eq 3){2}else{30});estado=$true;categoriaId=$taskCategoria.id}
}
New-Item -ItemType Directory -Force docs/evidencias | Out-Null
@{categoria=$taskCategoria;clientes=$taskClientes;productos=$taskProductos} | ConvertTo-Json -Depth 20 | Set-Content docs/evidencias/datos-s9.json -Encoding utf8
Write-Output 'Datos preparados: 3 clientes activos, 1 inactivo y 8 productos.'
