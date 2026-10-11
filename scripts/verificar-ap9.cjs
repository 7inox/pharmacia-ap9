const fs=require('node:fs'), assert=require('node:assert/strict'),ts=require('typescript');
require('@angular/compiler');
require.extensions['.ts']=(m,f)=>m._compile(ts.transpileModule(fs.readFileSync(f,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022,experimentalDecorators:true}}).outputText,f);
const {createEnvironmentInjector,runInInjectionContext}=require('@angular/core');
const {NonNullableFormBuilder,FormBuilder}=require('@angular/forms');
const {Router}=require('@angular/router');
const {of,Subject}=require('rxjs');
const {VentaForm}=require('../src/app/features/ventas/pages/venta-form/venta-form.ts');
const {VentaList}=require('../src/app/features/ventas/pages/venta-list/venta-list.ts');
const {VentaService}=require('../src/app/features/ventas/services/venta-service.ts');
const clientes=[{id:1,nombres:'Miguel',apellidos:'Tinocó',dni:'11111111',estado:true},{id:2,nombres:'Miguel',apellidos:'Tinoco',dni:'22222222',estado:false}];
const productos=[{id:1,nombre:'Producto uno',categoriaNombre:'Botica',precio:18.9,stock:8,estado:true},{id:2,nombre:'Producto dos',categoriaNombre:'Botica',precio:0.1,stock:3,estado:true}];
let post,envios,busquedas,nav;
function crear(T=VentaForm){post=new Subject();envios=[];busquedas=[];nav=[];const servicio={catalogo:t=>of(t==='clientes'?clientes:productos),registrar:b=>{envios.push(b);return post},buscar:(f,p,t)=>{busquedas.push({f,p,t});return of({contenido:[{estado:'REGISTRADA',total:0.1},{estado:'REGISTRADA',total:0.2},{estado:'ANULADA',total:90}],numeroPagina:p,totalPaginas:1,totalElementos:3})}};const i=createEnvironmentInjector([{provide:NonNullableFormBuilder,useValue:new FormBuilder().nonNullable},{provide:VentaService,useValue:servicio},{provide:Router,useValue:{navigate:(...a)=>{nav.push(a);return Promise.resolve(true)}}}]);return runInInjectionContext(i,()=>new T());}
const pruebas=[];
function test(nombre,fn){try{fn();pruebas.push({nombre,estado:'Pasa'})}catch(e){pruebas.push({nombre,estado:'Falla',mensaje:e.message})}}
test('Formulario vacío bloquea resumen',()=>{const v=crear();v.revisar();assert.equal(v.confirmando(),false)});
test('Búsqueda normaliza tildes y excluye inactivos',()=>{const v=crear();v.buscarCliente.setValue('tinoco');assert.equal(v.clientesEncontrados().length,1)});
test('FormArray recalcula 18.90 x 3',()=>{const v=crear();v.agregarProducto(productos[0]);v.detalles.at(0).controls.cantidad.setValue(3);assert.equal(v.total(),56.7)});
test('Repetidos incrementan una sola línea',()=>{const v=crear();v.agregarProducto(productos[0]);v.agregarProducto(productos[0]);assert.equal(v.detalles.length,1);assert.equal(v.cantidadEnDetalle(1),2)});
test('Enter agrega y evita submit',()=>{const v=crear();v.buscarProducto.setValue('uno');let prevent=false;v.agregarPrimero({preventDefault(){prevent=true}});assert.ok(prevent);assert.equal(v.detalles.length,1);assert.equal(v.confirmando(),false)});
test('Cantidades inválidas y stock bloquean resumen',()=>{const v=crear();v.elegirCliente(clientes[0]);v.agregarProducto(productos[0]);for(const n of [0,-1,1.5,9]){v.detalles.at(0).controls.cantidad.setValue(n);v.revisar();assert.equal(v.confirmando(),false)}});
test('Quitar recalcula total',()=>{const v=crear();productos.forEach(p=>v.agregarProducto(p));v.quitarLinea(0);assert.equal(v.total(),0.1)});
test('Doble confirmación envía un POST sin precio ni total',()=>{const v=crear();v.elegirCliente(clientes[0]);v.agregarProducto(productos[0]);v.revisar();v.confirmar();v.confirmar();assert.equal(envios.length,1);assert.deepEqual(envios[0],{clienteId:1,detalles:[{productoId:1,cantidad:1}]})});
test('409 conserva cliente y detalle',()=>{const v=crear();v.elegirCliente(clientes[0]);v.agregarProducto(productos[0]);v.revisar();v.confirmar();post.error({status:409,error:{mensaje:'Stock insuficiente'}});assert.equal(v.guardando(),false);assert.equal(v.confirmando(),false);assert.equal(v.form.controls.clienteId.value,1);assert.equal(v.detalles.length,1)});
test('Registro navega a comprobante e imprime si se selecciona',()=>{const v=crear();v.elegirCliente(clientes[0]);v.agregarProducto(productos[0]);v.imprimirAlRegistrar.set(true);v.revisar();v.confirmar();post.next({id:7});assert.deepEqual(nav[0],[['/ventas',7],{queryParams:{nueva:1,imprimir:1}}])});
test('Consulta suma céntimos y excluye anuladas',()=>{const v=crear(VentaList);assert.equal(v.totalPagina(),0.3)});
test('Rango invertido no llama al servicio',()=>{const v=crear(VentaList);const n=busquedas.length;v.filtros.patchValue({desde:'2026-10-12',hasta:'2026-10-11'});v.buscar();assert.equal(busquedas.length,n);assert.ok(v.error())});
fs.mkdirSync('docs/evidencias-ap9',{recursive:true});fs.writeFileSync('docs/evidencias-ap9/unitarias.json',JSON.stringify(pruebas,null,2));console.log(JSON.stringify({pasan:pruebas.filter(p=>p.estado==='Pasa').length,total:pruebas.length,fallas:pruebas.filter(p=>p.estado==='Falla')},null,2));if(pruebas.some(p=>p.estado==='Falla'))process.exitCode=1;
