package com.gnegdev.scanity.dto;

import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import org.springframework.web.multipart.MultipartFile;

import java.time.LocalDateTime;
import java.util.UUID;

@Data
public class UploadScanRequest {
    @JsonProperty(value = "user_id")
    @JsonAlias(value = "user_id")
    private final UUID userId;

    @NotNull
    private final MultipartFile file;

    @NotNull
    private final MultipartFile dicom;

    private final LocalDateTime date;

    private final String name;

    private final String description;
}
