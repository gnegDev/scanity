package com.gnegdev.scanity.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import org.springframework.web.multipart.MultipartFile;

import java.time.LocalDateTime;
import java.util.UUID;

@Data
public class UploadScanRequest {
    @NotNull
    private final MultipartFile file;

    private final LocalDateTime date;

    @JsonProperty(value = "user_id")
    private final UUID userId;

    private final String description;
}
