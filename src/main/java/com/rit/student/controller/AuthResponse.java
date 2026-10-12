package com.rit.student.controller;

public record AuthResponse(boolean success, String message, String token) {
}
