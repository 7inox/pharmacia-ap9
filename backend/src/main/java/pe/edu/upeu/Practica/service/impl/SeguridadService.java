package pe.edu.upeu.Practica.service.impl;

import java.nio.charset.StandardCharsets;
import java.util.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.domain.Sort;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import pe.edu.upeu.Practica.dto.auth.AuthDtos.*;
import pe.edu.upeu.Practica.entity.*;
import pe.edu.upeu.Practica.exception.RecursosNoEncontradoException;
import pe.edu.upeu.Practica.exception.ReglaNegocioException;
import pe.edu.upeu.Practica.repository.*;
import pe.edu.upeu.Practica.security.*;

@Service
public class SeguridadService {
    private static final Logger log = LoggerFactory.getLogger(SeguridadService.class);
    private final UsuarioRepository usuarios;
    private final EmpleadoRepository empleados;
    private final RolRepository roles;
    private final AuthenticationManager authentication;
    private final PasswordEncoder encoder;
    private final JwtService jwt;
    public SeguridadService(UsuarioRepository usuarios, EmpleadoRepository empleados, RolRepository roles,
            AuthenticationManager authentication, PasswordEncoder encoder, JwtService jwt) {
        this.usuarios=usuarios; this.empleados=empleados; this.roles=roles;
        this.authentication=authentication; this.encoder=encoder; this.jwt=jwt;
    }
    @Transactional(readOnly=true)
    public LoginResponse login(LoginRequest request) {
        var authenticated=authentication.authenticate(
            new UsernamePasswordAuthenticationToken(request.username().trim(), request.password()));
        UserDetails principal=(UserDetails) authenticated.getPrincipal();
        Usuario user=byName(principal.getUsername());
        log.info("Inicio de sesión correcto: {}", user.getUsername());
        return new LoginResponse(jwt.generate(principal,user.getPassword()), "Bearer", jwt.expirationSeconds(), user.getUsername(),
            user.getEmpleado().getNombreCompleto(), PermisosPorRol.roles(user.getRoles()),
            PermisosPorRol.permisos(user.getRoles()));
    }
    @Transactional(readOnly=true) public UsuarioResponse me(String username) { return response(byName(username)); }
    @Transactional
    public void changePassword(String username, CambioPasswordRequest request) {
        Usuario user=byName(username);
        checkPasswordLength(request.passwordNueva());
        if (!encoder.matches(request.passwordActual(), user.getPassword()))
            throw new ReglaNegocioException("La contraseña actual no es correcta");
        if (encoder.matches(request.passwordNueva(), user.getPassword()))
            throw new ReglaNegocioException("La nueva contraseña debe ser distinta de la actual");
        user.setPassword(encoder.encode(request.passwordNueva()));
        log.info("Contraseña cambiada: usuario={}", user.getUsername());
    }
    @Transactional(readOnly=true)
    public List<UsuarioResponse> listUsers() { return usuarios.findAll(Sort.by("username")).stream().map(this::response).toList(); }
    @Transactional(readOnly=true)
    public List<EmpleadoResponse> listEmployees() {
        return empleados.findAll(Sort.by("apellidos","nombres")).stream().map(e ->
            new EmpleadoResponse(e.getId(),e.getDni(),e.getNombres(),e.getApellidos(),e.getCargo(),
                e.getEmail(),e.getEstado(),usuarios.existsByEmpleadoId(e.getId()))).toList();
    }
    @Transactional(readOnly=true)
    public List<RolResponse> listRoles() {
        return roles.findAll(Sort.by("nombre")).stream().map(r ->
            new RolResponse(r.getId(),r.getNombre(),r.getDescripcion(),PermisosPorRol.permisos(List.of(r)))).toList();
    }
    @Transactional
    public UsuarioResponse create(UsuarioRequest request) {
        String username=request.username().trim().toLowerCase(Locale.ROOT);
        checkPasswordLength(request.password());
        Empleado employee=empleados.findById(request.empleadoId()).orElseThrow(() ->
            new RecursosNoEncontradoException("Empleado no encontrado"));
        if (!Boolean.TRUE.equals(employee.getEstado())) throw new ReglaNegocioException("El empleado está inactivo");
        if (usuarios.existsByEmpleadoId(employee.getId())) throw new ReglaNegocioException("El empleado ya tiene un usuario");
        if (usuarios.existsByUsernameIgnoreCase(username)) throw new ReglaNegocioException("Ya existe ese usuario");
        Set<Rol> selected=findRoles(request.rolIds());
        Usuario user=new Usuario(); user.setUsername(username); user.setPassword(encoder.encode(request.password()));
        user.setEmpleado(employee); user.setRoles(selected);
        return response(usuarios.save(user));
    }
    @Transactional
    public UsuarioResponse assignRoles(Long id, AsignarRolesRequest request, String actor) {
        Usuario user=byId(id); Set<Rol> selected=findRoles(request.rolIds());
        if (user.getUsername().equalsIgnoreCase(actor) && user.getRoles().stream().anyMatch(r -> r.getNombre().equals("ADMIN"))
                && selected.stream().noneMatch(r -> r.getNombre().equals("ADMIN")))
            throw new ReglaNegocioException("Un administrador no puede quitarse el rol ADMIN");
        user.setRoles(new HashSet<>(selected));
        return response(user);
    }
    @Transactional
    public UsuarioResponse setState(Long id, EstadoRequest request, String actor) {
        Usuario user=byId(id);
        if (!request.estado() && user.getUsername().equalsIgnoreCase(actor))
            throw new ReglaNegocioException("Un administrador no puede desactivarse a sí mismo");
        user.setEstado(request.estado());
        return response(user);
    }
    private void checkPasswordLength(String password) {
        if (password.getBytes(StandardCharsets.UTF_8).length>72)
            throw new ReglaNegocioException("La contraseña no puede superar 72 bytes");
    }
    private Set<Rol> findRoles(Set<Long> ids) {
        List<Rol> found=roles.findAllById(ids);
        if (found.size()!=ids.size()) throw new RecursosNoEncontradoException("Algún rol no existe");
        return new HashSet<>(found);
    }
    private Usuario byId(Long id) { return usuarios.findById(id).orElseThrow(() -> new RecursosNoEncontradoException("Usuario no encontrado")); }
    private Usuario byName(String username) { return usuarios.findByUsernameIgnoreCase(username).orElseThrow(() -> new RecursosNoEncontradoException("Usuario no encontrado")); }
    private UsuarioResponse response(Usuario u) {
        return new UsuarioResponse(u.getId(),u.getUsername(),u.getEmpleado().getId(),
            u.getEmpleado().getNombreCompleto(),PermisosPorRol.roles(u.getRoles()),
            PermisosPorRol.permisos(u.getRoles()),u.getEstado(),u.getFechaCreacion());
    }
}
