package com.gnegdev.scanity.service.db.repository;

import com.gnegdev.scanity.entity.ScanAnalysis;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface ScanAnalysisRepository extends JpaRepository<ScanAnalysis, UUID> {
}