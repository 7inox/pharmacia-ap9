import { Component, inject } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { MENU } from '../../core/config/menu';
import { AuthService } from '../../core/auth/auth.service';
@Component({ selector: 'app-sidebar', imports: [RouterLink, RouterLinkActive], templateUrl: './sidebar.html', styleUrl: './sidebar.css' })
export class Sidebar {
    protected readonly auth = inject(AuthService);
    protected readonly menu = MENU;
    protected canSee(route: string): boolean {
      const permission: Record<string,string> = {
        '/ventas':'VENTAS_LEER', '/reportes/ventas-por-categoria':'REPORTES_VER',
        '/productos':'CATALOGO_LEER', '/categorias':'CATALOGO_LEER', '/clientes':'CLIENTES_LEER',
        '/usuarios':'USUARIOS_ADMINISTRAR'
      };
      return !permission[route] || this.auth.has(permission[route]);
    }
}
