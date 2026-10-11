$ErrorActionPreference='Stop'
$taskDatos=Get-Content docs/evidencias/datos-s9.json -Raw | ConvertFrom-Json
$taskBase='http://localhost:8080/api/v1'
function Prueba($id,$metodo,$ruta,$cuerpo) {
  $taskArgs=@{Uri="$taskBase/$ruta";Method=$metodo;SkipHttpErrorCheck=$true}
  if($null -ne $cuerpo){$taskArgs.ContentType='application/json';$taskArgs.Body=($cuerpo|ConvertTo-Json -Depth 10 -Compress)}
  $taskRespuesta=Invoke-WebRequest @taskArgs
  @{id=$id;metodo=$metodo;ruta=$ruta;solicitud=$cuerpo;http=[int]$taskRespuesta.StatusCode;respuesta=($taskRespuesta.Content|ConvertFrom-Json)} | ConvertTo-Json -Depth 20 | Set-Content "docs/evidencias/${id}_http.json" -Encoding utf8
  Write-Output "$id HTTP $($taskRespuesta.StatusCode)"
}
Prueba 'C-04' Get 'ventas/1' $null
Prueba 'V-05' Post 'ventas' @{clienteId=$taskDatos.clientes[0].id;detalles=@(@{productoId=$taskDatos.productos[6].id;cantidad=1},@{productoId=$taskDatos.productos[6].id;cantidad=1})}
Prueba 'M-02' Post 'ventas' @{clienteId=$taskDatos.clientes[3].id;detalles=@(@{productoId=$taskDatos.productos[0].id;cantidad=1})}
Prueba 'V-06' Post 'ventas' @{clienteId=$taskDatos.clientes[0].id;detalles=@(@{productoId=$taskDatos.productos[0].id;cantidad=-1})}
Prueba 'V-02' Post 'ventas' @{clienteId=$taskDatos.clientes[0].id;detalles=@(@{productoId=$taskDatos.productos[0].id;cantidad=2.5})}
Prueba 'R-01' Get 'reportes/ventas-por-categoria' $null
