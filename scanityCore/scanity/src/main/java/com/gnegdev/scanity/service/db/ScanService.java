package com.gnegdev.scanity.service.db;

import com.gnegdev.scanity.dto.UploadScanRequest;
import com.gnegdev.scanity.entity.Scan;
import com.gnegdev.scanity.entity.User;
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
    private final S3ClientService s3ClientService;
    private final ScanRepository scanRepository;
    private final UserService userService;

    public Scan uploadScan(UploadScanRequest uploadScanRequest) throws IOException {
        Scan scan = new Scan();

        String filename = s3ClientService.uploadFile(uploadScanRequest);
        String url = s3ClientService.getUrl(filename);

        User user = userService.getUserReferenceByUUID(uploadScanRequest.getUserId());

        scan.setFilename(filename);

        scan.setUrl(url);
        scan.setUser(user);

        scan.setName(uploadScanRequest.getName());
        scan.setDate(uploadScanRequest.getDate());
        scan.setDescription(uploadScanRequest.getDescription());

        return scanRepository.save(scan);
    }

    public Optional<Scan> getScanByUUID(UUID uuid) {
        return scanRepository.findById(uuid);
    }
}
