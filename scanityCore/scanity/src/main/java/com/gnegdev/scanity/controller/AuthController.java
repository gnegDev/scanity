package com.gnegdev.scanity.controller;

import com.gnegdev.scanity.dto.CreateUserRequest;
import com.gnegdev.scanity.dto.LogInUserRequest;
import com.gnegdev.scanity.entity.User;
import com.gnegdev.scanity.service.auth.AuthService;
import com.gnegdev.scanity.service.db.UserService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@RestController
@RequestMapping("/scanity/api/auth")
@RequiredArgsConstructor
public class AuthController {
    private final UserService userService;
    private final AuthService authService;

    @PostMapping("/signin")
    public ResponseEntity<User> createUser(@Valid @RequestBody CreateUserRequest createUserRequest) {
        User user = userService.createUser(createUserRequest);
        return new ResponseEntity<>(user, HttpStatus.CREATED);
    }

    @PostMapping("/login")
    public ResponseEntity<?> logInUser(@Valid @RequestBody LogInUserRequest logInUserRequest) {
        Optional<User> user = userService.getUserByEmail(logInUserRequest.getEmail());

        if (user.isEmpty() || !authService.checkPassword(logInUserRequest.getPassword(), user.get().getPassword())) {
            return new ResponseEntity<>("Incorrect login or password", HttpStatus.UNAUTHORIZED);
        } else {
            return new ResponseEntity<>(user, HttpStatus.OK);
        }
    }
}
