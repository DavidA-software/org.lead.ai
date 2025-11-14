package com.orglead.ai.backend.controller;

import com.orglead.ai.backend.dto.UserDTO.CreateAccountRequest;
import com.orglead.ai.backend.dto.UserDTO.LoginRequest;
import com.orglead.ai.backend.dto.UserDTO.Response;
import com.orglead.ai.backend.service.UserService;
import org.springframework.web.bind.annotation.*;

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

}
