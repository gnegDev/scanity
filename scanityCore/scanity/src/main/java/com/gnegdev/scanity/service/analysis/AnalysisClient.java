package com.gnegdev.scanity.service.analysis;

import com.gnegdev.scanity.dto.ScanAnalysisResponse;
import com.gnegdev.scanity.dto.UploadScanRequest;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.core.io.Resource;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestClient;

import java.io.IOException;

@Service
public class AnalysisClient {
    @Value("${analysis.endpoint}")
    private String endpoint;

    private final RestClient restClient = RestClient.create();

    public ScanAnalysisResponse analyzeScan(UploadScanRequest request) throws IOException {
        // Подготовка частей для multipart запроса
        MultiValueMap<String, Object> parts = new LinkedMultiValueMap<>();

        parts.add("userId", request.getUserId().toString());
        parts.add("date", request.getDate().toString());
        parts.add("name", request.getName());
        parts.add("description", request.getDescription());

        // Конвертация MultipartFile в Resource
        Resource fileResource = new ByteArrayResource(request.getFile().getBytes()) {
            @Override
            public String getFilename() {
                return request.getFile().getOriginalFilename();
            }
        };

        parts.add("file", fileResource);

        // Отправка запроса
        ResponseEntity<ScanAnalysisResponse> response = restClient.post()
                .uri(endpoint + "/analyze")
                .contentType(MediaType.MULTIPART_FORM_DATA)
                .body(parts)
                .retrieve()
                .toEntity(ScanAnalysisResponse.class);

        return response.getBody();
    }
}