import { HttpErrorResponse, HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, throwError } from 'rxjs';
import { environment } from '../../../environments/environment';
import { AuthService } from './auth.service';

export const authInterceptor: HttpInterceptorFn = (request, next) => {
  const auth = inject(AuthService);
  const session = auth.validSession();
  const apiRequest = request.url.startsWith(environment.apiUrl);
  const outgoing = apiRequest && session ? request.clone({
    setHeaders: { Authorization: `Bearer ${session.token}` }
  }) : request;
  return next(outgoing).pipe(catchError((error: HttpErrorResponse) => {
    if (apiRequest && error.status === 401 && !request.url.endsWith('/auth/login')) auth.logout();
    return throwError(() => error);
  }));
};
