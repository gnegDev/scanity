package com.gnegdev.scanity.service.db;

import com.gnegdev.scanity.dto.ScanAnalysisResponse;
import com.gnegdev.scanity.dto.UploadScanRequest;
import com.gnegdev.scanity.entity.Scan;
import com.gnegdev.scanity.entity.ScanAnalysis;
import com.gnegdev.scanity.entity.User;
import com.gnegdev.scanity.service.db.repository.ScanAnalysisRepository;
import com.gnegdev.scanity.service.db.repository.ScanRepository;
import com.gnegdev.scanity.service.s3.S3ClientService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.Optional;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class ScanAnalysisService {
    private final ScanAnalysisRepository scanAnalysisRepository;

    public ScanAnalysis uploadScanAnalysis(ScanAnalysisResponse scanAnalysisResponse) {
        ScanAnalysis scanAnalysis = new ScanAnalysis();

        scanAnalysis.setHasIllness(scanAnalysisResponse.isHasIllness());
        scanAnalysis.setDiagnosis(scanAnalysisResponse.getDiagnosis());
        scanAnalysis.setDescription(scanAnalysisResponse.getDescription());
        scanAnalysis.setDate(scanAnalysisResponse.getDate());

        return scanAnalysisRepository.save(scanAnalysis);
    }

}
