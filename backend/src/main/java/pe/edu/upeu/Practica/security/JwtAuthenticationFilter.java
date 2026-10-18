package pe.edu.upeu.Practica.security;

import io.jsonwebtoken.ExpiredJwtException;
import io.jsonwebtoken.JwtException;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import org.springframework.http.HttpHeaders;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.web.filter.OncePerRequestFilter;

public class JwtAuthenticationFilter extends OncePerRequestFilter {
    public static final String ERROR = "jwt.error";
    private final JwtService jwt;
    private final UsuarioDetailsService users;
    public JwtAuthenticationFilter(JwtService jwt, UsuarioDetailsService users) { this.jwt = jwt; this.users = users; }
    @Override protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain chain)
        throws ServletException, IOException {
        String header = request.getHeader(HttpHeaders.AUTHORIZATION);
        if (header != null && header.startsWith("Bearer ")) {
            try {
                var claims=jwt.claims(header.substring(7).trim());
                String username = claims.getSubject();
                UserDetails user = users.loadUserByUsername(username);
                if (!jwt.currentCredential(claims,user)) request.setAttribute(ERROR,"El token fue revocado por cambio de contraseña");
                else if (user.isEnabled()) {
                    var auth = new UsernamePasswordAuthenticationToken(user, null, user.getAuthorities());
                    auth.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));
                    SecurityContextHolder.getContext().setAuthentication(auth);
                } else request.setAttribute(ERROR, "El usuario está deshabilitado");
            } catch (ExpiredJwtException ex) {
                request.setAttribute(ERROR, "El token ha expirado. Inicie sesión nuevamente");
            } catch (UsernameNotFoundException ex) {
                request.setAttribute(ERROR, "El usuario del token no existe");
            } catch (JwtException | IllegalArgumentException ex) {
                request.setAttribute(ERROR, "El token no es válido");
            }
        }
        chain.doFilter(request, response);
    }
}
