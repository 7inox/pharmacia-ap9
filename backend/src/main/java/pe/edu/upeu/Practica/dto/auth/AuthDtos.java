package pe.edu.upeu.Practica.dto.auth;

import jakarta.validation.constraints.*;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Set;

public final class AuthDtos {
    private AuthDtos() {}
    public record LoginRequest(@NotBlank String username, @NotBlank String password) {}
    public record LoginResponse(String token, String tipo, long expiresIn, String username,
        String nombreCompleto, List<String> roles, List<String> permisos) {}
    public record UsuarioRequest(@NotBlank String username,
        @NotBlank @Size(min=8, max=72) @Pattern(regexp="(?s)(?=.*[A-Za-z])(?=.*[0-9]).*") String password,
        @NotNull Long empleadoId, @NotEmpty Set<@NotNull Long> rolIds) {}
    public record UsuarioResponse(Long id, String username, Long empleadoId, String empleado,
        List<String> roles, List<String> permisos, Boolean estado, LocalDateTime fechaCreacion) {}
    public record EmpleadoResponse(Long id, String dni, String nombres, String apellidos, String cargo,
        String email, Boolean estado, boolean tieneUsuario) {}
    public record RolResponse(Long id, String nombre, String descripcion, List<String> permisos) {}
    public record CambioPasswordRequest(@NotBlank String passwordActual,
        @NotBlank @Size(min=8, max=72) @Pattern(regexp="(?s)(?=.*[A-Za-z])(?=.*[0-9]).*") String passwordNueva) {}
    public record AsignarRolesRequest(@NotEmpty Set<@NotNull Long> rolIds) {}
    public record EstadoRequest(@NotNull Boolean estado) {}
}
