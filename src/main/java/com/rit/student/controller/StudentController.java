package com.rit.student.controller;

import com.rit.student.model.Student;
import com.rit.student.service.StudentService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/students")
public class StudentController {

    private final StudentService studentService;

    public StudentController(StudentService studentService) {
        this.studentService = studentService;
    }

    @PostMapping
    public ResponseEntity<Student> create(@RequestBody StudentRequest request) {
        if (request == null || !hasText(request.name()) || !hasText(request.prn())
                || !hasText(request.department()) || request.year() == null) {
            return ResponseEntity.badRequest().build();
        }

        Student student = studentService.create(
                request.name().trim(),
                request.prn().trim(),
                request.department().trim(),
                request.year());
        return ResponseEntity.status(HttpStatus.CREATED).body(student);
    }

    @GetMapping
    public List<Student> findAll() {
        return studentService.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Student> findById(@PathVariable Long id) {
        return studentService.findById(id)
                .map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    private boolean hasText(String value) {
        return value != null && !value.isBlank();
    }
}
