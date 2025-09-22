package com.gnegdev.scanity.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class LogInUserRequest {
    @NotBlank
    String email;

    @NotBlank
    String password;
}
