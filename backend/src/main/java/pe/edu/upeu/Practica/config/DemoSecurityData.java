package pe.edu.upeu.Practica.config;

import java.util.Set;
import java.nio.charset.StandardCharsets;
import org.springframework.boot.ApplicationRunner;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.security.crypto.password.PasswordEncoder;
import pe.edu.upeu.Practica.entity.Empleado;
import pe.edu.upeu.Practica.entity.Rol;
import pe.edu.upeu.Practica.entity.Usuario;
import pe.edu.upeu.Practica.repository.EmpleadoRepository;
import pe.edu.upeu.Practica.repository.RolRepository;
import pe.edu.upeu.Practica.repository.UsuarioRepository;

@Configuration @Profile("dev") @ConditionalOnProperty(name="app.seed-demo-security", havingValue="true")
public class DemoSecurityData {
    @Bean ApplicationRunner seedSecurity(EmpleadoRepository empleados, RolRepository roles,
            UsuarioRepository usuarios, PasswordEncoder encoder) {
        return args -> {
            String password=System.getenv("PHARMA_DEMO_PASSWORD");
            if (password == null || password.length()<8 || password.getBytes(StandardCharsets.UTF_8).length>72
                    || !password.matches("(?s)(?=.*[A-Za-z])(?=.*[0-9]).*"))
                throw new IllegalStateException("PHARMA_DEMO_PASSWORD debe tener 8+ caracteres, letras y números");
            Rol admin=role(roles,"ADMIN","Administración completa");
            Rol vendedor=role(roles,"VENDEDOR","Ventas y clientes");
            Rol almacenero=role(roles,"ALMACENERO","Catálogo e inventario");
            user(empleados,usuarios,encoder,"admin", "90000001",Set.of(admin),password);
            user(empleados,usuarios,encoder,"vendedor", "90000002",Set.of(vendedor),password);
            user(empleados,usuarios,encoder,"almacen", "90000003",Set.of(almacenero),password);
            user(empleados,usuarios,encoder,"supervisor", "90000004",Set.of(vendedor,almacenero),password);
            user(empleados,usuarios,encoder,"inactivo", "90000005",Set.of(vendedor),password);
        };
    }
    private Rol role(RolRepository repository,String name,String description) {
        return repository.findAll().stream().filter(r -> name.equals(r.getNombre())).findFirst().orElseGet(() -> {
            Rol r=new Rol();r.setNombre(name);r.setDescripcion(description);return repository.save(r);
        });
    }
    private void user(EmpleadoRepository empleados,UsuarioRepository usuarios,PasswordEncoder encoder,
            String username,String dni,Set<Rol> assignedRoles,String password) {
        if (usuarios.existsByUsernameIgnoreCase(username)) {
            // Only repair the original demo supervisor; preserve other existing accounts.
            if ("supervisor".equals(username)) usuarios.findByUsernameIgnoreCase(username).ifPresent(existing -> {
                if (empleados.findById(existing.getEmpleado().getId()).map(Empleado::getDni).filter("90000004"::equals).isPresent()
                        && existing.getRoles().stream().map(Rol::getNombre).collect(java.util.stream.Collectors.toSet()).equals(Set.of("SUPERVISOR"))) {
                    existing.setRoles(assignedRoles);
                    usuarios.save(existing);
                }
            });
            return;
        }
        Empleado e=new Empleado();e.setDni(dni);e.setNombres(username.substring(0,1).toUpperCase()+username.substring(1));
        e.setApellidos("Demostración");e.setCargo("Pruebas S10");e.setEmail(username+"@demo.local");
        e=empleados.save(e);
        Usuario u=new Usuario();u.setUsername(username);u.setPassword(encoder.encode(password));
        u.setEmpleado(e);u.setRoles(assignedRoles);
        if ("inactivo".equals(username)) u.setEstado(false);
        usuarios.save(u);
    }
}
