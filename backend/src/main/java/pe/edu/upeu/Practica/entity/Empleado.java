package pe.edu.upeu.Practica.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import java.time.LocalDateTime;

@Entity @Table(name = "empleados") @Getter @Setter
public class Empleado {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY) private Long id;
    @Column(nullable = false, length = 8, unique = true) private String dni;
    @Column(nullable = false, length = 100) private String nombres;
    @Column(nullable = false, length = 100) private String apellidos;
    @Column(nullable = false, length = 60) private String cargo;
    @Column(nullable = false, length = 150, unique = true) private String email;
    @Column(length = 15) private String telefono;
    @Column(nullable = false) private Boolean estado = true;
    @Column(name = "fecha_creacion", nullable = false) private LocalDateTime fechaCreacion;
    @Column(name = "fecha_modificacion") private LocalDateTime fechaModificacion;
    @PrePersist void prePersist() { fechaCreacion = LocalDateTime.now(); }
    @PreUpdate void preUpdate() { fechaModificacion = LocalDateTime.now(); }
    public String getNombreCompleto() { return nombres + " " + apellidos; }
}
