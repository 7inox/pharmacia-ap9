package pe.edu.upeu.Practica.controller;

import jakarta.validation.Valid;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;
import pe.edu.upeu.Practica.dto.auth.AuthDtos.*;
import pe.edu.upeu.Practica.service.impl.SeguridadService;

@RestController @RequestMapping("/api/v1")
public class UsuarioController {
    private final SeguridadService service;
    public UsuarioController(SeguridadService service) { this.service=service; }
    @GetMapping("/usuarios") public List<UsuarioResponse> list() { return service.listUsers(); }
    @PostMapping("/usuarios") public ResponseEntity<UsuarioResponse> create(@Valid @RequestBody UsuarioRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED).body(service.create(request));
    }
    @PutMapping("/usuarios/{id}/roles") public UsuarioResponse roles(@PathVariable Long id,
            @Valid @RequestBody AsignarRolesRequest request, Authentication auth) {
        return service.assignRoles(id,request,auth.getName());
    }
    @PatchMapping("/usuarios/{id}/estado") public UsuarioResponse state(@PathVariable Long id,
            @Valid @RequestBody EstadoRequest request, Authentication auth) {
        return service.setState(id,request,auth.getName());
    }
    @GetMapping("/empleados") public List<EmpleadoResponse> employees() { return service.listEmployees(); }
    @GetMapping("/roles") public List<RolResponse> roles() { return service.listRoles(); }
}
