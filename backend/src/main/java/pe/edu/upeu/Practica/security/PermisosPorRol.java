package pe.edu.upeu.Practica.security;

import java.util.*;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import pe.edu.upeu.Practica.entity.Rol;

public final class PermisosPorRol {
    private static final Set<String> TODOS = Set.of("CATALOGO_LEER", "CATALOGO_ESCRIBIR",
        "CLIENTES_LEER", "CLIENTES_ESCRIBIR", "VENTAS_LEER", "VENTAS_REGISTRAR",
        "REPORTES_VER", "USUARIOS_ADMINISTRAR");
    private static final Map<String, Set<String>> MAPA = Map.of(
        "ADMIN", TODOS,
        "VENDEDOR", Set.of("CATALOGO_LEER", "CLIENTES_LEER", "CLIENTES_ESCRIBIR", "VENTAS_LEER", "VENTAS_REGISTRAR"),
        "ALMACENERO", Set.of("CATALOGO_LEER", "CATALOGO_ESCRIBIR"));
    private PermisosPorRol() {}
    public static List<String> roles(Collection<Rol> roles) {
        return roles.stream().map(Rol::getNombre).sorted().toList();
    }
    public static List<String> permisos(Collection<Rol> roles) {
        return roles.stream().flatMap(r -> MAPA.getOrDefault(r.getNombre(), Set.of()).stream())
            .distinct().sorted().toList();
    }
    public static List<GrantedAuthority> authorities(Collection<Rol> roles) {
        List<GrantedAuthority> result = new ArrayList<>();
        roles(roles).forEach(r -> result.add(new SimpleGrantedAuthority("ROLE_" + r)));
        permisos(roles).forEach(p -> result.add(new SimpleGrantedAuthority(p)));
        return result;
    }
}
