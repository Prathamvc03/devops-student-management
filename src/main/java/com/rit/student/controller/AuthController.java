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
        boolean hasIdentifier = hasText(request.username()) || hasText(request.email());
        if (!hasIdentifier || !hasText(request.password())) {
            return invalidCredentials();
        }

        return ResponseEntity.ok(new AuthResponse(true, "Login successful", DUMMY_TOKEN));
    }

    private ResponseEntity<AuthResponse> invalidCredentials() {
        return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                .body(new AuthResponse(false, "Invalid credentials", null));
    }

    private boolean hasText(String value) {
        return value != null && !value.isBlank();
    }
}
