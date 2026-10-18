package pe.edu.upeu.Practica.controller;

import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;
import pe.edu.upeu.Practica.dto.auth.AuthDtos.*;
import pe.edu.upeu.Practica.service.impl.SeguridadService;

@RestController @RequestMapping("/api/v1/auth")
public class AuthController {
    private final SeguridadService service;
    public AuthController(SeguridadService service) { this.service=service; }
    @PostMapping("/login") public LoginResponse login(@Valid @RequestBody LoginRequest request) {
        return service.login(request);
    }
    @GetMapping("/me") public UsuarioResponse me(Authentication auth) { return service.me(auth.getName()); }
    @PutMapping("/password") public ResponseEntity<Void> password(Authentication auth,
            @Valid @RequestBody CambioPasswordRequest request) {
        service.changePassword(auth.getName(),request);
        return ResponseEntity.noContent().build();
    }
}
