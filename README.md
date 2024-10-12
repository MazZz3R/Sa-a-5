## About project
The application consists of three individual services:
1. auth_service: handles authentication and authorization.
1. message_service: responsible for handling messages.
1. user_service: manages user related tasks.

Each service is dockerised, they communicate with each other using HTTP.

## Project Structure
```
.
├── docker-compose.yaml
├── auth_service
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── message_service
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── notification_service
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
└── user_service
    ├── Dockerfile
    ├── app.py
    └── requirements.txt
```

## Getting Started

To run the application, you need to install docker first.
Then, run it using `docker compose up`