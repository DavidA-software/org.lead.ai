package com.orglead.ai.backend.service;

import com.orglead.ai.backend.dto.UserDTO.CreateAccountRequest;
import com.orglead.ai.backend.dto.UserDTO.LoginRequest;
import com.orglead.ai.backend.dto.UserDTO.Response;
import com.orglead.ai.backend.model.User;
import com.orglead.ai.backend.repository.UserRepository;
import org.springframework.stereotype.Service;

import java.util.Optional;

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
}
