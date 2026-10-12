package com.rit.student.service;

import com.rit.student.model.Student;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

@Service
public class StudentService {

    private final AtomicLong nextId = new AtomicLong(1);
    private final ConcurrentHashMap<Long, Student> students = new ConcurrentHashMap<>();

    public Student create(String name, String prn, String department, Integer year) {
        long id = nextId.getAndIncrement();
        Student student = new Student(id, name, prn, department, year);
        students.put(id, student);
        return student;
    }

    public List<Student> findAll() {
        return students.values().stream()
                .sorted((first, second) -> Long.compare(first.id(), second.id()))
                .toList();
    }

    public Optional<Student> findById(Long id) {
        return Optional.ofNullable(students.get(id));
    }
}
