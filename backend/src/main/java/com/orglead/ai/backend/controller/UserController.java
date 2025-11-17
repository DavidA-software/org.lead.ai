package com.orglead.ai.backend.controller;

import com.orglead.ai.backend.dto.UserDTO.CreateAccountRequest;
import com.orglead.ai.backend.dto.UserDTO.ForgotPasswordRequest;
import com.orglead.ai.backend.dto.UserDTO.LoginRequest;
import com.orglead.ai.backend.dto.UserDTO.ResetPasswordRequest;
import com.orglead.ai.backend.dto.UserDTO.Response;
import com.orglead.ai.backend.service.UserService;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("user")
public class UserController {
    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @PostMapping("/create")
    public Response create(@RequestBody CreateAccountRequest userRequest) {
        return userService.create(userRequest);
    }
    @PostMapping("/login")
    public Response login(@RequestBody LoginRequest userRequest) {
        return userService.login(userRequest);
    }

    @PutMapping("/update/{id}")
    public Response update(@PathVariable Long id, @RequestBody CreateAccountRequest userRequest) {
        return userService.update(id, userRequest);
    }
    @DeleteMapping("/delete/{id}")
    public Response delete(@PathVariable Long id){
        return userService.delete(id);
    }

    @PostMapping("/forgot-password")
    public Response forgotPassword(@RequestBody ForgotPasswordRequest request) {
        return userService.forgotPassword(request);
    }

    @PostMapping("/reset-password")
    public Response resetPassword(@RequestBody ResetPasswordRequest request) {
        return userService.resetPassword(request);
    }

    @PostMapping("/simple-reset-password")
    public Response simpleResetPassword(@RequestBody Map<String, String> request) {
        return userService.simpleResetPassword(
            request.get("email"),
            request.get("currentPassword"),
            request.get("newPassword")
        );
    }

}
