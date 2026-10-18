import { HttpClient } from '@angular/common/http';
import { computed, inject, Injectable, signal } from '@angular/core';
import { Router } from '@angular/router';
import { tap } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface Session {
  token: string;
  username: string;
  nombreCompleto: string;
  roles: string[];
  permisos: string[];
  expiresAt: number;
}
interface LoginResponse extends Omit<Session, 'expiresAt'> { expiresIn: number; }
const KEY = 'pharmasoft-session';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly router = inject(Router);
  private readonly state = signal<Session | null>(this.read());
  readonly session = this.state.asReadonly();
  readonly authenticated = computed(() => this.validSession() !== null);

  login(username: string, password: string) {
    return this.http.post<LoginResponse>(`${environment.apiUrl}/auth/login`, { username, password }).pipe(
      tap(response => {
        const session: Session = {
          token: response.token, username: response.username, nombreCompleto: response.nombreCompleto,
          roles: response.roles, permisos: response.permisos,
          expiresAt: Date.now() + response.expiresIn * 1000
        };
        sessionStorage.setItem(KEY, JSON.stringify(session));
        this.state.set(session);
      })
    );
  }

  validSession(): Session | null {
    const session = this.state();
    if (session && session.expiresAt > Date.now()) return session;
    if (session) this.clear();
    return null;
  }
  has(permission: string): boolean { return this.validSession()?.permisos.includes(permission) ?? false; }
  logout() { this.clear(); void this.router.navigate(['/login']); }
  private clear() { sessionStorage.removeItem(KEY); this.state.set(null); }
  private read(): Session | null {
    try {
      const raw = sessionStorage.getItem(KEY);
      const session = raw ? JSON.parse(raw) as Session : null;
      return session && session.expiresAt > Date.now() ? session : null;
    } catch { return null; }
  }
}
