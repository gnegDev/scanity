package com.gnegdev.scanity.entity;

import com.fasterxml.jackson.annotation.JsonProperty;
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
@Table(name = "scan_analysis")
public class ScanAnalysis {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "id", nullable = false)
    private UUID id;

    @Column(name = "has_illness", nullable = false)
    @JsonProperty("has_illness")
    private Boolean hasIllness = false;

    @Column(name = "diagnosis")
    private String diagnosis;

    @Column(name = "description")
    private String description;

    @Column(name = "date", nullable = false)
    @JdbcTypeCode(SqlTypes.TIMESTAMP)
    private LocalDateTime date;



}