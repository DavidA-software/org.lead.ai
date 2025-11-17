package com.orglead.ai.backend.service;

import com.orglead.ai.backend.dto.UserDTO.CreateAccountRequest;
import com.orglead.ai.backend.dto.UserDTO.ForgotPasswordRequest;
import com.orglead.ai.backend.dto.UserDTO.LoginRequest;
import com.orglead.ai.backend.dto.UserDTO.ResetPasswordRequest;
import com.orglead.ai.backend.dto.UserDTO.Response;
import com.orglead.ai.backend.model.User;
import com.orglead.ai.backend.repository.UserRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.Optional;
import java.util.UUID;

@Service
public class UserService {
    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public Response create(CreateAccountRequest userRequest) {
        try {
            User newUser = User.builder()
                    .email(userRequest.getEmail())
                    .password(userRequest.getPassword())
                    .firstName(userRequest.getFirstName())
                    .lastName(userRequest.getLastName())
                    .build();

            userRepository.save(newUser);

            return Response.builder()
                    .message("User created successfully!")
                    .id(newUser.getId())
                    .email(userRequest.getEmail())
                    .firstName(userRequest.getFirstName())
                    .lastName(userRequest.getLastName())
                    .build();
        } catch (Exception e) {
            return Response.builder()
                    .message("Fail: " + e.getMessage())
                    .build();
        }
    }

    public Response login(LoginRequest userRequest) {
        String requestEmail = userRequest.getEmail();
        String requestPassword = userRequest.getPassword();
        Optional<User> user = userRepository.findByEmailAndPassword(requestEmail, requestPassword);

        if (user.isPresent()) {
            return Response.builder()
                    .message("User successfully logged in!")
                    .id(user.get().getId())
                    .email(user.get().getEmail())
                    .firstName(user.get().getFirstName())
                    .lastName(user.get().getLastName())
                    .build();
        }

        return Response.builder()
                .message("Incorrect credentials!")
                .build();
    }

    public Response update(Long id, CreateAccountRequest userRequest) {
       Optional<User> user = userRepository.findById(id);

       if(user.isPresent()) {
           user.get().setEmail(userRequest.getEmail());
           user.get().setPassword(userRequest.getPassword());
           user.get().setFirstName(userRequest.getFirstName());
           user.get().setLastName(userRequest.getLastName());
          userRepository.save(user.get());

          return Response.builder()
                  .message("Account Updated Successfully!")
                  .id(id)
                  .email(user.get().getEmail())
                  .firstName(user.get().getFirstName())
                  .lastName(user.get().getLastName())
                  .build();
       }
       return Response.builder()
               .message("Unable To Update Account! Unable To Find Account!")
               .build();
    }

    public Response delete(Long id) {
        Optional<User> user = userRepository.findById(id);

        if(user.isPresent()) {
            userRepository.delete(user.get());
            return Response.builder()
                    .message("Account Successfully Deleted")
                    .build();
        }
        return Response.builder()
                .message("Unable To Delete Account! Unable To Find Account!")
                .build();
    }

    public Response forgotPassword(ForgotPasswordRequest request) {
        Optional<User> user = userRepository.findByEmail(request.getEmail());

        if (user.isPresent()) {
            // Generate reset token
            String resetToken = UUID.randomUUID().toString();
            LocalDateTime expiryTime = LocalDateTime.now().plusHours(1); // Token expires in 1 hour

            // Save token and expiry to user
            user.get().setResetToken(resetToken);
            user.get().setResetTokenExpiry(expiryTime);
            userRepository.save(user.get());

            // For simple development: return token directly in response
            // In production, send via email instead
            return Response.builder()
                    .message("Password reset token generated successfully!")
                    .token(resetToken) // Return token directly for simple development
                    .build();
        }

        // For security, don't reveal if email exists or not
        return Response.builder()
                .message("If an account with that email exists, a password reset token has been generated.")
                .build();
    }

    public Response resetPassword(ResetPasswordRequest request) {
        Optional<User> user = userRepository.findByResetToken(request.getToken());

        if (user.isPresent()) {
            // Check if token is expired
            if (user.get().getResetTokenExpiry() == null || 
                user.get().getResetTokenExpiry().isBefore(LocalDateTime.now())) {
                return Response.builder()
                        .message("Password reset token has expired. Please request a new one.")
                        .build();
            }

            // Update password and clear reset token
            user.get().setPassword(request.getNewPassword());
            user.get().setResetToken(null);
            user.get().setResetTokenExpiry(null);
            userRepository.save(user.get());

            return Response.builder()
                    .message("Password has been reset successfully!")
                    .id(user.get().getId())
                    .email(user.get().getEmail())
                    .firstName(user.get().getFirstName())
                    .lastName(user.get().getLastName())
                    .build();
        }

        return Response.builder()
                .message("Invalid or expired reset token.")
                .build();
    }

    public Response simpleResetPassword(String email, String currentPassword, String newPassword) {
        Optional<User> user = userRepository.findByEmailAndPassword(email, currentPassword);

        if (user.isPresent()) {
            // Update password
            user.get().setPassword(newPassword);
            userRepository.save(user.get());

            return Response.builder()
                    .message("Password has been reset successfully!")
                    .id(user.get().getId())
                    .email(user.get().getEmail())
                    .firstName(user.get().getFirstName())
                    .lastName(user.get().getLastName())
                    .build();
        }

        return Response.builder()
                .message("Invalid email or current password.")
                .build();
    }
}
