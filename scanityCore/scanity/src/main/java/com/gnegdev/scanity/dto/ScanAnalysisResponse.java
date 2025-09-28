package com.gnegdev.scanity.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import org.springframework.web.multipart.MultipartFile;

import java.time.LocalDateTime;

@Data
public class ScanAnalysisResponse {

    @NotNull
    @JsonProperty("has_illness")
    private final boolean hasIllness;

    @NotBlank
    private final String diagnosis;

    private final String description;

    @NotNull
    private final LocalDateTime date;
}
