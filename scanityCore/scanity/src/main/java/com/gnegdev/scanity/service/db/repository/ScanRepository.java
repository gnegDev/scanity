package com.gnegdev.scanity.service.db.repository;

import com.gnegdev.scanity.entity.Scan;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface ScanRepository extends JpaRepository<Scan, UUID> {


}