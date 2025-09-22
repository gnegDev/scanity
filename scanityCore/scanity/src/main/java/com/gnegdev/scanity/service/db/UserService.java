package com.gnegdev.scanity.service.db;

import com.gnegdev.scanity.dto.CreateUserRequest;
import com.gnegdev.scanity.entity.User;
import com.gnegdev.scanity.service.db.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.Optional;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    public User createUser(CreateUserRequest createUserRequest) {
        User user = new User();

        String password = passwordEncoder.encode(createUserRequest.getPassword());

        user.setName(createUserRequest.getName());
        user.setEmail(createUserRequest.getEmail());
        user.setPassword(password);

        return userRepository.save(user);
    }

    public Optional<User> getUserByEmail(String email) {
        return userRepository.findByEmail(email);
    }

    public Optional<User> getUserByUUID(UUID uuid) {
        return userRepository.findById(uuid);
    }

    public User getUserReferenceByUUID(UUID uuid) {
        return userRepository.getReferenceById(uuid);
    }
}
