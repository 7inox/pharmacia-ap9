package pe.edu.upeu.Practica.config;

import com.fasterxml.jackson.databind.ObjectMapper;
import java.time.LocalDateTime;
import java.util.Map;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.cors.CorsConfigurationSource;
import pe.edu.upeu.Practica.security.JwtAuthenticationFilter;
import pe.edu.upeu.Practica.security.JwtService;
import pe.edu.upeu.Practica.security.UsuarioDetailsService;

@Configuration @EnableWebSecurity @EnableMethodSecurity
public class SecurityConfig {
    @Bean SecurityFilterChain filterChain(HttpSecurity http, JwtService jwt, UsuarioDetailsService users,
            @Qualifier("corsConfigurationSource") CorsConfigurationSource cors) throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        http.csrf(AbstractHttpConfigurer::disable).logout(AbstractHttpConfigurer::disable)
            .cors(c -> c.configurationSource(cors))
            .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(a -> a
                .requestMatchers("/api/v1/auth/login", "/api/health", "/swagger-ui.html",
                    "/swagger-ui/**", "/v3/api-docs/**", "/error").permitAll()
                .requestMatchers(HttpMethod.OPTIONS, "/**").permitAll()
                .requestMatchers(HttpMethod.GET, "/api/v1/categorias/**", "/api/v1/productos/**").hasAuthority("CATALOGO_LEER")
                .requestMatchers("/api/v1/categorias/**", "/api/v1/productos/**").hasAuthority("CATALOGO_ESCRIBIR")
                .requestMatchers(HttpMethod.GET, "/api/v1/clientes/**").hasAuthority("CLIENTES_LEER")
                .requestMatchers("/api/v1/clientes/**").hasAuthority("CLIENTES_ESCRIBIR")
                .requestMatchers(HttpMethod.GET, "/api/v1/ventas/**").hasAuthority("VENTAS_LEER")
                .requestMatchers(HttpMethod.POST, "/api/v1/ventas").hasAuthority("VENTAS_REGISTRAR")
                .requestMatchers("/api/v1/ventas/**").hasAuthority("VENTAS_REGISTRAR")
                .requestMatchers("/api/v1/usuarios/**", "/api/v1/empleados/**", "/api/v1/roles/**").hasAuthority("USUARIOS_ADMINISTRAR")
                .anyRequest().authenticated())
            .exceptionHandling(e -> e
                .authenticationEntryPoint((req, res, ex) -> {
                    res.setHeader("WWW-Authenticate", "Bearer");
                    Object reason = req.getAttribute(JwtAuthenticationFilter.ERROR);
                    writeError(mapper, req.getRequestURI(), res, 401, "Unauthorized",
                        reason == null ? "Debe iniciar sesión para acceder a este recurso" : reason.toString());
                })
                .accessDeniedHandler((req, res, ex) ->
                    writeError(mapper, req.getRequestURI(), res, 403, "Forbidden",
                        "No tiene permisos para realizar esta operación")))
            .addFilterBefore(new JwtAuthenticationFilter(jwt, users), UsernamePasswordAuthenticationFilter.class);
        return http.build();
    }
    private static void writeError(ObjectMapper mapper, String path, jakarta.servlet.http.HttpServletResponse response,
            int status, String error, String message) throws java.io.IOException {
        response.setStatus(status);
        response.setContentType(MediaType.APPLICATION_JSON_VALUE);
        response.setCharacterEncoding("UTF-8");
        mapper.writeValue(response.getWriter(), Map.of("timestamp", LocalDateTime.now().toString(),
            "status", status, "error", error, "message", message, "path", path));
    }
    @Bean PasswordEncoder passwordEncoder() { return new BCryptPasswordEncoder(); }
    @Bean AuthenticationManager authenticationManager(AuthenticationConfiguration configuration) throws Exception {
        return configuration.getAuthenticationManager();
    }
}
