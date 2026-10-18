export interface MenuItem {
    etiqueta: string;
    ruta: string;
    icono: string;
}
export const MENU: MenuItem[] = [{ etiqueta: 'Ventas', ruta: '/ventas', icono: '🛒' }, { etiqueta: 'Reportes', ruta: '/reportes/ventas-por-categoria', icono: '📊' }, { etiqueta: 'Productos', ruta: '/productos', icono: '▣' }, { etiqueta: 'Clientes', ruta: '/clientes', icono: '👥' }, { etiqueta: 'Inicio', ruta: '/inicio', icono: '⌂' }, { etiqueta: 'Categorías', ruta: '/categorias', icono: '▦' }, { etiqueta: 'Usuarios', ruta: '/usuarios', icono: '⚙' }, { etiqueta: 'Mi cuenta', ruta: '/cuenta', icono: '♙' }];
