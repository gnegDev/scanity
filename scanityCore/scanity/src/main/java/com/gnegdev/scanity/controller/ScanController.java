package com.gnegdev.scanity.controller;

import com.gnegdev.scanity.dto.UploadScanRequest;
import com.gnegdev.scanity.entity.Scan;
import com.gnegdev.scanity.service.db.ScanService;
import com.gnegdev.scanity.service.s3.S3ClientService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.util.Optional;
import java.util.UUID;

@RestController
@RequestMapping("/scanity/api/scans")
@RequiredArgsConstructor
public class ScanController {
    private final ScanService scanService;
    private final S3ClientService s3ClientService;

    @PostMapping(path = "/upload")
    public ResponseEntity<Scan> uploadScan(@Valid @ModelAttribute UploadScanRequest uploadScanRequest) throws IOException {
        Scan scan = scanService.uploadScan(uploadScanRequest);

        return new ResponseEntity<>(scan, HttpStatus.CREATED);
    }

    @GetMapping("/{uuid}")
    public ResponseEntity<?> getScanById(@PathVariable("uuid") UUID uuid) {
        Optional<Scan> scan = scanService.getScanByUUID(uuid);
        if (scan.isEmpty()) {
            return new ResponseEntity<>("Scan not found", HttpStatus.NOT_FOUND);
        }
        return ResponseEntity.ok(scan.get());
    }

    @DeleteMapping("/delete/{uuid}")
    public ResponseEntity<?> deleteScanById(@PathVariable("uuid") UUID uuid) {
        scanService.deleteScanByUUID(uuid);
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }

    @GetMapping("/file/{filename}")
    public ResponseEntity<byte[]> getScanFile(@PathVariable("filename") String filename) throws IOException {
        byte[] data = s3ClientService.getFile(filename);

        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=" + filename)
                .body(data);
    }
}
