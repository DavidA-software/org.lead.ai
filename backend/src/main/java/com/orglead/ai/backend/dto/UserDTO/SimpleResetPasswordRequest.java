package com.orglead.ai.backend.dto.UserDTO;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class SimpleResetPasswordRequest {
    private String email;
    private String currentPassword;
    private String newPassword;
}

