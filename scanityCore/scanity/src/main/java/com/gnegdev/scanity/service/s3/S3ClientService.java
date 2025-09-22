package com.gnegdev.scanity.service.s3;

import com.gnegdev.scanity.dto.UploadScanRequest;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import software.amazon.awssdk.core.ResponseInputStream;
import software.amazon.awssdk.core.sync.RequestBody;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.GetObjectRequest;
import software.amazon.awssdk.services.s3.model.GetObjectResponse;
import software.amazon.awssdk.services.s3.model.PutObjectRequest;

import java.io.IOException;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class S3ClientService {
    private final S3Client s3Client;

    @Value("${minio.bucket}")
    private String bucket;

    public String uploadFile(UploadScanRequest fileUploadRequest) throws IOException {
        MultipartFile file = fileUploadRequest.getFile();

        String filename = UUID.randomUUID() + "_" + file.getOriginalFilename();

        PutObjectRequest request = PutObjectRequest.builder()
                .bucket(bucket)
                .key(filename)
                .contentType(file.getContentType())
                .build();

        s3Client.putObject(request, RequestBody.fromBytes(file.getBytes()));
        return filename;
    }

    public byte[] getFile(String filename) throws IOException {
        GetObjectRequest request = GetObjectRequest.builder()
                .bucket(bucket)
                .key(filename)
                .build();

        ResponseInputStream<GetObjectResponse> stream = s3Client.getObject(request);
        return stream.readAllBytes();
    }

}
