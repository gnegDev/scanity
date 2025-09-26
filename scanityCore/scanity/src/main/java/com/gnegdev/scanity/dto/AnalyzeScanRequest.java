package com.gnegdev.scanity.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import org.springframework.web.multipart.MultipartFile;

import java.time.LocalDateTime;

@Data
public class AnalyzeScanRequest {


    @NotNull
    private final boolean has_illness;

    @NotBlank
    private final String diagnosis;

    private final String description;

    @NotNull
    private final LocalDateTime date;

    @NotNull
    private final MultipartFile file;
}
