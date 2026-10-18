package pe.edu.upeu.Practica.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import java.time.LocalDateTime;
import java.util.HashSet;
import java.util.Set;

@Entity @Table(name = "usuarios") @Getter @Setter
public class Usuario {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY) private Long id;
    @Column(nullable = false, unique = true, length = 50) private String username;
    @Column(nullable = false, length = 100) private String password;
    @Column(nullable = false) private Boolean estado = true;
    @OneToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "empleado_id", nullable = false, unique = true) private Empleado empleado;
    @ManyToMany(fetch = FetchType.EAGER)
    @JoinTable(name = "usuario_roles", joinColumns = @JoinColumn(name = "usuario_id"),
        inverseJoinColumns = @JoinColumn(name = "rol_id"))
    private Set<Rol> roles = new HashSet<>();
    @Column(name = "fecha_creacion", nullable = false) private LocalDateTime fechaCreacion;
    @Column(name = "fecha_modificacion") private LocalDateTime fechaModificacion;
    @PrePersist void prePersist() { fechaCreacion = LocalDateTime.now(); }
    @PreUpdate void preUpdate() { fechaModificacion = LocalDateTime.now(); }
}
