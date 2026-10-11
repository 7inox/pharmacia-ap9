// Visor local del código AOT para verificar la SPA sin empaquetador.
// Uso: ngc -p tsconfig.app.json --rootDir src --outDir tmp/aot; node scripts/servir-aot.cjs
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const raiz = path.resolve(__dirname,'..');
const imports = {'rxjs':'/modules/rxjs/dist/esm/index.js','rxjs/operators':'/modules/rxjs/dist/esm/operators/index.js','tslib':'/modules/tslib/tslib.es6.mjs'};
for(const nombre of ['core','common','compiler','forms','platform-browser','router']) {
  const paquete=JSON.parse(fs.readFileSync(path.join(raiz,'node_modules/@angular',nombre,'package.json'),'utf8'));
  for(const [clave,valor] of Object.entries(paquete.exports)) {
    if(clave.includes('*') || !valor.default?.endsWith('.mjs'))continue;
    imports[`@angular/${nombre}${clave==='.'?'':clave.slice(1)}`]=`/modules/@angular/${nombre}/${valor.default.replace(/^\.\//,'')}`;
  }
}
const html=`<!doctype html><html lang="es"><head><meta charset="utf-8"><title>PharmaSoft S9</title><base href="/"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="stylesheet" href="/styles.css"><script type="importmap">${JSON.stringify({imports})}</script></head><body><app-root></app-root><script>console.error=(...args)=>{const p=document.createElement("pre");p.textContent=args.map(String).join(" ");document.body.append(p)};window.addEventListener("error",e=>{const p=document.createElement("pre");p.textContent=e.message;document.body.append(p)});window.addEventListener("unhandledrejection",e=>{const p=document.createElement("pre");p.textContent=String(e.reason);document.body.append(p)});</script><script type="module">import '@angular/compiler'; import '/aot/main.js';</script></body></html>`;
http.createServer((req,res)=>{
  console.log(req.url);
  const url=new URL(req.url,'http://localhost');
  let base,rel;
  if(url.pathname.startsWith('/modules/')){base=path.join(raiz,'node_modules');rel=url.pathname.slice(9);}
  else if(url.pathname.startsWith('/aot/')){base=path.join(raiz,'tmp/aot');rel=url.pathname.slice(5);}
  else if(url.pathname==='/styles.css'){base=path.join(raiz,'src');rel='styles.css';}
  else {res.setHeader('Content-Type','text/html; charset=utf-8');res.end(html);return;}
  let archivo=path.resolve(base,rel);
  if(!archivo.startsWith(path.resolve(base)+path.sep)){res.writeHead(403);res.end();return;}
  if((!fs.existsSync(archivo) || !fs.statSync(archivo).isFile()) && fs.existsSync(archivo+'.js'))archivo+='.js';
  try {res.setHeader('Content-Type',archivo.endsWith('.css')?'text/css':'text/javascript; charset=utf-8');res.end(fs.readFileSync(archivo));}
  catch{console.error('No disponible:',archivo);res.writeHead(404);res.end('Archivo no disponible');}
}).listen(Number(process.env.LP2_FRONTEND_PORT??4200),'127.0.0.1',()=>console.log('SPA AOT en http://localhost:4200'));


