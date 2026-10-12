# devops-student-management
DevOps-Based Student Management Web Application

## Spring Boot API

Run the tests with `mvn test`, then start the API with `mvn spring-boot:run`.
The demo login endpoint is `POST /api/auth/login` and accepts JSON with either
a `username` or `email`, plus a non-blank `password`. It returns a dummy token
when both are present; this is not production authentication.
