package pe.edu.upeu.Practica.security;

import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import pe.edu.upeu.Practica.entity.Usuario;
import pe.edu.upeu.Practica.repository.UsuarioRepository;

@Service
public class UsuarioDetailsService implements UserDetailsService {
    private final UsuarioRepository repository;
    public UsuarioDetailsService(UsuarioRepository repository) { this.repository = repository; }
    @Override @Transactional(readOnly = true)
    public UserDetails loadUserByUsername(String username) {
        Usuario user = repository.findByUsernameIgnoreCase(username.trim())
            .orElseThrow(() -> new UsernameNotFoundException("Usuario no encontrado"));
        return User.withUsername(user.getUsername()).password(user.getPassword())
            .authorities(PermisosPorRol.authorities(user.getRoles()))
            .disabled(!Boolean.TRUE.equals(user.getEstado()) || !Boolean.TRUE.equals(user.getEmpleado().getEstado()))
            .build();
    }
}
