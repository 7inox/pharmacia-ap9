import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from './auth.service';

export const authGuard: CanActivateFn = (_, state) => {
  const auth = inject(AuthService);
  return auth.validSession() ? true : inject(Router).createUrlTree(['/login'], { queryParams: { returnUrl: state.url } });
};
export const permissionGuard: CanActivateFn = route => {
  const permission = route.data['permission'] as string | undefined;
  return !permission || inject(AuthService).has(permission) ? true : inject(Router).createUrlTree(['/inicio']);
};
