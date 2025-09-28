package com.gnegdev.scanity.service.db;

import com.gnegdev.scanity.dto.ScanAnalysisResponse;
import com.gnegdev.scanity.dto.UploadScanRequest;
import com.gnegdev.scanity.entity.Scan;
import com.gnegdev.scanity.entity.ScanAnalysis;
import com.gnegdev.scanity.entity.User;
import com.gnegdev.scanity.service.analysis.AnalysisClient;
import com.gnegdev.scanity.service.db.repository.ScanRepository;
import com.gnegdev.scanity.service.s3.S3ClientService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.time.LocalDateTime;
import java.util.Optional;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class ScanService {
    private final ScanRepository scanRepository;

    private final S3ClientService s3ClientService;
    private final UserService userService;
    private final AnalysisClient analysisClient;
    private final ScanAnalysisService scanAnalysisService;

    public Scan uploadScan(UploadScanRequest uploadScanRequest) throws IOException {
        Scan scan = new Scan();

        User user = userService.getUserReferenceByUUID(uploadScanRequest.getUserId());
        scan.setUser(user);

        String filename = s3ClientService.uploadFile(uploadScanRequest.getFile());
        String url = s3ClientService.getUrl(filename);
        scan.setFilename(filename);
        scan.setUrl(url);

        ScanAnalysisResponse scanAnalysisResponse = analysisClient.analyzeScan(uploadScanRequest);
        System.out.println(scanAnalysisResponse);
        ScanAnalysis scanAnalysis  = scanAnalysisService.uploadScanAnalysis(scanAnalysisResponse);
        scan.setScanAnalysis(scanAnalysis);

        scan.setName(uploadScanRequest.getName());
        scan.setDate(uploadScanRequest.getDate());
        scan.setDescription(uploadScanRequest.getDescription());

        return scanRepository.save(scan);
    }

    public Optional<Scan> getScanByUUID(UUID uuid) {
        return scanRepository.findById(uuid);
    }
}
