package com.gnegdev.scanity.entity;

import com.fasterxml.jackson.annotation.JsonBackReference;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import java.time.LocalDateTime;
import java.util.UUID;

@Getter
@Setter
@Entity
@Table(name = "scans")
public class Scan {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "id", nullable = false)
    private UUID id;

    @Column(name = "filename", nullable = false, unique = true, length = 1024)
    private String filename;

    @Column(name = "url", nullable = false, unique = true, length = 1024)
    private String url;

    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "user_id")
    @JsonBackReference
    private User user;

    @Column(name = "date", nullable = false)
    @JdbcTypeCode(SqlTypes.TIMESTAMP)
    private LocalDateTime date;

    @Column(name = "description")
    private String description;

    @Column(name = "name", nullable = false)
    private String name;

}