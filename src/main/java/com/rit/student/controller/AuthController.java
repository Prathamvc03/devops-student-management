package com.rit.student.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private static final String DUMMY_TOKEN = "dummy-auth-token";

    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(@RequestBody LoginRequest request) {
        if (request == null) {
            return invalidCredentials();
        }

        boolean hasIdentifier = hasText(request.username()) || hasText(request.email());
        if (!hasIdentifier || !hasText(request.password())) {
            return invalidCredentials();
        }

        return ResponseEntity.ok(new AuthResponse(true, "Login successful", DUMMY_TOKEN));
    }

    @PostMapping("/register")
    public ResponseEntity<RegistrationResponse> register(@RequestBody RegistrationRequest request) {
        if (request == null || !hasText(request.name()) || !hasText(request.email())
                || !hasText(request.password())) {
            return ResponseEntity.badRequest()
                    .body(new RegistrationResponse(false, "Name, email, and password are required"));
        }

        return ResponseEntity.status(HttpStatus.CREATED)
                .body(new RegistrationResponse(true, "Registration successful"));
    }

    private ResponseEntity<AuthResponse> invalidCredentials() {
        return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                .body(new AuthResponse(false, "Invalid credentials", null));
    }

    private boolean hasText(String value) {
        return value != null && !value.isBlank();
    }
}
