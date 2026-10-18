import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { finalize } from 'rxjs';
import { AuthService } from '../../core/auth/auth.service';

@Component({
  selector: 'app-login', imports: [FormsModule],
  template: `<main class="login-wrap"><form class="card login-card" (ngSubmit)="submit()">
    <p class="eyebrow">PHARMASOFT</p><h1>Iniciar sesión</h1>
    <p class="subtitulo">Accede con tu usuario de la botica.</p>
    @if (error()) { <p class="alerta" role="alert">{{ error() }}</p> }
    <div class="campo"><label for="username">Usuario</label><input id="username" type="text" name="username" autocomplete="username" required [(ngModel)]="username"></div>
    <div class="campo"><label for="password">Contraseña</label><input id="password" type="password" name="password" autocomplete="current-password" required [(ngModel)]="password"></div>
    <button class="btn primario" type="submit" [disabled]="loading()">{{ loading() ? 'Ingresando…' : 'Ingresar' }}</button>
  </form></main>`,
  styles: [`.login-wrap{min-height:100vh;display:grid;place-items:center;padding:24px;background:#edf3fa}.login-card{width:min(420px,100%)}.login-card input{width:100%;padding:12px;border:1px solid #cfd9e5;border-radius:7px;font:inherit}.login-card button{width:100%}`]
})
export class Login {
  private readonly auth = inject(AuthService);
  private readonly router = inject(Router);
  private readonly route = inject(ActivatedRoute);
  username = ''; password = '';
  readonly error = signal(''); readonly loading = signal(false);
  submit() {
    if (this.loading()) return;
    this.error.set(''); this.loading.set(true);
    this.auth.login(this.username, this.password).pipe(finalize(() => this.loading.set(false))).subscribe({
      next: () => {
        const wanted = this.route.snapshot.queryParamMap.get('returnUrl');
        void this.router.navigateByUrl(wanted?.startsWith('/') && !wanted.startsWith('//') ? wanted : '/inicio');
      },
      error: () => this.error.set('Usuario o contraseña incorrectos, o cuenta deshabilitada')
    });
  }
}
