package com.gnegdev.scanity.controller;

import com.gnegdev.scanity.entity.User;
import com.gnegdev.scanity.service.db.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;
import java.util.UUID;

@RestController
@RequestMapping("/scanity/api/users")
@RequiredArgsConstructor
public class UserController {
    private final UserService userService;

    @GetMapping("/{uuid}")
    public ResponseEntity<?> getUserById(@PathVariable("uuid") UUID uuid) {
        Optional<User> user = userService.getUserByUUID(uuid);
        if (user.isEmpty()) {
            return new ResponseEntity<>("User not found", HttpStatus.NOT_FOUND);
        }
        return ResponseEntity.ok(user.get());
    }

}
