# EduSphere-Microservices

A microservices-based Learning Management System (LMS) designed for a school environment.  
This project was developed as part of the **IT4020 – Modern Topics in IT** module.

## Project Overview

EduSphere-Microservices is a distributed backend system built using **microservices architecture** to support key school operations such as academic management, homework and assessments, group activities, learning materials, communication, and monitoring.

The system is designed to reflect a real-world school hierarchy, where principals, sectional heads, class teachers, subject teachers, students, and parents interact with different parts of the platform based on their roles and permissions.

## Project Type

This is a **microservices-based backend project**.

Instead of building one large monolithic application, the system is split into multiple independent services. Each service handles a specific business domain and communicates through APIs. An **API Gateway** is used as the single entry point to access all microservices.

## Core Microservices

The project consists of the following services:

1. **Academic Management Service**
   - Manages grades, classes, subjects, streams, timetables, and enrollments.

2. **Homework & Assessment Service**
   - Handles assignment creation, submissions, grading, feedback, and result publishing.

3. **Group Activities Service**
   - Supports group projects, memberships, peer evaluation, and shared submissions.

4. **Learning Materials Service**
   - Manages notes, PDFs, videos, links, and learning resources.

5. **Communication & Student Support Service**
   - Handles notices, alerts, messages, and support-related communication.

6. **Monitoring & Administration Service**
   - Provides dashboards, reports, risk indicators, and analytics for school leadership.

7. **API Gateway**
   - Central entry point for routing requests to all services.

## Key Functionalities

- School structure management
- Class and subject allocation
- Homework and assessment lifecycle
- Student submissions and grading
- Group-based activities and peer assessment
- Learning material publishing and access control
- School-wide and class-level communication
- Monitoring dashboards and reporting
- Centralized API access through gateway
- Swagger API documentation for each service

## Architecture Style

This project follows the **microservices architecture pattern**.

### Main characteristics:
- Independent services for each business domain
- Separate responsibilities for each service
- API-based communication
- Centralized API Gateway
- Scalable and modular design
- Easier maintenance and future extension

## Tech Stacks

- **Backend:** Node.js, Express.js, python, FastAPI
- **FrontEnd:** React 
- **API Gateway:** Express Gateway / custom Express gateway
- **Database:** MongoDB / PostgreSQL
- **Documentation:** Swagger
- **Testing:** Postman
- **Version Control:** Git & GitHub

## Project Structure

```bash
EduSphere-Microservices/
│
├── api-gateway/
├── academic-management-service/
├── homework-assessment-service/
├── group-activities-service/
├── learning-materials-service/
├── communication-student-support-service/
├── monitoring-administration-service/
├── Frontend/
├── docs/
└── README.md
```

## How to Clone the Project

```bash
git clone https://github.com/Dhanithya-Beligolla/EduSphere-Microservices.git
cd EduSphere-Microservices
```

## Example Service Ports
- **API Gateway:** http://localhost:8080
- **Academic Management Service:** http://localhost:3001
- **Homework & Assessment Service:** http://localhost:3002
- **Group Activities Service:** http://localhost:3003
- **Learning Materials Service:** http://localhost:3004
- **Communication & Student Support Service:** http://localhost:3005
- **Monitoring & Administration Service:** http://localhost:3006
